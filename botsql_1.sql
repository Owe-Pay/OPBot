
 
 -- ------------------------------------------- Create the Tables / Collections --------------------------------------------------
-- ------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE `Users` (
  `UserID` varchar(45) NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  `FirstName` varchar(45) NOT NULL,
  `notifiable` BOOLEAN ,
  `date` DATETIME DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Admins` (
  `UserID` varchar(45) NOT NULL ,
  `UserName` varchar(45) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Transactions` (
	`transaction_id` varchar(45) NOT NULL,
    `OrderID` varchar(45) NOT NULL,
    `date` DATETIME DEFAULT NULL,
    `AmountOwed` DOUBLE NOT NULL DEFAULT '0',
    `UserID_Creditor` varchar(45) NOT NULL,
    `UserID_Debtor` varchar(45) NOT NULL,
    `settled` BOOLEAN NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`transaction_id`)
)  ENGINE=INNODB AUTO_INCREMENT=797 DEFAULT CHARSET=UTF8MB4 COLLATE = utf8mb4_general_ci;

CREATE TABLE `Orders` (
  `OrderID` varchar(45) NOT NULL,
  `UserID` varchar(45) NOT NULL,
  `GroupID` varchar(45) NOT NULL,
  `Order_name` varchar(150) NOT NULL,
  `Order_amount` double NOT NULL DEFAULT '0',
  `MessageID` varchar(45),
  PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `TelegramGroups` (
  `GroupID` varchar(45) NOT NULL,
  `GroupName` varchar(45) NOT NULL,
  `Number_of_members` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`GroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `OwedAmount` (
  `UserID` varchar(45) NOT NULL,
  `AmountOwed` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `Payment` (
  `PaymentID` varchar(45) NOT NULL,
  `UserID` varchar(45) NOT NULL,
  `AmountCharged` double NOT NULL DEFAULT '0',
  `DateOfPayment` datetime DEFAULT NULL,
  PRIMARY KEY (`PaymentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `UserGroupRelational` (
	  `UserID` varchar(45) NOT NULL,
    `GroupID` varchar(45) NOT NULL,
    `Temp_Amount` double NOT NULL DEFAULT '0',
	  `State` varchar(45) NOT NULL DEFAULT 'inactive',
    `Temp_OrderID` varchar(45),
    PRIMARY KEY (`UserID`, `GroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;