-- ------------------------------------------- Create the Bot Database Schema -------------------------------------------------
CREATE DATABASE bot;
                        
-- ------------------------------------------- Create the Tables / Collections --------------------------------------------------
-- ------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE `bot`.`admins` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) NOT NULL,
  `group` varchar(45) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`message` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `chatid` varchar(45) NOT NULL,
  `date` datetime DEFAULT NULL,
  `type` varchar(45) NOT NULL,
  `first_name` text NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`Owed_Amount` (
  `UserID` varchar(45) NOT NULL,
  `AmountOwed` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`Payment` (
  `PaymentID` int NOT NULL AUTO_INCREMENT,
  `UserID` varchar(45) NOT NULL,
  `AmountCharged` double NOT NULL DEFAULT '0',
  `DateOfPayment` datetime DEFAULT NULL,
  PRIMARY KEY (`PaymentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
