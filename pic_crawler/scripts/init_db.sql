-- ** encoding UTF-8 **
-- --------------------------------------------------
-- File:	init_db.sql
-- Author:	DORSEy Q F TANG
-- Date:	16th Jan 2017
-- Description:	used to initialize the DB for image scrapy
-- --------------------------------------------------

DROP DATABASE IF EXISTS `CRAWLED_PICS`;
CREATE DATABASE IF NOT EXISTS `CRAWLED_PICS`;
USE `CRAWLED_PICS`;

-- ---------------------------------
-- create table domains to crawl images
-- ---------------------------------
DROP TABLE IF EXISTS `PIC_DOMAINS`;
CREATE TABLE `PIC_DOMAINS` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`DOMAIN` VARCHAR(128) NOT NULL COMMENT 'the domain from which the images will be crawled',
	`ABBREVIATION` VARCHAR(25) NOT NULL COMMENT 'the abbreviation for the domain',
	`RULE_4_NAVI_IMG` VARCHAR(128) NOT NULL COMMENT 'the rules for navigate to the image you want to crawl',
	`RULE_4_NAVI_2_NEXT_PAGE` VARCHAR(128) COMMENT 'the rule for navigating to the next page for next round',
	`PATTERN_EXTRACT_PAGINATION` VARCHAR(48) COMMENT 'the rule for navigating to the next page for next round',
	`RULE_4_LOCATE_DETAIL_IMG` VARCHAR(128) COMMENT 'the rule for navigating to the detail images for specific image',
	`ENABLE` INT(1) NOT NULL DEFAULT 0 COMMENT 'indicates whether should crawl images from this website, 0 for yes, 1 for no',
	`CREATED_TIME` TIMESTAMP COMMENT 'the created time for this record',
	PRIMARY KEY (`ID`),
	UNIQUE (`DOMAIN`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- ---------------------------------
-- create table categories
-- which defines all categoriesg
-- ---------------------------------
DROP TABLE IF EXISTS `CATEGORIES`;
CREATE TABLE `CATEGORIES` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`CATEGORY` VARCHAR(8) NOT NULL COMMENT 'categories, O for OUTER; T for top, B for bottom, D for dress, E for bag, S for shoes, A for acc; others, not recognized',
	`ABBREVIATION` CHAR NOT NULL COMMENT 'abbreviation for the category',
	PRIMARY KEY (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- ---------------------------------
-- create table pic_categories_2_URL
-- which defines categories/source URL address mapping
-- ---------------------------------
DROP TABLE IF EXISTS `PIC_CATEGORIES_2_URL`;
CREATE TABLE `PIC_CATEGORIES_2_URL` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`URL_ADDR` VARCHAR(128) NOT NULL COMMENT 'URL address from which the specific kind of images will be crawled',
	`CATEGORY_ID` INT NOT NULL COMMENT 'the category ID',
	`DOMAIN_ID` INT NOT NULL COMMENT 'domain ID',
	`CREATED_TIME` TIMESTAMP,
	PRIMARY KEY (`ID`),
	UNIQUE (`URL_ADDR`),
	FOREIGN KEY (`DOMAIN_ID`) REFERENCES `PIC_DOMAINS` (`ID`) ON DELETE CASCADE,
	FOREIGN KEY (`CATEGORY_ID`) REFERENCES `CATEGORIES` (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- ---------------------------------
-- create table for storing all crawled images
-- ---------------------------------
DROP TABLE IF EXISTS `IMAGES`;
CREATE TABLE `IMAGES` (
	`ID` INT(4) NOT NULL AUTO_INCREMENT,
	`NAME` VARCHAR(24) NOT NULL COMMENT 'image name without suffix',
	`FULL_NAME` VARCHAR(24) NOT NULL COMMENT 'image name with suffix',
	`STORE_PATH` VARCHAR(48) NOT NULL COMMENT 'relative path to the storage',
	`CATEGORY_ID` INT NOT NULL COMMENT 'the category ID',
	`DOMAIN_ID` INT NOT NULL COMMENT 'the domain ID',
	`CREATED_TIME` TIMESTAMP,
	PRIMARY KEY (`ID`),
	FOREIGN KEY (`CATEGORY_ID`) REFERENCES `CATEGORIES` (`ID`),
	FOREIGN KEY (`DOMAIN_ID`) REFERENCES `PIC_DOMAINS` (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- ---------------------------------
-- create table for storing all crawled image details
-- ---------------------------------
DROP TABLE IF EXISTS `IMAGE_DETAILS`;
CREATE TABLE `IMAGE_DETAILS` (
	`ID` INT(4) NOT NULL AUTO_INCREMENT,
	`NAME` VARCHAR(24) NOT NULL COMMENT 'image name without suffix',
	`FULL_NAME` VARCHAR(24) NOT NULL COMMENT 'image name with suffix',
	`STORE_PATH` VARCHAR(48) NOT NULL COMMENT 'relative path to the storage',
	`IMG_ID` INT(4) NOT NULL COMMENT 'parent image ID',
	`CREATED_TIME` TIMESTAMP,
	PRIMARY KEY (`ID`),
	FOREIGN KEY (`IMG_ID`) REFERENCES `IMAGES` (`ID`)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

-- ---------------------------------
-- create index
-- ---------------------------------
CREATE INDEX IDX_PIC_DOMAIN_ABBRVT ON `PIC_DOMAINS` (`ABBREVIATION`);
CREATE INDEX IDX_CATEGORY ON `CATEGORIES` (`CATEGORY`);
CREATE INDEX IDX_IMG_NAME ON `IMAGES` (`NAME`);
CREATE INDEX IDX_IMG_DETAIL_NAME ON `IMAGE_DETAILS` (`NAME`);

-- ---------------------------------
-- initialize required data 
-- ---------------------------------
INSERT INTO `CATEGORIES`(`CATEGORY`, `ABBREVIATION`) VALUES('TOP', 'T'), ('BOTTOM', 'B'), ('OUTER', 'O'), ('DRESS', 'D'), ('BAG', 'E'), ('SHOES', 'S'), ('ACC', 'A');
INSERT INTO `PIC_DOMAINS`(`DOMAIN`, `ABBREVIATION`, `RULE_4_NAVI_IMG`, `RULE_4_NAVI_2_NEXT_PAGE`, `PATTERN_EXTRACT_PAGINATION`, `RULE_4_LOCATE_DETAIL_IMG`) VALUES('http://www.roer.co.kr', 'ROER', '//img[@class=\'MS_prod_img_s\']', '//a[@class=\'now\']', 'r\'[pP][aA][gG][eE]=\\d+\'', '//img[contains(@src, \'ro\') and contains(@src, \'page\')]')
