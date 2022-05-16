import time
import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, func
from sqlalchemy.dialects.mysql import TINYINT

from . import db, sha3


def _x(data):
    """
    将多个数据格式化
    :param data:
    :return:
    """
    new_data = []
    for _ in data:
        d = _.__dict__
        d.pop("_sa_instance_state")
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
        if td[0] <= time_d[0] or td[1] >= time_d[-1]:
            continue
        time_d.insert(-1, td[0])
        time_d.insert(-1, td[1])

    # 返回可用时间段
    print(time_d)
    return list(zip(*[iter(time_d)] * 2))


class BuildingModel(db.Model):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='场馆名称')
    # open_time = Column(Integer, nullable=False, server_default=text("'0'"), comment='开启时间')
    # close_time = Column(Integer, nullable=False, server_default=text("'1440'"), comment='结束时间')
    # max_hour = Column(TINYINT, nullable=False, server_default=text("'0'"), comment='最大预约时间')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='开启')

    def get_buildings(self):
        building = BuildingModel.query.all()
        return _x(building)


class OptionModel(db.Model):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment='配置项')
    value = Column(String(255), nullable=False, comment='配置值')

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


class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='用户ID')
    seat_id = Column(Integer, nullable=False, comment='座位ID')
    start_time = Column(Integer, nullable=False, comment='预约开始时间')
    end_time = Column(Integer, nullable=False, comment='预约结束时间')
    cancelled = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='取消')

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        获取用户所有预约
        :param user_id:
        :return:
        """
        reservations = ReservationModel.query.filter(ReservationModel.user_id == user_id).all()
        return _x(reservations)

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
            if res[_r]["cancelled"]:
                res.pop(_r)
        return res

    @staticmethod
    def get_time_slot_by_seat_id(seat_id):
        """
        获取座位的有效预约时间段
        :return:
        """
        # TODO
        reservations = ReservationModel.query.filter(ReservationModel.seat_id == seat_id).all()
        # print(reservations)
        times = []
        for _r in reservations:
            if not _r.cancelled:
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


class RoomModel(db.Model):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='房间名称')
    building_id = Column(Integer, nullable=False, comment='启用')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='启用')

    @staticmethod
    def get_rooms():
        rooms = RoomModel.query.all()
        return _x(rooms)

    @staticmethod
    def get_rooms_by_building_id(building_id):
        rooms = RoomModel.query.filter(RoomModel.building_id == building_id).all()
        return _x(rooms)

    @staticmethod
    def get_room_by_id(id):
        room = RoomModel.query.filter(RoomModel.id == id).all()
        return _x(room)[0]


class SeatModel(db.Model):
    __tablename__ = 'seat'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, nullable=False, comment='房间ID')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='启用')

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


if __name__ == '__main__':
    print(ReservationModel.get_reservations_by_user_id(1))
