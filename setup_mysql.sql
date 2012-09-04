-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generato il: Set 04, 2012 alle 12:40
-- Versione del server: 5.5.25
-- Versione PHP: 5.4.4

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT=0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `mysql_database_name`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `Push_Android`
--
-- Creazione: Set 04, 2012 alle 09:25
--

DROP TABLE IF EXISTS `Push_Android`;
CREATE TABLE IF NOT EXISTS `Push_Android` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idRegistration` varchar(255) NOT NULL,
  `enabled` enum('on','off') NOT NULL,
  `status` varchar(255) NOT NULL,
  `counter` int(10) unsigned NOT NULL,
  `lastSend` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `service_type` enum('c2dm','gcm') NOT NULL DEFAULT 'c2dm',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idRegistration` (`idRegistration`),
  KEY `enabled` (`enabled`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `Push_Android_Check`
--
-- Creazione: Set 04, 2012 alle 09:25
-- Ultimo cambiamento: Set 04, 2012 alle 09:54
--

DROP TABLE IF EXISTS `Push_Android_Check`;
CREATE TABLE IF NOT EXISTS `Push_Android_Check` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `status` enum('on','sending','off') NOT NULL,
  `service_type` enum('c2dm','gcm') NOT NULL DEFAULT 'c2dm',
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_type` (`service_type`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dump dei dati per la tabella `Push_Android_Check`
--

INSERT INTO `Push_Android_Check` (`id`, `status`, `service_type`, `lastchange`) VALUES
(1, 'off', 'gcm', '2012-09-04 09:54:45');
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

