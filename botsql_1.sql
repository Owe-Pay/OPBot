-- ------------------------------------------- Create the Bot Database Schema -------------------------------------------------
CREATE DATABASE bot;
                        
-- ------------------------------------------- Create the Tables / Collections --------------------------------------------------
-- ------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE `bot`.`admins` (
  `UserID` int NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`users` (
  `UserID` int NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  `notifiable` BOOLEAN ,
  `date` DATETIME DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`transactions` (
	`transaction_id` INT NOT NULL AUTO_INCREMENT,
    `OrderID` INT NOT NULL,
    `date` DATETIME DEFAULT NULL,
    `AmountOwed` DOUBLE NOT NULL DEFAULT '0',
    `UserID_Creditor` INT NOT NULL,
    `UserID_Debitor` INT NOT NULL,
    PRIMARY KEY (`transaction_id`)
)  ENGINE=INNODB AUTO_INCREMENT=797 DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;

CREATE TABLE `bot`.`Orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `GroupID` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bot`.`Groups` (
  `GroupID` varchar(45) NOT NULL,
  `Number_of_members` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`GroupID`)
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
