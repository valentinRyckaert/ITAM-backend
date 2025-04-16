Enter password: 
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.6.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: itamweb
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `DEV_id` int(11) NOT NULL AUTO_INCREMENT,
  `DEV_name` text NOT NULL,
  `DEV_os` text NOT NULL,
  `DG_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`DEV_id`),
  KEY `ix_device_DEV_id` (`DEV_id`),
  KEY `ix_device_DEV_name` (`DEV_name`(768)),
  KEY `ix_device_DEV_os` (`DEV_os`(768)),
  KEY `ix_device_DG_id` (`DG_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`DG_id`) REFERENCES `devicegroup` (`DG_id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES
(1,'TEL-2-002-android','android',1),
(2,'LAP-3-003-fedora','fedora',2),
(3,'LAP-3-003-fedora','fedora',3),
(4,'TEL-5-005-ios','ios',6),
(5,'LAP-6-006-windows','windows',NULL),
(6,'PC-7-007-fedora','fedora',NULL),
(7,'TEL-8-008-android','android',NULL),
(8,'LAP-9-009-ubuntu','ubuntu',NULL),
(9,'PC-1-010-windows','windows',NULL),
(10,'TEL-2-011-ios','ios',NULL),
(11,'LAP-3-012-debian','debian',NULL),
(12,'PC-4-013-ubuntu','ubuntu',NULL),
(13,'TEL-5-014-android','android',NULL),
(14,'LAP-6-015-fedora','fedora',NULL),
(15,'PC-7-016-debian','debian',NULL),
(16,'TEL-8-017-android','android',NULL),
(17,'LAP-9-018-windows','windows',NULL),
(18,'PC-1-019-fedora','fedora',NULL),
(19,'TEL-2-020-android','android',NULL),
(20,'LAP-3-021-ubuntu','ubuntu',NULL),
(21,'PC-4-022-windows','windows',NULL),
(22,'TEL-5-023-android','android',NULL),
(23,'LAP-6-024-debian','debian',NULL),
(24,'PC-7-025-ubuntu','ubuntu',NULL),
(25,'TEL-8-026-ios','ios',NULL),
(26,'LAP-9-027-fedora','fedora',NULL),
(27,'PC-1-028-debian','debian',NULL),
(28,'TEL-2-029-android','android',NULL),
(29,'LAP-3-030-windows','windows',NULL),
(30,'PC-4-031-fedora','fedora',NULL),
(31,'TEL-5-032-android','android',NULL),
(32,'LAP-6-033-ubuntu','ubuntu',NULL),
(33,'PC-7-034-windows','windows',NULL),
(34,'TEL-8-035-ios','ios',NULL),
(35,'LAP-9-036-debian','debian',NULL),
(37,'PC-1-001-windows','windows',NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicegroup`
--

DROP TABLE IF EXISTS `devicegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicegroup` (
  `DG_id` int(11) NOT NULL AUTO_INCREMENT,
  `DG_libelle` text NOT NULL,
  PRIMARY KEY (`DG_id`),
  KEY `ix_devicegroup_DG_libelle` (`DG_libelle`(768)),
  KEY `ix_devicegroup_DG_id` (`DG_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicegroup`
--

LOCK TABLES `devicegroup` WRITE;
/*!40000 ALTER TABLE `devicegroup` DISABLE KEYS */;
INSERT INTO `devicegroup` VALUES
(1,'Groupe Zone 1'),
(2,'Groupe Zone 2'),
(3,'Groupe Zone 3'),
(4,'Groupe Zone 4'),
(5,'Groupe Zone 5'),
(6,'Groupe Zone 6'),
(7,'Groupe Zone 7'),
(8,'Groupe Zone 8'),
(9,'Groupe Zone 9'),
(10,'string'),
(11,'string'),
(12,'string'),
(13,'string'),
(14,'string'),
(15,'string'),
(16,'string');
/*!40000 ALTER TABLE `devicegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package`
--

DROP TABLE IF EXISTS `package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package` (
  `PACK_id` int(11) NOT NULL AUTO_INCREMENT,
  `PACK_name` text NOT NULL,
  `PACK_type` text NOT NULL,
  `PACK_os_supported` text NOT NULL,
  `DEV_id` int(11) DEFAULT NULL,
  `DG_id` int(11) DEFAULT NULL,
  `PG_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`PACK_id`),
  KEY `ix_package_PACK_os_supported` (`PACK_os_supported`(768)),
  KEY `ix_package_PACK_name` (`PACK_name`(768)),
  KEY `ix_package_PG_id` (`PG_id`),
  KEY `ix_package_PACK_type` (`PACK_type`(768)),
  KEY `ix_package_PACK_id` (`PACK_id`),
  KEY `ix_package_DG_id` (`DG_id`),
  KEY `ix_package_DEV_id` (`DEV_id`),
  CONSTRAINT `package_ibfk_1` FOREIGN KEY (`DEV_id`) REFERENCES `device` (`DEV_id`),
  CONSTRAINT `package_ibfk_2` FOREIGN KEY (`DG_id`) REFERENCES `devicegroup` (`DG_id`),
  CONSTRAINT `package_ibfk_3` FOREIGN KEY (`PG_id`) REFERENCES `packagegroup` (`PG_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package`
--

LOCK TABLES `package` WRITE;
/*!40000 ALTER TABLE `package` DISABLE KEYS */;
INSERT INTO `package` VALUES
(35,'c_svelte','.pdf','any',NULL,NULL,NULL),
(36,'ddd','.odt','any',NULL,NULL,NULL),
(37,'PPE-TODO','.txt','any',NULL,NULL,NULL);
/*!40000 ALTER TABLE `package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packagegroup`
--

DROP TABLE IF EXISTS `packagegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packagegroup` (
  `PG_id` int(11) NOT NULL AUTO_INCREMENT,
  `PG_libelle` text NOT NULL,
  PRIMARY KEY (`PG_id`),
  KEY `ix_packagegroup_PG_id` (`PG_id`),
  KEY `ix_packagegroup_PG_libelle` (`PG_libelle`(768))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packagegroup`
--

LOCK TABLES `packagegroup` WRITE;
/*!40000 ALTER TABLE `packagegroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `packagegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `USER_id` int(11) NOT NULL AUTO_INCREMENT,
  `USER_username` text NOT NULL,
  `USER_passHash` text NOT NULL,
  `USER_type` int(11) NOT NULL,
  `USER_isActive` tinyint(1) NOT NULL,
  PRIMARY KEY (`USER_id`),
  KEY `ix_user_USER_passHash` (`USER_passHash`(768)),
  KEY `ix_user_USER_username` (`USER_username`(768)),
  KEY `ix_user_USER_isActive` (`USER_isActive`),
  KEY `ix_user_USER_type` (`USER_type`),
  KEY `ix_user_USER_id` (`USER_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,'admin','$2b$12$/GVZxPEYmhCT3MpY/uS8R.l3dXhpA5fBqzUIa9lESLMXgoVs6s2J2',0,1),
(2,'user-1','',1,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-16 15:50:29
