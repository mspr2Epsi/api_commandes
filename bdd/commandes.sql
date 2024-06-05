-- Drop existing tables if they exist
DROP TABLE IF EXISTS `detailscommande`;
DROP TABLE IF EXISTS `commandes`;

-- Create the `commandes` table
CREATE TABLE IF NOT EXISTS `commandes` (
  `CommandeID` int NOT NULL AUTO_INCREMENT,
  `ClientID` int DEFAULT NULL,
  `DateCommande` datetime DEFAULT NULL,
  `Statut` varchar(255) DEFAULT NULL,
  `PrixTotal` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`CommandeID`),
  KEY `fk_commandes_clients` (`ClientID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert data into the `commandes` table
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

-- Create the `detailscommande` table
CREATE TABLE IF NOT EXISTS `detailsCommande` (
  `DetailID` int NOT NULL AUTO_INCREMENT,
  `CommandeID` int DEFAULT NULL,
  `ProduitID` int DEFAULT NULL,
  `Quantite` int DEFAULT NULL,
  PRIMARY KEY (`DetailID`),
  KEY `fk_detailsCommande_commandes` (`CommandeID`),
  KEY `fk_detailsCommande_produits` (`ProduitID`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert data into the `detailscommande` table
INSERT INTO `detailsCommande` (`DetailID`, `CommandeID`, `ProduitID`, `Quantite`) VALUES
(1, 1, 1, 2),
(2, 1, 2, 3),
(3, 9, 8, 12),
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

-- Commit the transaction
COMMIT;
