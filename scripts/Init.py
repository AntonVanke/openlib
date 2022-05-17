from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, func, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

HOSTNAME = "localhost"
PORT = "3306"
DATABASE = "openlib"
USERNAME = "root"
PASSWORD = "11111111a"
app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
db = SQLAlchemy(app)

Base = declarative_base()
metadata = Base.metadata


class Building(db.Model):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, comment='场馆名称')
    # open_time = Column(Integer, nullable=False, server_default=text("'0'"), comment='开启时间')
    # close_time = Column(Integer, nullable=False, server_default=text("'1440'"), comment='结束时间')
    # max_hour = Column(Integer, nullable=False, server_default=text("'0'"), comment='最大预约时间')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='开启')


class Option(db.Model):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment='配置项')
    value = Column(LONGTEXT, nullable=False, comment='配置值')


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    seat_id = Column(Integer, ForeignKey('seat.id'), nullable=False, comment='座位ID')
    start_time = Column(Integer, nullable=False, comment='预约开始时间')
    end_time = Column(Integer, nullable=False, comment='预约结束时间')
    cancelled = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='取消')
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='预约创建时间')


class Room(db.Model):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('building.id'), nullable=False, comment='启用')
    name = Column(String(100), nullable=False, comment='房间名称')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='启用')


class Seat(db.Model):
    __tablename__ = 'seat'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, comment='房间ID')
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='启用')


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True, comment='学号教工号')
    password = Column(String(255), nullable=False, comment='密码')
    name = Column(String(40), nullable=False, comment='姓名')
    school = Column(String(100), nullable=False, comment='学校')
    college = Column(String(100), nullable=False, comment='学院')
    major = Column(String(100), nullable=False, comment='专业')
    class_name = Column(String(50), nullable=False, comment='班级')
    create_time = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now(), comment='创建账户时间')
    update_time = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    enabled = db.Column(TINYINT(1), nullable=False, server_default=db.text("1"))
    type = Column(TINYINT, nullable=False, server_default=text("1"), comment='用户类型')


if __name__ == '__main__':
    db.create_all()
