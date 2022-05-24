import datetime
import time

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from .models import UserModel, ReservationModel, RoomModel, SeatModel, OptionModel, BuildingModel, StatisticsModel, \
    check
from . import jwt, scheduler


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def invalid_token_callback(*args, **kwargs):
    return {
        'code': 301,
        'message': "token 无效",
        'data': None
    }


class Login(Resource):
    def post(self):
        """
        获取 Token
        :return:
        """
        code = None
        message = None
        data = None

        args = reqparse.RequestParser() \
            .add_argument('username', type=str, location='json', required=True, help="用户名不能为空") \
            .add_argument("password", type=str, location='json', required=True, help="密码不能为空") \
            .parse_args()

        flag_user_exist, flag_password_correct, user = UserModel.authenticate(args['username'], args['password'])

        if not flag_user_exist:
            code = 201
            message = "用户不存在"
        elif not flag_password_correct:
            code = 202
            message = "密码错误"
        else:
            code = 200
            message = "成功"
            data = {
                "token": create_access_token(identity={"id": user.id, "type": user.type})
            }

        return jsonify({
            "code": code,
            "message": message,
            "data": data
        })


class User(Resource):
    @jwt_required()
    def get(self):
        """
        获取 用户信息
        :return:
        """
        code = 200
        message = "成功"
        data = UserModel.get_user_info(get_jwt_identity()["id"])
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self):
        """
        修改密码
        :return:
        """
        code = 200
        message = "成功"
        data = None

        args = reqparse.RequestParser() \
            .add_argument('old_password', type=str, location='json', required=True, help="旧密码不能为空") \
            .add_argument('new_password', type=str, location='json', required=True, help="新密码不能为空") \
            .parse_args()
        # 判断新密码是否达到指定长度
        if len(args["new_password"]) < 8:
            code = 201
            message = "无效的密码长度"
        elif not UserModel.update_password(get_jwt_identity()['id'], args["old_password"], args["new_password"]):
            code = 202
            message = "旧密码错误"

        return {
            "code": code,
            "message": message,
            "data": data
        }


class Reserve(Resource):
    @jwt_required()
    def get(self, reservation_id=None):
        code = 200
        message = "成功"
        if reservation_id is None:
            data = ReservationModel.get_reservations_by_user_id(user_id=get_jwt_identity()["id"])
        else:
            data = ReservationModel.get_reservations_by_reservation_id(reservation_id)
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self, reservation_id=None):
        """
        预约座位
        """
        code = 299
        message = "未知错误"
        data = None

        args = reqparse.RequestParser() \
            .add_argument('seat_id', type=str, location='json', required=False, help="座位号不能为空") \
            .add_argument('start_time', type=str, location='json', required=False) \
            .add_argument('end_time', type=str, location='json', required=False) \
            .add_argument('_method', type=str, location='json', required=False) \
            .parse_args()

        if str(args["_method"]).lower() == "delete":
            # 如果是取消预约
            return self.delete(reservation_id)

        if args["start_time"] is None or args["end_time"] is None:
            return {
                "code": 202,
                "message": "`start_time` 或 `end_time`: 请求字段不存在",
                "data": None
            }
        seat_id = args["seat_id"]
        user_id = get_jwt_identity()["id"]
        start_time = int(args["start_time"])
        end_time = int(args["end_time"])
        # 判断座位是否存在
        if not SeatModel.is_exist(seat_id):
            code = 201
            message = f"`seat_id:`{seat_id} 不存在的座位"
        elif not SeatModel.is_usable_seat(seat_id):
            code = 201
            message = f"`seat_id:`{seat_id} 不存在的座位"
        else:
            # 判断时间是否在正确的间隔
            now = int(datetime.datetime.now().timestamp())
            available = ReservationModel.get_time_slot_by_seat_id(seat_id)
            if now <= start_time < end_time:
                for td in available:
                    if td[0] <= start_time and td[1] >= end_time:
                        ReservationModel.add_reservation(user_id, seat_id, start_time, end_time)
                        # 在可用时间段
                        code = 200
                        message = "成功"
                        data = ReservationModel.get_enabled_reservations_by_user_id(user_id)
                if message != "成功":
                    code = 202
                    message = "预约时间段冲突"
                    data = {"available_time_period": available}
            else:
                # 不在时间段内， 返回可用时间段
                code = 203
                message = "无效的预约时间"
                data = {"available_time_period": available}

        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def delete(self, reservation_id=None):
        """
        取消预约
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if reservation_id is None:
            code = 204
            message = "`reservation_id`: 请求字段不存在"
        else:
            if not ReservationModel.cancel(reservation_id):
                code = 205
                message = "无效的预约"

        return {
            "code": code,
            "message": message,
            "data": data
        }


class Option(Resource):
    def get(self, name=None):
        code = 200
        message = "成功"
        data = None

        if not name:
            data = OptionModel.get_options()
        else:
            if OptionModel.is_option_exist(name):
                data = [OptionModel.get_option_by_name(name)]
            else:
                code = 201
                message = f"{name}: 查询不存在"

        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self, name=None, args=None):
        """
        修改设置项
        :return:
        """
        return self.put(name, args)

    @jwt_required()
    def put(self, name=None, args=None):
        """
        修改设置项
        :return:
        """
        code = 200
        message = "成功"
        data = None

        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        if name is None:
            return {
                "code": 202,
                "message": "`name`: 请求字段不存在",
                "data": None
            }
        if args is None:
            args = reqparse.RequestParser() \
                .add_argument('value', type=str, location='json', required=False) \
                .parse_args()
        if args["value"] is None:
            return {
                "code": 202,
                "message": "`value`: 请求字段不存在",
                "data": None
            }
        if not OptionModel.update_option(name, args["value"]):
            code = 203
            message = f"{name}: 查询不存在"
        return {
            "code": code,
            "message": message,
            "data": data
        }


class Building(Resource):
    """
    分馆
    """

    def get(self, building_id=0):
        """
        获取建筑信息
        :param building_id:
        :return:
        """
        code = 200
        message = "成功"
        if not building_id:
            data = BuildingModel.get_buildings()
        else:
            data = BuildingModel.get_rooms_by_building(building_id)
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self, building_id=0):
        """
        管理员: 添加或修改建筑信息
        :param building_id:
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        args = reqparse.RequestParser() \
            .add_argument('name', type=str, location='json', required=False) \
            .add_argument('enabled', type=str, location='json', required=False) \
            .add_argument('_method', type=str, location='json', required=False) \
            .parse_args()
        if not building_id:
            # 添加场馆
            if args["name"]:
                enabled = args["enabled"] or 1
                for building in BuildingModel.get_buildings():
                    if building["name"] == args["name"]:
                        code = 203
                        message = f"重复的字段: [name]:`{args['name']}`"
                        return {
                            "code": code,
                            "message": message,
                            "data": data
                        }
                BuildingModel.add_building(BuildingModel(name=args["name"], enabled=enabled))
            else:
                code = 201
                message = f"`name`: 请求字段不存在"
        else:
            if str(args["_method"]).lower() == "delete":
                # 删除一个场馆
                return self.delete(building_id)
            elif str(args["_method"]).lower() == "put":
                # 修改场馆
                return self.put(building_id, args)
            else:
                code = 210
                message = "不明确的请求"

        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def delete(self, building_id=0):
        """
        管理员: 删除场馆
        :param building_id:
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        if not building_id:
            code = 202
            message = "`building_id`: 请求的字段不存在"
        else:
            if not BuildingModel.del_building(building_id):
                code = 209
                message = f"[id]:{building_id}: 查询不存在"
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def put(self, building_id=0, args=None):
        """
        管理员: 修改场馆
        :param building_id:
        :param args:
        :return:
        """
        code = 200
        message = "成功"
        data = None

        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }

        if args is None:
            args = reqparse.RequestParser() \
                .add_argument('name', type=str, location='json', required=False) \
                .add_argument('enabled', type=str, location='json', required=False) \
                .parse_args()

        if not building_id:
            code = 202
            message = f"[id]:{building_id}: 查询不存在"
        else:
            for building in BuildingModel.get_buildings():
                if building["name"] == args["name"]:
                    code = 203
                    message = f"重复的字段: [name]:`{args['name']}`"
                    return {
                        "code": code,
                        "message": message,
                        "data": data
                    }
            BuildingModel.edit_building(building_id, name=args["name"], enabled=args["enabled"])
        return {
            "code": code,
            "message": message,
            "data": data
        }


class Room(Resource):
    """
    房间
    """

    def get(self, room_id=0):
        """
        获取房间信息或房间里的seat
        :param room_id:
        :return:
        """
        code = 200
        message = "成功"
        if not room_id:
            data = RoomModel.get_rooms()
        else:
            data = RoomModel.get_seats_by_room_id(room_id)
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self):
        """
        添加房间
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        args = reqparse.RequestParser() \
            .add_argument('name', type=str, location='json', required=False) \
            .add_argument('enabled', type=str, location='json', required=False) \
            .add_argument('building', type=str, location='json', required=False) \
            .add_argument('_method', type=str, location='json', required=False) \
            .parse_args()
        if args["_method"].lower() == "put":
            self.put()
        elif args["_method"].lower() == "delete":
            return self.delete()

        if args["name"] is None or args["enabled"] is None or args["building"] is None:
            code = 201
            message = f"参数不完整({args['name']},{args['enabled']},{args['building']})"
        elif len(args["name"]) > 20 or len(args["enabled"]) > 1 or len(args["building"]) > 2:
            code = 202
            message = "参数超过限制"
        else:
            RoomModel.add_room(args["name"], args["building"], args["enabled"])
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def put(self):
        """
        修改房间
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        args = reqparse.RequestParser() \
            .add_argument('id', type=str, location='json', required=False) \
            .add_argument('name', type=str, location='json', required=False) \
            .add_argument('enabled', type=str, location='json', required=False) \
            .add_argument('building', type=str, location='json', required=False) \
            .parse_args()
        if args["id"] is None and args["building"] is None and args["enabled"] is None:
            message = f"参数不完整({args['name']},{args['enabled']},{args['building']})"
        if not RoomModel.update_room_by_id(args["id"], args["name"], args["building"], args["enabled"]):
            code = 201
            message = "失败"
            data = RoomModel.get_rooms()
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def delete(self):
        """
        删除房间
        :return:
        """
        code = 200
        message = "成功"
        data = None
        if int(get_jwt_identity()["type"]) != 2:
            # 如果不是管理员退出
            return {
                "code": 302,
                "message": "访问受限",
                "data": None
            }
        args = reqparse.RequestParser() \
            .add_argument('id', type=str, location='json', required=False) \
            .parse_args()
        if not RoomModel.del_room_by_id(room_id=args["id"]):
            code = 201
            message = "失败"
            data = RoomModel.get_rooms()
        return {
            "code": code,
            "message": message,
            "data": data
        }


class Seat(Resource):
    """
    座位
    """

    def get(self, seat_id):
        code = 200
        message = "成功"
        print(SeatModel.is_exist(seat_id), SeatModel.is_usable_seat(seat_id))
        if SeatModel.is_exist(seat_id) and SeatModel.is_usable_seat(seat_id):
            data = SeatModel.get_time_slot_by_seat_id(seat_id)
        else:
            data = None
            code = 201
            message = "无效的座位"
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self):
        pass


class Statistics(Resource):
    """
    统计
    1. 座位数量
    2. 预约数量
    3. 正在进行数量
    4. 暂离数量
    5. 迟到数量
    """

    def get(self, info_time=None):
        check()
        code = 200
        message = "成功"
        if info_time is None:
            data = StatisticsModel.get_data_now()
        elif int(info_time) < 100:
            data = StatisticsModel.get_inseat_data_by_times(int(info_time))
        else:
            data = StatisticsModel.get_data_by_time(int(info_time))
        return {
            "code": code,
            "message": message,
            "data": data
        }


# 定时器
@scheduler.task('cron', id='record', minute="*")
def job1():
    # 信息时间
    info_time = int(time.time())
    # 座位数
    seat = len(SeatModel.query.filter(SeatModel.enabled == 1).all())
    # 预约人数
    reserve = len(ReservationModel.query.filter(ReservationModel.status == 1).all())
    # 在座人数
    inseat = len(ReservationModel.query.filter(ReservationModel.status == 3).all())
    # 暂离人数
    leave = len(ReservationModel.query.filter(ReservationModel.status == 5).all())
    info = (info_time, seat, reserve, inseat, leave)
    StatisticsModel.add_data(*info)


@scheduler.task('cron', id='check', minute="*")
# @scheduler.task('cron', id='check', second="*")
def job2():
    """
    判定关闭和迟到的座位
    :return:
    """
    check()