import datetime
import json
import time

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, func, ForeignKey, and_
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT

from . import db, sha3

td = datetime.timedelta(days=+1)


def _x(data):
    """
    将多个数据格式化
    :param data:
    :return:
    """
    new_data = []
    for _ in data:
        d = _.__dict__
        try:
            d.pop("_sa_instance_state")
        except KeyError:
            print(f"{d}中没有属性")
        if d.get("create_time", 0):
            d["create_time"] = d["create_time"].__str__()
        new_data.append(d)
    return new_data


def _y(data):
    """
    将预约时间段取反
    :param data:
    :return:
    """
    date = datetime.datetime.now()
    y = date.year
    m = date.month
    d = date.day
    # 获取配置项
    _open_time = OptionModel.get_option_by_name("open_time")["value"]
    _close_time = OptionModel.get_option_by_name("close_time")["value"]

    # 获取今天的开启关闭时间
    open_time = datetime.datetime.strptime(f"{y}-{m}-{d} {_open_time}", "%Y-%m-%d %H:%M")
    close_time = datetime.datetime.strptime(f"{y}-{m}-{d} {_close_time}", "%Y-%m-%d %H:%M")

    # 可用时间段
    time_d = [int(open_time.timestamp()), int(close_time.timestamp())]

    data.sort()
    for td in data:
        # 如果不是今天就跳过
        if td[0] < time_d[0] or td[1] > time_d[-1]:
            continue
        time_d.insert(-1, td[0])
        time_d.insert(-1, td[1])

    # 返回可用时间段
    print(time_d)
    return list(zip(*[iter(time_d)] * 2))


def check():
    now = int(time.time())
    # 迟到线
    timeout = now - int(OptionModel.get_option_by_name("time_out")["value"])
    # 迟到的预约
    # a = ReservationModel.query.all()
    # for _ in a:
    #     print(_.__dict__)
    timeout_reservations = ReservationModel.query.filter(ReservationModel.status == 1,
                                                         ReservationModel.start_time < timeout).all()
    # 完成的预约
    expire_reservations = ReservationModel.query.filter(ReservationModel.status.in_(["3", "5"]),
                                                        ReservationModel.start_time < timeout).all()
    # print(len(timeout_reservations), len(expire_reservations), now)
    for t in timeout_reservations:
        t.status = 6
        db.session.commit()
    for e in expire_reservations:
        e.status = 4
        db.session.commit()


class BuildingModel(db.Model):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, comment='场馆名称')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='开启')

    @staticmethod
    def get_buildings():
        """
        获取所有分馆
        :return:
        """
        building = BuildingModel.query.all()
        return _x(building)

    @staticmethod
    def get_rooms_by_building(building_id):
        """
        获取分馆里的所有房间
        :param building_id:
        :return:
        """
        rooms = RoomModel.query.filter(RoomModel.building_id == building_id).all()
        return _x(rooms)

    @staticmethod
    def add_building(data):
        """
        添加分馆
        :return:
        """
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def del_building(building_id):
        """
        删除分馆
        :return:
        """
        res = BuildingModel.query.filter(BuildingModel.id == building_id).delete()
        db.session.commit()
        return bool(res)

    @staticmethod
    def edit_building(building_id, name=None, enabled=None):
        """
        编辑分馆
        :return:
        """
        building = BuildingModel.query.filter(BuildingModel.id == building_id).first()
        if name is not None:
            building.name = name
        if enabled is not None:
            building.enabled = enabled
        db.session.commit()


class OptionModel(db.Model):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, comment='配置项')
    value = Column(LONGTEXT, nullable=False, comment='配置值')

    @staticmethod
    def is_option_exist(name):
        """
        判断设置是否存在
        :param name:
        :return:
        """
        return bool(OptionModel.query.filter(OptionModel.name == name).first())

    @staticmethod
    def get_options():
        """
        获取所有配置项
        :return:
        """
        return _x(OptionModel.query.all())

    @staticmethod
    def get_option_by_name(name):
        """
        获取指定配置项
        :param name:
        :return:
        """
        return _x([OptionModel.query.filter(OptionModel.name == name).first()])[0]

    @staticmethod
    def update_option(name, value):
        """
        修改配置项
        :param name:
        :param value:
        :return:
        """
        option = OptionModel.query.filter(OptionModel.name == name).first()
        if option is None:
            return False
        option.value = value
        db.session.commit()
        return True


# 可持续状态
normal_status = ["1", "3", "5"]
# 不可持续状态
over_status = ["2", "4", "6"]


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    seat_id = Column(Integer, ForeignKey('seat.id'), nullable=False, comment='座位ID')
    start_time = Column(Integer, nullable=False, comment='预约开始时间')
    end_time = Column(Integer, nullable=False, comment='预约结束时间')
    # cancelled = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='取消')
    # 1: 预约；2: 取消；3:进行中；4: 关闭；5：离开；6：迟到
    status = Column(Integer, nullable=False, server_default=text("'1'"), comment='状态')
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='预约创建时间')

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        获取用户所有预约
        :param user_id:
        :return:
        """
        # Fixme: 多表查询座位
        # reservations = ReservationModel.query.filter(ReservationModel.user_id == user_id).all()
        _reservations = db.session.query(ReservationModel, SeatModel.room_id) \
            .select_from(ReservationModel) \
            .join(SeatModel, ReservationModel.seat_id == SeatModel.id) \
            .all()
        print(_reservations)
        reservations = []
        # for _ in reservations:
        #     _[0]["seat_id"] = _[1]
        for _ in _reservations:
            a = _[0].__dict__
            a["room_id"] = _[1]
            a["create_time"] = a["create_time"].__str__()
            a.pop("_sa_instance_state")
            reservations.append(a)
        print(reservations)
        return reservations

    @staticmethod
    def get_enabled_reservations_by_user_id(user_id):
        """
        获取用户有效预约
        :param user_id:
        :return:
        """
        reservations = ReservationModel.query.filter(ReservationModel.user_id == user_id).all()
        for _ in reservations:
            if str(_.status) in over_status:
                reservations.remove(_)
        return _x(reservations)

    @staticmethod
    def get_reservations_by_reservation_id(reservation_id):
        """
        获取预约详情
        :param reservation_id:
        :return:
        """
        reservation = ReservationModel.query.filter(ReservationModel.id == reservation_id).all()
        return _x(reservation)

    @staticmethod
    def get_reservations_by_seat_id(seat_id):
        """
        获取座位没有当前所有有效预约
        :param seat_id:
        :return:
        """
        reservations = ReservationModel.query.filter(ReservationModel.seat_id == seat_id).all()
        res = _x(reservations)
        for _r in range(len(res)):
            if str(res[_r]["status"]) in over_status:
                res.pop(_r)
        return res

    @staticmethod
    def get_time_slot_by_seat_id(seat_id):
        """
        获取座位的有效预约时间段
        :return:
        """
        reservations = ReservationModel.query.filter(ReservationModel.seat_id == seat_id).all()
        times = []
        for _r in reservations:
            if str(_r.status) in normal_status:
                times.append([_r.start_time, _r.end_time])
        return _y(times)

    @staticmethod
    def add_reservation(user_id, seat_id, start_time, end_time):
        """
        增加预约
        :return:
        """
        data = ReservationModel(user_id=user_id, seat_id=seat_id, start_time=start_time, end_time=end_time)
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def cancel(reservation_id):
        """
        取消预约
        :param reservation_id:
        :return:
        """
        reservation = ReservationModel.query.filter(ReservationModel.id == reservation_id).all()
        if not bool(reservation):
            return False
        else:
            if str(reservation[0].status) == "1":
                reservation[0].status = 2
                db.session.commit()
                return True
            else:
                return False

    @staticmethod
    def close(reservation_id):
        """
        终止预约
        :param reservation_id:
        :return:
        """
        reservation = ReservationModel.query.filter(ReservationModel.id == reservation_id).all()
        if not bool(reservation):
            return False
        else:
            if str(reservation[0].status) in ["3", "5"]:
                reservation[0].status = 2
                db.session.commit()
                return True
            else:
                return False


class RoomModel(db.Model):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='房间名称')
    building_id = Column(Integer, ForeignKey('building.id'), nullable=False, comment='启用')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='启用')

    @staticmethod
    def get_rooms():
        rooms = RoomModel.query.all()
        return _x(rooms)

    @staticmethod
    def get_room_by_id(id):
        room = RoomModel.query.filter(RoomModel.id == id).all()
        return _x(room)[0]

    @staticmethod
    def get_seats_by_room_id(room_id):
        seats = SeatModel.query.filter(SeatModel.room_id == room_id).all()
        return _x(seats)

    @staticmethod
    def add_room(name, building_id, enabled):
        """
        添加新的房间
        :param name:
        :param building_id:
        :param enabled:
        :return:
        """
        room = RoomModel(name=name, building_id=building_id, enabled=enabled)
        db.session.add(room)
        db.session.commit()

    @staticmethod
    def update_room_by_id(room_id, name=None, building_id=None, enabled=None):
        """
        更新房间
        :param room_id:
        :param name:
        :param building_id:
        :param enabled:
        :return:
        """
        room = RoomModel.query.filter(RoomModel.id == room_id).all()
        if len(room):
            room[0].name = name or room[0].name
            room[0].building_id = building_id or room[0].building_id
            room[0].enabled = enabled or room[0].enabled
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def del_room_by_id(room_id):
        """
        删除房间
        :param room_id:
        :return:
        """
        res = RoomModel.query.filter(RoomModel.id == room_id).delete()
        db.session.commit()
        return bool(res)


class SeatModel(db.Model):
    __tablename__ = 'seat'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, comment='房间ID')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='启用')

    @staticmethod
    def get_time_slot_by_seat_id(seat_id):
        """
        获取座位的有效预约时段
        :param seat_id:
        :return:
        """
        return ReservationModel.get_time_slot_by_seat_id(seat_id)

    @staticmethod
    def is_exist(id):
        """
        判断座位是否存在
        :param id:
        :return:
        """
        return bool(SeatModel.query.filter(SeatModel.id == id).first())

    @staticmethod
    def is_usable_seat(id):
        """
        座位是否启用
        :return:
        """
        return SeatModel.query.filter(SeatModel.id == id).first().enabled

    @staticmethod
    def get_seats():
        """
        获取所有的座位
        :return:
        """
        seats = SeatModel.query.all()
        return _x(seats)

    @staticmethod
    def get_seats_by_room_id(room_id):
        """
        根据房间查找座位
        :param room_id:
        :return:
        """
        seats = SeatModel.query.filter(SeatModel.room_id == room_id).all()
        return _x(seats)

    @staticmethod
    def get_seat_by_id(id):
        """
        通过座位 id 查找座位
        :param id:
        :return:
        """
        seat = SeatModel.query.filter(SeatModel.id == id).all()
        return _x(seat)[0]


class UserModel(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True, comment='学号教工号')
    password = Column(String(255), nullable=False, comment='密码')
    name = Column(String(40), nullable=False, comment='姓名')
    school = Column(String(100), nullable=False, comment='学校')
    college = Column(String(100), nullable=False, comment='学院')
    major = Column(String(100), nullable=False, comment='专业')
    class_name = Column(String(50), nullable=False, comment='班级')
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建账户时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    enabled = Column(TINYINT(1), nullable=False, server_default=text("1"))
    type = Column(TINYINT, nullable=False, server_default=text("1"), comment='用户类型')

    @staticmethod
    def get_user_info(id):
        """
        通过ID获取用户信息
        :param id:
        :return:
        """
        user = UserModel.query.filter(UserModel.id == id).first()
        if user:
            return {
                "id": user.id,
                "type": user.type,
                "username": user.username,
                "name": user.name,
                "school": user.school,
                "college": user.college,
                "major": user.major,
                "class_name": user.class_name,
                "enabled": user.enabled
            }
        else:
            return {}

    @staticmethod
    def authenticate(username, password):
        """
        登录验证
        :param username: 用户名
        :param password: 密码
        :return:
        """
        # 用户是否存在
        flag_user_exist = True
        # 密码是否正确
        flag_password_correct = True

        user = UserModel.query.filter(UserModel.username == username).first()

        if user and user.enabled:
            if not sha3.check_hash(password, user.password):
                flag_password_correct = False
        else:
            flag_user_exist = False

        return flag_user_exist, flag_password_correct, user

    @staticmethod
    def update_password(id, old_password, new_password):
        """
        更新密码
        :param id: 用户 ID
        :param old_password: 旧的密码
        :param new_password: 新的密码
        :return: boolean 是否修改成功
        """
        user = UserModel.query.filter(UserModel.id == id).first()

        # 更新密码
        if user and sha3.check_hash(old_password, user.password):
            user.password = sha3.get_hash(new_password)
            db.session.commit()
            return True
        else:
            return False


class StatisticsModel(db.Model):
    __tablename__ = 'statistic'
    id = db.Column(db.Integer, primary_key=True)
    info_time = db.Column(db.Integer, nullable=False, info='采集时间')
    seat = db.Column(db.Integer, nullable=False, info='总座位数')
    reserve = db.Column(db.Integer, nullable=False, info='预约数量')
    inseat = db.Column(db.Integer, nullable=False, info='在座数')
    leave = db.Column(db.Integer, nullable=False, info='暂时离开人数')

    @staticmethod
    def add_data(info_time, seat, reserve, inseat, leave):
        """
        存储统计数据
        :param info_time:
        :param seat:
        :param reserve:
        :param inseat:
        :param leave:
        :return:
        """
        db.session.add(StatisticsModel(info_time=info_time, seat=seat, reserve=reserve, inseat=inseat, leave=leave))
        db.session.commit()

    @staticmethod
    def get_data_now():
        """
        获取当前的统计数据
        :return:
        """
        # stat = {
        #     "seat": "当前座位总数",
        #     "reserve": "当前预约数",
        #     "inseat": "当前在座数",
        #     "leave": "当前暂离数"
        # }
        seat = len(SeatModel.query.filter(SeatModel.enabled == 1).all())
        reserve = len(ReservationModel.query.filter(ReservationModel.status == 1).all())
        inseat = len(ReservationModel.query.filter(ReservationModel.status == 3).all())
        leave = len(ReservationModel.query.filter(ReservationModel.status == 5).all())
        stat = [{
            "status": "seat",
            "value": seat - leave - inseat,
            "title": "当前空座位数"
        }, {
            "status": "reserve",
            "value": reserve,
            "title": "当前预约数"
        }, {
            "status": "inseat",
            "value": inseat,
            "title": "当前在座数"
        }, {
            "status": "leave",
            "value": leave,
            "title": "当前暂离数"
        }]
        return stat
        # return {"info_time": int(time.time()), "seat": len(SeatModel.query.filter(SeatModel.enabled == 1).all()),
        #         "reserve": len(ReservationModel.query.filter(ReservationModel.status == 1).all()),
        #         "inseat": len(ReservationModel.query.filter(ReservationModel.status == 3).all()),
        #         "leave": len(ReservationModel.query.filter(ReservationModel.status == 5).all())}

    @staticmethod
    def get_data_by_time(info_time):
        """
        获取指定时间的信息
        :param info_time:
        :return:
        """
        info = StatisticsModel.query.filter(StatisticsModel.info_time > info_time - 30,
                                            StatisticsModel.info_time < info_time + 30).all()
        if not len(info):
            return {'reserve': 0, 'id': 0, 'leave': 0, 'seat': 0, 'inseat': 0, 'info_time': info_time}
        return _x(info)[0]

    @staticmethod
    def get_inseat_data_by_times(limit):
        """
        获取最近几次的在座数据
        :param limit:
        :return:
        """
        info = StatisticsModel.query.order_by(StatisticsModel.info_time.desc()).limit(limit).all()
        return _x(info)

    @staticmethod
    def get_data_by_day(date):
        # Fixme: 获取今天的统计信息
        #  1. 如何排除重复的?
        today = datetime.datetime.strptime(date, "%Y-%m-%d")
        tomorrow = today + td
        StatisticsModel.query.filter(StatisticsModel.info_time >= int(today.timestamp()),
                                     StatisticsModel.info_time < int(tomorrow.timestamp())).all()


if __name__ == '__main__':
    pass
