SET autocommit=0;
SET unique_checks=0;
SET foreign_key_checks=0;

DROP TABLE IF EXISTS `glb.node`;
CREATE TABLE `glb.node` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `glb_id` int(11) NOT NULL,
    `ip_address` varchar(128) DEFAULT NULL,
    `type` varchar(32) DEFAULT NULL,
    `weight` int(11) DEFAULT NULL,
    `ip_type` varchar(32) DEFAULT NULL,
    `status` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_d_ip_type` FOREIGN KEY (ip_type) REFERENCES `enum.glb.node.ip_type`(name),
    CONSTRAINT `fk_d_node_status` FOREIGN KEY (status) REFERENCES `enum.glb.node.status`(name),
    CONSTRAINT `fk_d_glb` FOREIGN KEY (glb_id) REFERENCES glb(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb.name_server`;
CREATE TABLE `glb.name_server` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(15) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `glb.node.monitor`;
CREATE TABLE `glb.node.monitor` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `node_id` int(11) DEFAULT NULL,
    `interval` int(11) DEFAULT NULL,
    `threshold` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_d_node` FOREIGN KEY (node_id) REFERENCES `glb.node`(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb.status`;
CREATE TABLE `glb.status` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `glb_id` int(11) NOT NULL,
    `time` timestamp DEFAULT CURRENT_TIMESTAMP,
    `location` varchar(16) DEFAULT NULL,
    `status` varchar(16) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `glb_time_loc` (glb_id,location,time),
    CONSTRAINT `fk_d_status` FOREIGN KEY (status) REFERENCES `enum.glb.status`(name),
    CONSTRAINT `fk_d_glb_id` FOREIGN KEY (glb_id) REFERENCES glb(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb`;
CREATE TABLE `glb` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `account_id` int(11) NOT NULL,
    `name` varchar(128) DEFAULT NULL,
    `cname` varchar(128) DEFAULT NULL,
    `algorithm` varchar(32) DEFAULT NULL,
    `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_d_algo` FOREIGN KEY (algorithm) REFERENCES `enum.glb.algorithm`(name)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum.glb.algorithm`;
CREATE TABLE `enum.glb.algorithm` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum.glb.status`;
CREATE TABLE `enum.glb.status` (
    `name` varchar(16) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum.glb.node.status`;
CREATE TABLE `enum.glb.node.status` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum.glb.node.ip_type`;
CREATE TABLE `enum.glb.node.ip_type` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `enum.glb.node.region`;
CREATE TABLE `enum.glb.node.region` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(32) DEFAULT NULL,
    `code` varchar(128) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb.node.region`;
CREATE TABLE `glb.node.region` (
    `node_id` int(11),
    `region_id` int(11)
) ENGINE=InnoDB;


INSERT INTO `enum.glb.algorithm` VALUES('RANDOM', 'Random');
INSERT INTO `enum.glb.algorithm` VALUES('GEOIP', 'GeoIP');
INSERT INTO `enum.glb.algorithm` VALUES('WEIGHTED', 'Weighted');
INSERT INTO `enum.glb.algorithm` VALUES('LATENCY', 'Latency');
INSERT INTO `enum.glb.algorithm` VALUES('POLICY', 'Policy');
INSERT INTO `enum.glb.algorithm` VALUES('PERFORMANCE', 'Performance');
INSERT INTO `enum.glb.algorithm` VALUES('NONE', 'Nada');

INSERT INTO `enum.glb.status` VALUES('ACTIVE', 'Active');
INSERT INTO `enum.glb.status` VALUES('BUILD', 'Build');
INSERT INTO `enum.glb.status` VALUES('DELETED', 'Deleted');
INSERT INTO `enum.glb.status` VALUES('PENDING_DELETE', 'Pending Delete');
INSERT INTO `enum.glb.status` VALUES('PENDING_UPDATE', 'Pending Update');
INSERT INTO `enum.glb.status` VALUES('QUEUE', 'Queue');
INSERT INTO `enum.glb.status` VALUES('NONE', 'Nada');

INSERT INTO `enum.glb.node.status` VALUES('OFFLINE', 'Node is offline');
INSERT INTO `enum.glb.node.status` VALUES('ONLINE', 'Node is online');
INSERT INTO `enum.glb.node.status` VALUES('UNKNOWN', 'Node is in an unknown status');

INSERT INTO `enum.glb.node.ip_type` VALUES('IPV4', 'IPV4');
INSERT INTO `enum.glb.node.ip_type` VALUES('IPV6', 'IPV6');

INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('CATCH_ALL', '1', 'A region for ip addresses that do not map to other regions');
INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('NORTH_AMERICA', '2', 'The North American region');
INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('SOUTH_AMERICA', '3', 'The South American region');
INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('EUROPE', '4', 'European region');
INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('ASIA', '5', 'Asian region');
INSERT INTO `enum.glb.node.region`(`name`, `code`, `description`) VALUES('PACIFIC', '6', 'Pacific region');


set unique_checks=1;
set foreign_key_checks=1;
COMMIT;
