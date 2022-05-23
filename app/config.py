import os

# 数据库
HOSTNAME = "localhost"
PORT = "3306"
DATABASE = "openlib"
USERNAME = "root"
PASSWORD = "11111111a"


class Config:
    # 定时器
    SCHEDULER_API_ENABLED = True

    # 调试
    DEBUG = os.environ.get('FLASK_DEBUG') or True

    # 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    # print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 安全控制
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "123"
    # print(JWT_SECRET_KEY)
    # JWT_COOKIE_CSRF_PROTECT = True
    # JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 7200
    PROPAGATE_EXCEPTIONS = True
