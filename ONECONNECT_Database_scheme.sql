-- MySQL dump 10.13  Distrib 8.0.14, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: chatbot
-- ------------------------------------------------------
-- Server version	8.0.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `analysis`
--

DROP TABLE IF EXISTS `analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `analysis` (
  `analysis_id` int(11) NOT NULL AUTO_INCREMENT,
  `analysis_user_input` varchar(100) DEFAULT NULL,
  `analysis_timestamp` datetime NOT NULL,
  `faq_id` int(11) NOT NULL,
  PRIMARY KEY (`analysis_id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analysis`
--

LOCK TABLES `analysis` WRITE;
/*!40000 ALTER TABLE `analysis` DISABLE KEYS */;
INSERT INTO `analysis` VALUES (1,'How old are you?','2019-03-12 11:54:58',4),(2,'How old are you?','2019-03-12 11:54:58',4),(3,'Where is Oneconnect?','2019-03-12 13:35:18',-1),(4,'How old are you?','2019-03-12 13:38:30',4),(5,'Where is OneConnect?','2019-03-12 15:39:05',-1),(6,'Hello?','2019-03-12 15:39:22',-1),(7,'Where is OneConnect?','2019-03-12 15:45:50',-1),(8,'Where is ONECONNECT?','2019-03-13 15:21:21',-1),(9,'Where is ONECONNECT?','2019-03-13 15:25:25',-1),(10,'Where is ONECONNECT?','2019-03-13 15:42:11',-1),(11,'Hello','2019-03-13 15:42:55',-1),(12,'Guess what is my current mood?','2019-03-13 15:43:18',11),(13,'Guess what is my current mood?','2019-03-22 11:04:22',11),(14,'sad','2019-03-22 11:04:29',13),(15,'what is the number of employees in oneconnect singapore?','2019-03-22 11:29:45',6),(16,'what is the number of employees in oneconnect China?','2019-03-22 11:30:26',5),(17,'what is the number of employees?','2019-03-22 11:36:13',5),(18,'Guess what is my current mood?','2019-03-22 11:57:18',11),(19,'Guess what is my current mood?','2019-03-22 11:57:57',11),(20,'happy','2019-03-22 11:58:00',12),(21,'sad','2019-03-22 11:58:06',13),(22,'sad','2019-03-22 11:58:10',13),(23,'sad','2019-03-22 11:58:13',13),(24,'Guess what is my current mood?','2019-03-22 12:04:16',11),(25,'sad','2019-03-22 12:04:17',13),(26,'Guess what is my current mood?','2019-03-22 12:04:55',11),(27,'sad','2019-03-22 12:04:58',13),(28,'Guess what is my current mood?','2019-03-22 12:08:30',11),(29,'sad','2019-03-22 12:08:32',13),(30,'Hello, chatbot','2019-03-27 15:56:10',8),(31,'Hello,chatbot','2019-03-27 15:56:39',8),(32,'Guess what is my current mood?','2019-03-27 15:57:27',11),(33,'Hello','2019-03-27 16:04:21',-1),(34,'Hello, Chatbot','2019-03-27 16:04:30',8),(35,'How are you?','2019-04-02 11:14:52',-1),(36,'What the hell?','2019-04-02 11:15:04',-1),(37,'Hello?','2019-04-02 11:15:14',-1),(38,'Excuse me?','2019-04-02 11:15:20',-1),(39,'Hello, Chatbot','2019-04-02 11:15:34',8),(40,'Guess what is my current mood?','2019-04-02 11:17:55',11),(41,'I love rirakkuma','2019-04-02 11:24:36',-1),(42,'I want Rilakkuma!','2019-04-02 11:24:58',9),(43,'I want rirakkuma','2019-04-02 11:28:55',-1),(44,'I want Rilakkuma!','2019-04-02 11:29:27',9),(45,'Hello','2019-04-02 12:00:37',-1),(46,'Hello','2019-04-02 13:56:48',-1),(47,'Hello, chatbot','2019-04-02 13:56:53',8),(48,'Hello','2019-04-02 14:03:45',-1),(49,'Guess what is my current mood?','2019-04-02 14:03:56',11),(50,'happy','2019-04-02 14:03:59',12),(51,'sad','2019-04-02 14:04:00',13),(52,'How are you?','2019-04-02 14:16:07',-1),(53,'I want rilakkuma!','2019-04-02 14:16:30',9),(54,'I want Rilakkuma!','2019-04-02 14:16:53',9),(55,'hello','2019-04-02 14:31:19',-1),(56,'Hello','2019-04-08 22:29:06',-1),(57,'What\'s your name?','2019-04-08 22:29:17',2),(58,'Where is ONECONNECT?','2019-04-08 22:29:41',1),(59,'Hello','2019-04-09 10:16:09',-1),(60,'Hello','2019-04-09 10:17:01',-1),(61,'Hello?','2019-04-09 10:17:18',-1),(62,'Hello','2019-04-09 10:23:49',-1),(63,'What is the building?','2019-04-09 10:24:01',2),(64,'Guess what is my current mood?','2019-04-09 10:24:17',11),(65,'happy','2019-04-09 10:24:24',12),(66,'sad','2019-04-09 10:24:27',13);
/*!40000 ALTER TABLE `analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `faq` (
  `faq_id` int(11) NOT NULL AUTO_INCREMENT,
  `faq_question` varchar(100) DEFAULT NULL,
  `faq_answer` varchar(100) DEFAULT NULL,
  `faq_type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`faq_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq`
--

LOCK TABLES `faq` WRITE;
/*!40000 ALTER TABLE `faq` DISABLE KEYS */;
INSERT INTO `faq` VALUES (1,'Where is ONECONNECT ?','20 Pasir Panjang Road #01-25 Singapore 117439','1'),(2,'What is the building name?','mapletree business city','1'),(3,'What is OneConnect\'s business?','FinTech','1'),(4,'How old is OneConnect?','3 years old','1'),(6,'How many employees are there in OneConnect Singapore?','Over 100 people','1'),(7,'How much does Ping An invest on OneConnect?','US$7.5 Billion','1'),(8,'Hello, chatbot!','http://m.plonga.com/uploads/thumbs/tropical-minion-delivery-html5-game.jpg','2'),(9,'I want Rilakkuma!','./assets/images/rilakkuma.gif','2'),(11,'Guess what is my current mood?','happy,sad','3'),(12,'Happy','Enjoy your day~','1'),(13,'Sad','Cheer up~','1');
/*!40000 ALTER TABLE `faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faq_category`
--

DROP TABLE IF EXISTS `faq_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `faq_category` (
  `faq_category_id` int(11) NOT NULL AUTO_INCREMENT,
  `faq_category_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`faq_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq_category`
--

LOCK TABLES `faq_category` WRITE;
/*!40000 ALTER TABLE `faq_category` DISABLE KEYS */;
INSERT INTO `faq_category` VALUES (1,'text'),(2,'image'),(3,'buttons');
/*!40000 ALTER TABLE `faq_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `user_password` varchar(200) NOT NULL,
  `user_first_name` varchar(45) NOT NULL,
  `user_last_name` varchar(45) NOT NULL,
  `user_email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','sha256$rafDWogy$19fb384a7468b508b2d77ca62dceac65d3b726d234634c2a1ed1ff09d37dc992','Peter','LU','peterlu@pingan.com');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'chatbot'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-09 11:37:37
