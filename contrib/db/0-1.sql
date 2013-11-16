SET autocommit=0;
SET unique_checks=0;
SET foreign_key_checks=0;

DROP TABLE IF EXISTS `node`;
CREATE TABLE `node` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `glb_id` int(11) NOT NULL,
    `ip_address` varchar(128) DEFAULT NULL,
    `type` varchar(32) DEFAULT NULL,
    `status` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_d_glb` FOREIGN KEY (glb_id) REFERENCES glb(id)
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
    `threshold` varchar(11) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_d_node` FOREIGN KEY (node_id) REFERENCES node(id)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb`;
CREATE TABLE `glb` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `account_id` int(11) NOT NULL,
    `name` varchar(128) DEFAULT NULL,
    `cname` varchar(128) DEFAULT NULL,
    `status` varchar(128) DEFAULT NULL,
    `algorithm` varchar(32) DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT  `fk_d_status` FOREIGN KEY (status) REFERENCES glb_status(name)
    CONSTRAINT  `fk_d_algo` FOREIGN KEY (algorithm) REFERENCES glb_algorithm(name)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `glb_algorithm`;

CREATE TABLE `glb_algorithm` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

CREATE TABLE `glb_status` (
    `name` varchar(32) DEFAULT NULL,
    `description` varchar(128) DEFAULT NULL,
    PRIMARY KEY (`name`)
) ENGINE=InnoDB;

INSERT INTO `glb_algorithm` VALUES('RANDOM', 'Random');
INSERT INTO `glb_algorithm` VALUES('GEOIP', 'GeoIP');
INSERT INTO `glb_algorithm` VALUES('WEIGHTED', 'Weighted');
INSERT INTO `glb_algorithm` VALUES('LATENCY', 'Latency');
INSERT INTO `glb_algorithm` VALUES('POLICY', 'Policy');
INSERT INTO `glb_algorithm` VALUES('PERFORMANCE', 'Performance');
INSERT INTO `glb_algorithm` VALUES('NONE', 'Nada');

INSERT INTO `glb_status` VALUES('ACTIVE', 'Active');
INSERT INTO `glb_status` VALUES('BUILD', 'Build');
INSERT INTO `glb_status` VALUES('DELETED', 'Deleted');
INSERT INTO `glb_status` VALUES('PENDING_DELETE', 'Pending Delete');
INSERT INTO `glb_status` VALUES('PENDING_UPDATE', 'Pending Update');
INSERT INTO `glb_status` VALUES('QUEUE', 'Queue');
INSERT INTO `glb_status` VALUES('NONE', 'Nada');


set unique_checks=1;
set foreign_key_checks=1;
COMMIT;