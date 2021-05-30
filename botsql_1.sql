 -- ------------------------------------------- Create the Tables / Collections --------------------------------------------------
-- ------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE `users` (
  `UserID` varchar(45) NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  `notifiable` BOOLEAN ,
  `date` DATETIME DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `admins` (
  `UserID` varchar(45) NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `transactions` (
	`transaction_id` INT NOT NULL AUTO_INCREMENT,
    `OrderID` varchar(45) NOT NULL,
    `date` DATETIME DEFAULT NULL,
    `AmountOwed` DOUBLE NOT NULL DEFAULT '0',
    `UserID_Creditor` varchar(45) NOT NULL,
    `UserID_Debitor` varchar(45) NOT NULL,
    PRIMARY KEY (`transaction_id`)
)  ENGINE=INNODB AUTO_INCREMENT=797 DEFAULT CHARSET=UTF8MB4 COLLATE = utf8mb4_general_ci;

CREATE TABLE `Orders` (
  `OrderID` varchar(45) NOT NULL AUTO_INCREMENT,
  `GroupID` varchar(45) NOT NULL DEFAULT '0',
  PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Groups` (
  `GroupID` varchar(45) NOT NULL,
  `Number_of_members` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`GroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Owed_Amount` (
  `UserID` varchar(45) NOT NULL,
  `AmountOwed` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE admins`Payment` (
  `PaymentID` int NOT NULL AUTO_INCREMENT,
  `UserID` varchar(45) NOT NULL,
  `AmountCharged` double NOT NULL DEFAULT '0',
  `DateOfPayment` datetime DEFAULT NULL,
  PRIMARY KEY (`PaymentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
