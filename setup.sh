#!/bin/bash

ROOT_SQL_PASS="YouShouldChangeThis"

function setup {
	if [ -z "`grep percona /etc/apt/sources.list`" ]
	then
		echo -n "Adding apt repository for percona-server..."
		apt-key adv --keyserver keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A &> /dev/null
		echo "deb http://repo.percona.com/apt wheezy main" >> /etc/apt/sources.list
		echo "deb-src http://repo.percona.com/apt wheezy main" >> /etc/apt/sources.list
		echo " done."
	fi

	echo -n "Running apt-get update..."
	apt-get update > /dev/null
	echo " done."

	echo -n "Installing package depdendencies via apt..."
	export DEBIAN_FRONTEND=noninteractive
	apt-get -q -y install vim lighttpd python-pip percona-server-5.6 libmysqlclient-dev python-dev &> /dev/null
	echo " done."

	echo -n "Installing requirement dependencies via pip..."
	pip install --upgrade 'distribute>=0.7.3' > /dev/null
	pip install --upgrade 'six>=1.3.0' > /dev/null
	echo " done."

	echo -n "Installing requirements via pip..."
	pip install --upgrade -r requires.txt &> /dev/null
	echo " done."

	echo -n "Deploying files to /var/www/glb and setting permissions..."
	mkdir /var/www/glb
	cp -r * /var/www/glb/
	cp contrib/config/example.config.cfg /var/www/glb/config.cfg
	chgrp -R www-data /var/www/glb
	chmod -R g+rX /var/www/glb
	echo " done."

	echo -n "Setting up MySQL DB..."
	mysql_status=`echo "status" | mysql -u root 2>&1 | grep '^ERROR 1045'`
	if [ -z "$mysql_status" ]
	then
		mysql -u root < "contrib/db/init.sql"
		mysql -u root glb < "contrib/db/0-1.sql"
		mysqladmin -u root password "$ROOT_SQL_PASS"
		echo " done."
	else
		echo " needs password."
		mysql -u root -p < "contrib/db/init.sql"
		mysql -u root -p glb < "contrib/db/0-1.sql"
	fi

	echo -n "Setting up lighttpd config..."
	sed -i 's/^#\(.*mod_rewrite\)/ \1/' /etc/lighttpd/lighttpd.conf
	sed "s:WORKING_DIR:/var/www/glb:" contrib/deployment/50-glb.conf > /etc/lighttpd/conf-available/50-glb.conf 
	ln -s /etc/lighttpd/conf-available/10-fastcgi.conf /etc/lighttpd/conf-enabled/ &> /dev/null
	ln -s /etc/lighttpd/conf-available/50-glb.conf /etc/lighttpd/conf-enabled/ &> /dev/null
	echo " done."
	
	service lighttpd restart
}

pushd `dirname $0` > /dev/null
setup
popd > /dev/null
