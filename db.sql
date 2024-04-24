/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - track&go
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`track&go` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `track&go`;

/*Table structure for table `contact` */

DROP TABLE IF EXISTS `contact`;

CREATE TABLE `contact` (
  `id` int(255) NOT NULL auto_increment,
  `username` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `subject` varchar(500) default NULL,
  `message` longtext,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `contact` */

insert  into `contact`(`id`,`username`,`email`,`subject`,`message`) values (1,'kalpesh','yash@gmail.com','sasda','None'),(2,'kalpesh','yash@gmail.com','sasda','dsgsd');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `Id` int(255) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `Contact` varchar(255) default NULL,
  `Address` varchar(255) default NULL,
  `subject` longtext,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`Id`,`name`,`email`,`Contact`,`Address`,`subject`) values (1,'kalpesh','sujay@gmail.com','45645656','mumbail','20 Best Location Tracking Apps for Accurate GPS Location');

/*Table structure for table `register` */

DROP TABLE IF EXISTS `register`;

CREATE TABLE `register` (
  `Id` int(255) NOT NULL auto_increment,
  `Username` varchar(255) default NULL,
  `Email` varchar(255) default NULL,
  `Contact` varchar(255) default NULL,
  `Password` varchar(255) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `register` */

insert  into `register`(`Id`,`Username`,`Email`,`Contact`,`Password`) values (6,'roshan','roshu@gmail.com','655564656565','a'),(7,'roshan','roshu@gmail.com','655564656565','a');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
