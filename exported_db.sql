-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: careerpathdb
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `career_fields`
--

DROP TABLE IF EXISTS `career_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `career_fields` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `course_required` varchar(100) DEFAULT NULL,
  `skills_required` text,
  `related_jobs` text,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `career_fields`
--

LOCK TABLES `career_fields` WRITE;
/*!40000 ALTER TABLE `career_fields` DISABLE KEYS */;
INSERT INTO `career_fields` VALUES (1,'Software Engineering','B.Tech','Python, DSA, DBMS, Problem-Solving','Backend Developer, Frontend Developer, Full Stack Developer, Software Engineer','Designing and developing software applications.'),(2,'Data Science','B.Sc / B.Tech','Python, SQL, Machine Learning, Data Visualization','Data Scientist, Data Analyst, AI Engineer','Extracting insights from data using statistical and computational techniques.'),(3,'Mechanical Engineering','B.Tech','AutoCAD, SolidWorks, Thermodynamics, Mechanics','Mechanical Engineer, CAD Designer, Manufacturing Engineer','Design and analysis of mechanical systems and structures.'),(4,'Civil Engineering','B.Tech','AutoCAD, Structural Analysis, Surveying','Civil Engineer, Structural Engineer, Site Supervisor','Planning, designing, and maintaining infrastructure and buildings.'),(5,'Marketing','BBA / MBA','SEO, Digital Marketing, Communication, Market Analysis','Marketing Manager, Brand Strategist, SEO Analyst','Promoting products and services to the right audience.'),(6,'Finance','B.Com / MBA','Excel, Accounting, Financial Modeling, Investment Strategies','Financial Analyst, Investment Banker, Accountant','Managing money, investments, and financial planning.'),(7,'Psychology','B.A / M.A','Empathy, Counseling, Research, Behavioral Analysis','Clinical Psychologist, HR Specialist, Counselor','Study of human behavior and mental processes.'),(8,'Law','LLB / LLM','Critical Thinking, Legal Research, Communication','Lawyer, Legal Advisor, Public Prosecutor','Study and application of legal systems and policies.'),(9,'Architecture','B.Arch','AutoCAD, Creativity, Structural Design','Architect, Urban Planner, Interior Designer','Designing and planning buildings and structures.');
/*!40000 ALTER TABLE `career_fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_history`
--

DROP TABLE IF EXISTS `search_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `query` varchar(255) NOT NULL,
  `searched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `search_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_history`
--

LOCK TABLES `search_history` WRITE;
/*!40000 ALTER TABLE `search_history` DISABLE KEYS */;
INSERT INTO `search_history` VALUES (1,1,'engineer','2025-04-04 14:55:51'),(2,1,'medicine','2025-04-04 14:56:45');
/*!40000 ALTER TABLE `search_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'gugugaga','somyakhera0309@gmail.com','pbkdf2:sha256:1000000$5gSsovi2JN0TWY8t$3f90d15b6720b97e3f64b937aef3cebb5b7f182cdcabd39bade4bab27de062f7');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 12:52:35
