from . import api
from .controller import User, Login, Reserve, Option, Building, Room, Seat, Statistics

# 用户
api.add_resource(User, '/user')
# 登录
api.add_resource(Login, '/login')
# 预约查询及预约
api.add_resource(Reserve, '/reserve', '/reserve/<reservation_id>')
# 设置
api.add_resource(Option, '/option', '/option/<name>')
# 场馆
api.add_resource(Building, '/building', '/building/<building_id>')
# 房间
api.add_resource(Room, '/room', '/room/<room_id>')
# 座位
api.add_resource(Seat, '/seat/<seat_id>')
# 信息
api.add_resource(Statistics, '/info', '/info/<info_time>')
