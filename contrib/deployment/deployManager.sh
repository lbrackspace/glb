#!/bin/bash

ROOT_SQL_PASS="YouShouldChangeThis"

function setup {
        debian_version=`lsb_release -c 2> /dev/null | awk '{ print $2 }'`
        case $debian_version in
                wheezy)
                        echo "Detected distribution: Debian $debian_version, proceeding with deployment."
                        extra_packages=""
                        ;;
                raring | quantal | precise | saucy)
                        echo "Detected distribution: Ubuntu $debian_version, proceeding with deployment."
                        extra_packages="libssl-dev"
                        ;;
                squeeze)
                        echo "Detected distribution: Debian $debian_version, which is unsupported."
                        extra_packages=""
                        return 1
                        ;;
                lucid)
                        echo "Detected distribution: Ubuntu $debian_version, which is unsupported."
                        #extra_packages="libssl-dev"
                        return 1
                        ;;
                *)
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04+ (Precise or later)."
                        return 1
                        ;;
        esac

	echo -n "Running apt-get update..."
	apt-get update > /dev/null
	echo " done."

	echo -n "Installing package depdendencies via apt..."
	export DEBIAN_FRONTEND=noninteractive
	apt-get -q -y install python-pip libmysqlclient-dev python-dev $extra_packages &> /dev/null
	echo " done."

	echo -n "Installing requirement dependencies via pip..."
	pip install --upgrade 'distribute>=0.7.3' > /dev/null
	pip install --upgrade 'six>=1.3.0' > /dev/null
	echo " done."

	echo -n "Installing requirements via pip..."
	pip install --upgrade -r requires.txt &> /dev/null
	echo " done."

        cp contrib/config/example.config.cfg config.cfg
}

function setupServer {
        ssh_opts="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
        echo "Copying SSH pubkey to server..."
        tempdir=`mktemp -d /tmp/glbtemp.XXXXXX`
        mkdir $tempdir/.ssh
        cp ~/.ssh/id_rsa.pub $tempdir/.ssh/authorized_keys2
        scp -rq $ssh_opts $tempdir/.ssh root@$1: &> /dev/null
        rm -rf $tempdir &> /dev/null

        ssh $ssh_opts root@$1 'if [ -z `which lsb_release` ]; then apt-get install -yq lsb-release &> /dev/null; fi' &> /dev/null
        debian_version=`ssh $ssh_opts root@$1 lsb_release -c 2> /dev/null | awk '{ print $2 }'`
        case $debian_version in
                wheezy)
                        ;;
                raring | quantal | precise | saucy)
                        ;;
                squeeze)
                        echo "Debian $debian_version is unsupported."
                        return 1
                        ;;
                lucid)
                        echo "Ubuntu $debian_version is unsupported."
                        return 1
                        ;;
                *)
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04+ (Precise or later)."
                        return 1
                        ;;
        esac

        echo -n "Copying GLB files to server..."
        rsync -aqz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --exclude=".git*" --delete ./ root@$1:glb/ &> /dev/null
        echo " done."

        ssh $ssh_opts root@$1 glb/contrib/deployment/deployManager.sh 2> /dev/null

        echo "Connect to server and run glb/runManager.sh to start the controller."
}

pushd `dirname $0`/../../ > /dev/null
if [ -z "$1" ]
then
    setup
else
    setupServer $1
fi
popd > /dev/null
