-- MySQL dump 10.13  Distrib 8.0.28, for macos11 (x86_64)
--
-- Host: 127.0.0.1    Database: openlib
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `building`
--

DROP TABLE IF EXISTS `building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `building` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '场馆名称',
  `enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '开启',
  PRIMARY KEY (`id`),
  UNIQUE KEY `building_name_uindex` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `building`
--

LOCK TABLES `building` WRITE;
/*!40000 ALTER TABLE `building` DISABLE KEYS */;
INSERT INTO `building` VALUES (10,'南校区第一图书馆',1);
/*!40000 ALTER TABLE `building` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `option`
--

DROP TABLE IF EXISTS `option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `option` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '配置项',
  `value` longtext NOT NULL COMMENT '配置值',
  PRIMARY KEY (`id`),
  UNIQUE KEY `option_name_uindex` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `option`
--

LOCK TABLES `option` WRITE;
/*!40000 ALTER TABLE `option` DISABLE KEYS */;
INSERT INTO `option` VALUES (1,'web_name','座位预约系统'),(2,'web_url','http://127.0.0.1/'),(3,'max_hour','4'),(4,'open_time','6:00'),(5,'close_time','22:00'),(6,'announce','<p>        为了加强图书馆智能化管理水平，维护读者在图书馆平等利用阅览座位的权益，防止抢座、占座和入馆拥挤等不良现象的发生，图书馆采取座位管理系统来规范和维护阅览秩序。以下为管理系统操作流程及规则：<br />\\r\\n        电脑派位采用读者自选和随机派发两种方式，读者可任选一种。<br />\\r\\n        电脑派位时间：7:00 --- 22:30。当晚19:30开放次日座位预约，可在网页、微信、APP预约座位。<br />\\r\\n        每次预约座位时长0.5～4小时，距结束60分钟内，可续座0.5～2小时。<br />\\r\\n        签到时间：必须在预选时间之前30分钟内及预选时间之后15分钟之内到图书馆进行签到（现场选座无需签到）。<br />\\r\\n        “暂时离开”阅览室时，请在触屏机上刷卡，“暂离”时座位保留30分钟。超时视为放弃座位，系统收回。30分钟内返回请在触屏机上刷卡，系统将自动恢复原座位。<br />\\r\\n        如需离开阅览室超过30分钟，请在触屏机上刷卡时选择“结束使用”，原座位重新进入派位。<br />\\r\\n       餐时( 11:00--12:30 ；17:00--18:30)刷卡“暂离”，系统保留90分钟。<br />\\r\\n        如果读者有三次违规操作，系统会自动列入黑名单，取消派位资格7天。以下情况属于违规操作：1）读者离开座位但未释放；2）读者选择“暂离”但未在规定时间内返回并恢复座位；3）读者预约座位却未在规定时间内签到。<br />\\r\\n        触屏机使用说明：在屏幕下方刷卡区刷卡，即可进行预约选座。<br />\\r\\n        手机客户端：请登录http://seatlib.hpu.edu.cn，扫码下载（或者直接扫描二维码下载）。安装后首先设置服务器地址：seatlib.hpu.edu.cn，然后输入学号和密码登陆。<\\/p>');
/*!40000 ALTER TABLE `option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `seat_id` int NOT NULL COMMENT '座位ID',
  `start_time` int NOT NULL COMMENT '预约开始时间',
  `end_time` int NOT NULL COMMENT '预约结束时间',
  `cancelled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '取消',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
INSERT INTO `reservation` VALUES (1,1,1,1652673600,1652677200,1,'2022-05-16 10:11:53'),(13,1,1,1652706000,1652709600,0,'2022-05-16 12:35:14');
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `building_id` int NOT NULL COMMENT '启用',
  `enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '启用',
  `name` varchar(100) NOT NULL COMMENT '房间名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,1,1,'第一阅览厅');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat`
--

DROP TABLE IF EXISTS `seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL COMMENT '房间ID',
  `enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat`
--

LOCK TABLES `seat` WRITE;
/*!40000 ALTER TABLE `seat` DISABLE KEYS */;
INSERT INTO `seat` VALUES (1,1,1),(2,1,0);
/*!40000 ALTER TABLE `seat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(40) NOT NULL COMMENT '学号教工号',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `name` varchar(40) NOT NULL COMMENT '姓名',
  `school` varchar(100) NOT NULL COMMENT '学校',
  `college` varchar(100) NOT NULL COMMENT '学院',
  `major` varchar(100) NOT NULL COMMENT '专业',
  `class_name` varchar(50) NOT NULL COMMENT '班级',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建账户时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `type` tinyint NOT NULL DEFAULT '1' COMMENT '用户类型',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'311809030326','4bdd1624ccc38c6d61f21dd65e82d86efb873cf9806b4fe3b90c467db07b6286:cSTE5khq','冯君奭','河南理工大学','计算机学院','信息管理与信息系统','1803','2022-05-07 03:30:21','2022-05-07 03:30:21',1,1),(2,'10001','224b796f089fed20ca8a844d9fef1698795ccc84e8ec12799817d43ecdc165c4:QUVwkKb3','管理员','河南理工大学','无','无','无','2022-05-17 02:49:35','2022-05-17 02:49:35',1,2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-19 13:12:33
