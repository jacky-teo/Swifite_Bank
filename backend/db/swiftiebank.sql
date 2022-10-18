DROP DATABASE IF EXISTS `swiftiebank`;
CREATE DATABASE IF NOT EXISTS `swiftiebank` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `swiftiebank`;

-- customer --
-- Path: backend\db\swiftiebank.sql
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `account_type` varchar(255) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `customers` (`customer_id`, `username`, `password`, `account_type`) VALUES
(1, 'customer1', 'password', 'customer'),
(2, 'customer2', 'password', 'customer'),
(3, 'business1', 'password', 'business');

-- LOANS -- 
-- Path: backend\db\swiftiebank.sql
DROP TABLE IF EXISTS `loans`;
CREATE TABLE `loans` (
  `loan_id` int(11) NOT NULL AUTO_INCREMENT,
  `business_id` int(11) NOT NULL,
  `loan_amount` int(11) NOT NULL,
  `loan_duration` int(11) NOT NULL,
  `loan_start_date` date NOT NULL,
  `loan_interest` int(11) NOT NULL,
  PRIMARY KEY (`loan_id`),
  FOREIGN KEY (`business_id`) REFERENCES `customers`(`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- INERT LOANS --
INSERT INTO `loans` (`loan_id`, `business_id`, `loan_amount`, `loan_duration`, `loan_start_date`, `loan_interest`) VALUES
(1, 3, 10000, 12, '2021-01-01', 5),
(2, 3, 20000, 24, '2021-01-01', 25),
(3, 3, 30000, 36, '2021-01-01', 15),
(4, 3, 30000, 36, '2021-01-01', 35),
(5, 3, 30000, 36, '2021-01-01', 15);

-- Customer_loan --
-- Path: backend\db\swiftiebank.sql
DROP TABLE IF EXISTS `customer_loans`;
CREATE TABLE `customer_loans` (
  `customer_id` int(11) NOT NULL,
  `loan_id` int(11) NOT NULL,
  `customer_loans`Float NOT NULL,
  FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`),
  FOREIGN KEY (`loan_id`) REFERENCES `loans`(`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- INSERT CUSTOMER_LOAN --
INSERT INTO `customer_loans` (`customer_id`, `loan_id`,`customer_loans`) VALUES
(1, 1, 1000),
(2, 1, 1000),
(2, 2, 1000),
(1, 2, 1000);


-- Payments -- 
-- Path: backend\db\swiftiebank.sql
DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `business_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `loan_id` int(11) NOT NULL,
  `payment_amount` int(11) NOT NULL,
  `payment_date` date NOT NULL,
  PRIMARY KEY (`payment_id`),
  FOREIGN KEY (`business_id`) REFERENCES `customers`(`customer_id`),
  FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`),
  FOREIGN KEY (`loan_id`) REFERENCES `loans`(`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `payments` (`payment_id`, `business_id`, `customer_id`, `loan_id`, `payment_amount`, `payment_date`) VALUES
(1, 3, 1, 1, 100, '2021-01-01'),
(2, 3, 1, 1, 100, '2021-02-01');

-- wallets --
-- Path: backend\db\swiftiebank.sql
DROP TABLE IF EXISTS `wallets`;
CREATE TABLE `wallets` (
  `wallet_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `wallet_balance` FLOAT NOT NULL,
  PRIMARY KEY (`wallet_id`),
  FOREIGN KEY (`customer_id`) REFERENCES `customers`(`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `wallets` (`wallet_id`, `customer_id`, `wallet_balance`) VALUES
(1, 1, 10000),
(2, 2, 10000);

