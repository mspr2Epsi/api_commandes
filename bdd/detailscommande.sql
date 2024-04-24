-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 24 avr. 2024 à 14:50
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `mspr2`
--

-- --------------------------------------------------------

--
-- Structure de la table `detailscommande`
--

DROP TABLE IF EXISTS `detailscommande`;
CREATE TABLE IF NOT EXISTS `detailscommande` (
  `DetailID` int NOT NULL AUTO_INCREMENT,
  `CommandeID` int DEFAULT NULL,
  `ProduitID` int DEFAULT NULL,
  `Quantite` int DEFAULT NULL,
  PRIMARY KEY (`DetailID`),
  KEY `fk_detailsCommande_commandes` (`CommandeID`),
  KEY `fk_detailsCommande_produits` (`ProduitID`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `detailscommande`
--

INSERT INTO `detailscommande` (`DetailID`, `CommandeID`, `ProduitID`, `Quantite`) VALUES
(1, 1, 1, 2),
(2, 1, 2, 3),
(3, 2, 3, 1),
(4, 2, 4, 2),
(5, 3, 5, 2),
(6, 3, 6, 1),
(7, 4, 7, 3),
(8, 4, 8, 1),
(9, 5, 9, 4),
(10, 5, 10, 2),
(11, 6, 11, 3),
(12, 6, 12, 2),
(13, 7, 13, 1),
(14, 7, 14, 3),
(15, 8, 15, 2),
(16, 8, 16, 1),
(17, 9, 17, 3),
(18, 9, 18, 2);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
