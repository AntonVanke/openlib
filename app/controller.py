import datetime

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from .models import UserModel, ReservationModel, RoomModel, SeatModel, OptionModel
from . import jwt


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def invalid_token_callback(*args, **kwargs):
    return jsonify({
        'code': 201,
        'message': "Invalid token",
        'data': None
    }), 403


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
            message = "Nonexistent user"
        elif not flag_password_correct:
            code = 202
            message = "Wrong password"
        else:
            code = 200
            message = "success"
            data = {
                "token": create_access_token(identity=user.id)
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
        message = "success"
        data = UserModel.get_user_info(get_jwt_identity())
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
        message = "success"
        data = None

        args = reqparse.RequestParser() \
            .add_argument('old_password', type=str, location='json', required=True, help="旧密码不能为空") \
            .add_argument('new_password', type=str, location='json', required=True, help="新密码不能为空") \
            .parse_args()
        # 判断新密码是否达到指定长度
        if len(args["new_password"]) < 8:
            code = 201
            message = "Irregular new password"
        elif not UserModel.update_password(get_jwt_identity(), args["old_password"], args["new_password"]):
            code = 202
            message = "Invalid old password"

        return {
            "code": code,
            "message": message,
            "data": data
        }


class Reserve(Resource):
    @jwt_required()
    def get(self):
        code = 200
        message = "success"
        data = ReservationModel.get_reservations_by_user_id(user_id=get_jwt_identity())
        return {
            "code": code,
            "message": message,
            "data": data
        }

    @jwt_required()
    def post(self):
        """
        预约座位
        """
        code = 299
        message = "Unknown error"
        data = None

        args = reqparse.RequestParser() \
            .add_argument('seat_id', type=str, location='json', required=True, help="座位号不能为空") \
            .add_argument('start_time', type=str, location='json', required=True, help="开始时间不正确") \
            .add_argument('end_time', type=str, location='json', required=True, help="结束时间不正确") \
            .parse_args()
        user_id = get_jwt_identity()
        seat_id = args["seat_id"]
        start_time = int(args["start_time"])
        end_time = int(args["end_time"])
        # 判断座位是否存在
        if not SeatModel.is_exist(seat_id):
            code = 201
            message = "Nonexistent seat"
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
                        message = "success"
                        data = ReservationModel.get_reservations_by_user_id(user_id)
                if message != "success":
                    code = 202
                    message = "Invalid appointment time"
                    data = available
            else:
                # 不在时间段内， 返回可用时间段
                code = 203
                message = "Illegal time"
                data = available

        return {
            "code": code,
            "message": message,
            "data": data
        }
        # print(seat_id, start_time, end_time)
        # print(SeatModel.is_exist(seat_id))
        # print(SeatModel.get_seat_by_id(seat_id))
        # print(RoomModel.get_rooms())


class Option(Resource):
    @jwt_required()
    def get(self, name=None):
        code = 200
        message = "success"
        data = None

        if not name:
            data = OptionModel.get_options()
        else:
            if OptionModel.is_option_exist(name):
                data = [OptionModel.get_option_by_name(name)]
            else:
                code = 201
                message = f"{name}: This option item does not exist"

        return {
            "code": code,
            "message": message,
            "data": data
        }
