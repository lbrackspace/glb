#!/bin/bash
SQL_FILE=$1
CONFIG_FILE=/etc/rackspace/glb/config.cfg

pw=$(awk -F'db_password=' '{print $2}' $CONFIG_FILE)
un=glb

echo "Recreating database and user privileges"
mysql -uroot -e"drop database if exists glb; create database glb; GRANT ALL PRIVILEGES ON glb.* TO $un@localhost IDENTIFIED BY '$pw'"

echo "Importing the sql file"
mysql -uglb -p$pw -Dglb <$SQL_FILE

echo "Displaying the created tables..."
echo | mysql -uglb -p$pw -e"use glb; show tables;"
