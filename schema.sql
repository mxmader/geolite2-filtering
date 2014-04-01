--
-- Table structure for table `ip_blocks`
--

CREATE TABLE IF NOT EXISTS `ip_blocks` (
  `network_start_ip` varchar(64) NOT NULL,
  `ipv4_dec_start_address` int(32) unsigned NOT NULL DEFAULT '0',
  `ipv4_dec_end_address` int(32) unsigned NOT NULL DEFAULT '0',
  `network_mask_length` int(32) unsigned NOT NULL,
  `geoname_id` int(32) unsigned NOT NULL,
  `registered_country_geoname_id` int(32) unsigned NOT NULL,
  `represented_country_geoname_id` int(32) unsigned NOT NULL,
  `postal_code` varchar(16) NOT NULL,
  `latitude` varchar(24) NOT NULL,
  `longitude` varchar(24) NOT NULL,
  `is_anonymous_proxy` tinyint(1) NOT NULL,
  `is_satellite_provider` tinyint(1) NOT NULL,
  PRIMARY KEY (`ipv4_dec_start_address`,`ipv4_dec_end_address`),
  KEY `geoname_id` (`geoname_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `locations`
--

CREATE TABLE IF NOT EXISTS `locations` (
  `geoname_id` int(32) unsigned NOT NULL,
  `continent_code` varchar(8) NOT NULL,
  `continent_name` varchar(64) NOT NULL,
  `country_iso_code` varchar(8) NOT NULL,
  `country_name` varchar(64) NOT NULL,
  `subdivision_iso_code` varchar(8) NOT NULL,
  `subdivision_name` varchar(64) NOT NULL,
  `city_name` varchar(64) NOT NULL,
  `metro_code` varchar(8) NOT NULL,
  `time_zone` varchar(32) NOT NULL,
  PRIMARY KEY (`geoname_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for table `ip_blocks`
--
ALTER TABLE `ip_blocks`
  ADD CONSTRAINT `ip_blocks_ibfk_1` FOREIGN KEY (`geoname_id`) REFERENCES `locations` (`geoname_id`) ON UPDATE CASCADE;
