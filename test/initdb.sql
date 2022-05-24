# Init DataBase v0.1.0 初始化系统数据库
create table if not exists openlib.building
(
    id      int auto_increment
        primary key,
    name    varchar(100)         not null comment '场馆名称',
    enabled tinyint(1) default 1 not null comment '开启',
    constraint building_name_uindex
        unique (name)
);

create table if not exists openlib.`option`
(
    id    int auto_increment
        primary key,
    name  varchar(255) not null comment '配置项',
    value longtext     not null comment '配置值',
    constraint option_name_uindex
        unique (name)
);

create table if not exists openlib.reservation
(
    id          int auto_increment
        primary key,
    user_id     int                                 not null comment '用户ID',
    seat_id     int                                 not null comment '座位ID',
    start_time  int                                 not null comment '预约开始时间',
    end_time    int                                 not null comment '预约结束时间',
    status      int       default 1                 not null comment '状态',
    create_time timestamp default CURRENT_TIMESTAMP not null
);

create table if not exists openlib.room
(
    id          int auto_increment
        primary key,
    building_id int                  not null comment '启用',
    enabled     tinyint(1) default 1 not null comment '启用',
    name        varchar(100)         not null comment '房间名称'
);

create table if not exists openlib.seat
(
    id      int auto_increment
        primary key,
    room_id int                  not null comment '房间ID',
    enabled tinyint(1) default 1 not null comment '启用'
);

create table if not exists openlib.statistic
(
    id        int auto_increment
        primary key,
    info_time int not null comment '采集时间',
    seat      int not null comment '总座位数',
    reserve   int not null comment '预约数量',
    inseat    int not null comment '在座数',
    `leave`   int not null comment '暂时离开人数
'
)
    comment '统计信息';

create table if not exists openlib.user
(
    id          int auto_increment
        primary key,
    username    varchar(40)                          not null comment '学号教工号',
    password    varchar(255)                         not null comment '密码',
    name        varchar(40)                          not null comment '姓名',
    school      varchar(100)                         not null comment '学校',
    college     varchar(100)                         not null comment '学院',
    major       varchar(100)                         not null comment '专业',
    class_name  varchar(50)                          not null comment '班级',
    create_time timestamp  default CURRENT_TIMESTAMP not null comment '创建账户时间',
    update_time timestamp  default CURRENT_TIMESTAMP not null,
    enabled     tinyint(1) default 1                 not null,
    type        tinyint    default 1                 not null comment '用户类型',
    constraint username
        unique (username)
);

/*
设置表
为了系统正常运行必须使用
*/
# 迟到时间 150s
INSERT INTO openlib.`option` (name, value)
VALUES ('time_out', '150');
# 网站名称
INSERT INTO openlib.`option` (name, value)
VALUES ('web_name', '座位预约系统');
# 网站地址
INSERT INTO openlib.`option` (name, value)
VALUES ('web_url', 'http://127.0.0.1:5000/');
# 最大预约时间
INSERT INTO openlib.`option` (name, value)
VALUES ('max_hour', '4');
# 开启预约时间
INSERT INTO openlib.`option` (name, value)
VALUES ('open_time', '6:00');
# 关闭预约时间
INSERT INTO openlib.`option` (name, value)
VALUES ('close_time', '23:50');
# 公告
INSERT INTO openlib.`option` (name, value)
VALUES ('announce', '这里是公告');
