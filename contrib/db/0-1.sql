SET autocommit=0;
SET unique_checks=0;
SET foreign_key_checks=0;

DROP TABLE IF EXISTS `node`;
CREATE TABLE `node` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `glb_id` int(11) NOT NULL,
    `ip_address` varchar(128) DEFAULT NULL,
    `type` varchar(32) DEFAULT NULL,
    `weight` int(11) DEFAULT NULL,
    `ip_type` varchar(32) DEFAULT NULL,
    `status` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_n_ip_type` FOREIGN KEY (ip_type) REFERENCES `enum_node_ip_type`(name),
    CONSTRAINT `fk_n_node_status` FOREIGN KEY (status) REFERENCES `enum_node_status`(name),
    CONSTRAINT `fk_n_glb` FOREIGN KEY (glb_id) REFERENCES glb(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `name_server`;
CREATE TABLE `name_server` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(15) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `monitor`;
CREATE TABLE `monitor` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `node_id` int(11) DEFAULT NULL,
    `interval` int(11) DEFAULT NULL,
    `threshold` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_m_node_id` FOREIGN KEY (node_id) REFERENCES `node`(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `dc_stat`;
CREATE TABLE `dc_stat` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `glb_id` int(11) NOT NULL,
    `updated` timestamp DEFAULT CURRENT_TIMESTAMP,
    `location` varchar(16) DEFAULT NULL,
    `status` varchar(16) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `glb_updated_loc` (glb_id,location,updated),
    CONSTRAINT `fk_dc_status` FOREIGN KEY (status) REFERENCES `enum_dc_status`(name),
    CONSTRAINT `fk_dc_location` FOREIGN KEY (location) REFERENCES `enum_dc_location`(name),
    CONSTRAINT `fk_dc_glb_id` FOREIGN KEY (glb_id) REFERENCES glb(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb`;
CREATE TABLE `glb` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `account_id` int(11) NOT NULL,
    `name` varchar(128) DEFAULT NULL,
    `cname` varchar(128) DEFAULT NULL,
    `algorithm` varchar(32) DEFAULT NULL,
    `status` varchar(32) DEFAULT NULL,
    `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_g_status` FOREIGN KEY (status) REFERENCES `enum_glb_status`(name),
    CONSTRAINT  `fk_g_algo` FOREIGN KEY (algorithm) REFERENCES `enum_glb_algorithm`(name)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_glb_algorithm`;
CREATE TABLE `enum_glb_algorithm` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_glb_status`;
CREATE TABLE `enum_glb_status` (
    `name` varchar(16) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_node_status`;
CREATE TABLE `enum_node_status` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_node_ip_type`;
CREATE TABLE `enum_node_ip_type` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_node_region`;
CREATE TABLE `enum_node_region` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(32) DEFAULT NULL,
    `code` varchar(128) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_dc_status`;
CREATE TABLE `enum_dc_status` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_dc_region`;
CREATE TABLE `enum_dc_region` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum_dc_location`;
CREATE TABLE `enum_dc_location` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `node_region`;
CREATE TABLE `node_region` (
    `node_id` int(11),
    `region_id` int(11)
) ENGINE=InnoDB;


INSERT INTO `enum_glb_algorithm` VALUES('RANDOM', 'Random');
INSERT INTO `enum_glb_algorithm` VALUES('GEO_IP', 'GeoIP');
INSERT INTO `enum_glb_algorithm` VALUES('WEIGHTED', 'Weighted');
INSERT INTO `enum_glb_algorithm` VALUES('LATENCY', 'Latency');
INSERT INTO `enum_glb_algorithm` VALUES('POLICY', 'Policy');
INSERT INTO `enum_glb_algorithm` VALUES('PERFORMANCE', 'Performance');
INSERT INTO `enum_glb_algorithm` VALUES('NONE', 'Nada');

INSERT INTO `enum_glb_status` VALUES('ACTIVE', 'Active');
INSERT INTO `enum_glb_status` VALUES('BUILD', 'Build');
INSERT INTO `enum_glb_status` VALUES('DELETED', 'Deleted');
INSERT INTO `enum_glb_status` VALUES('PENDING_DELETE', 'Pending Delete');
INSERT INTO `enum_glb_status` VALUES('PENDING_UPDATE', 'Pending Update');
INSERT INTO `enum_glb_status` VALUES('QUEUE', 'Queue');
INSERT INTO `enum_glb_status` VALUES('NONE', 'Nada');

INSERT INTO `enum_node_status` VALUES('OFFLINE', 'Node is offline');
INSERT INTO `enum_node_status` VALUES('ONLINE', 'Node is online');
INSERT INTO `enum_node_status` VALUES('UNKNOWN', 'Node is in an unknown status');

INSERT INTO `enum_dc_status` VALUES('OFFLINE', 'Node is offline for this DC');
INSERT INTO `enum_dc_status` VALUES('ONLINE', 'Node is online for this DC');
INSERT INTO `enum_dc_status` VALUES('UNKNOWN', 'Node is in an unknown status for this DC');

INSERT INTO `enum_dc_location` VALUES('DFW', 'DFW Region');
INSERT INTO `enum_dc_location` VALUES('ORD', 'ORD Region');
INSERT INTO `enum_dc_location` VALUES('HKG', 'HKG Region');
INSERT INTO `enum_dc_location` VALUES('SYD', 'SYD Region');
INSERT INTO `enum_dc_location` VALUES('IAD', 'IAD Region');

INSERT INTO `enum_node_ip_type` VALUES('IPV4', 'IPV4');
INSERT INTO `enum_node_ip_type` VALUES('IPV6', 'IPV6');

INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('CATCH_ALL', '1', 'A region for ip addresses that do not map to other regions');
INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('NORTH_AMERICA', '2', 'The North American region');
INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('SOUTH_AMERICA', '3', 'The South American region');
INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('EUROPE', '4', 'European region');
INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('ASIA', '5', 'Asian region');
INSERT INTO `enum_node_region`(`name`, `code`, `description`) VALUES('PACIFIC', '6', 'Pacific region');


set unique_checks=1;
set foreign_key_checks=1;
COMMIT;
