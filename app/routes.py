from . import api
from .controller import User, Login, Reserve, Option

# 用户
api.add_resource(User, '/user')
# 登录
api.add_resource(Login, '/login')
# 预约查询及预约
api.add_resource(Reserve, '/reserve')
# 设置
api.add_resource(Option, '/option', '/option/<name>')
