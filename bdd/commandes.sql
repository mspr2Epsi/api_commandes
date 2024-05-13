-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 13, 2024 at 01:39 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mspr2`
--

-- --------------------------------------------------------

--
-- Table structure for table `commandes`
--

DROP TABLE IF EXISTS `commandes`;
CREATE TABLE IF NOT EXISTS `commandes` (
  `CommandeID` int NOT NULL AUTO_INCREMENT,
  `ClientID` int DEFAULT NULL,
  `DateCommande` datetime DEFAULT NULL,
  `Statut` varchar(255) DEFAULT NULL,
  `PrixTotal` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`CommandeID`),
  KEY `fk_commandes_clients` (`ClientID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `commandes`
--

INSERT INTO `commandes` (`CommandeID`, `ClientID`, `DateCommande`, `Statut`, `PrixTotal`) VALUES
(1, 6, '2024-06-24 00:00:00', 'En cours new', '50.00'),
(2, 2, '2024-04-24 16:30:37', 'En cours', '0.00'),
(3, 3, '2024-04-24 16:30:37', 'En cours', '0.00'),
(4, 4, '2024-04-24 16:30:37', 'En cours', '0.00'),
(5, 5, '2024-04-24 16:30:37', 'En cours', '0.00'),
(6, 6, '2024-04-24 16:30:37', 'En cours', '0.00'),
(7, 7, '2024-04-24 16:30:37', 'En cours', '0.00'),
(8, 8, '2024-04-24 16:30:37', 'En cours', '0.00'),
(9, 9, '2024-04-24 16:30:37', 'En cours', '0.00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
