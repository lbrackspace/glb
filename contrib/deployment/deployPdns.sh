#!/bin/bash

function setupServer {
        ssh_opts="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
        echo "Copying SSH pubkey to server..."
        tempdir=`mktemp -d /tmp/glbtemp.XXXXXX`
        mkdir $tempdir/.ssh
        cp ~/.ssh/id_rsa.pub $tempdir/.ssh/authorized_keys2
        scp -rq $ssh_opts $tempdir/.ssh root@$1: &> /dev/null
        rm -rf $tempdir &> /dev/null

        ssh $ssh_opts root@$1 'apt-get update' &> /dev/null
        ssh $ssh_opts root@$1 'if [ -z `which lsb_release` ]; then apt-get install -yq lsb-release; fi' &> /dev/null
        debian_version=`ssh $ssh_opts root@$1 lsb_release -c 2> /dev/null | awk '{ print $2 }'`
        case $debian_version in
                wheezy)
                        echo "Detected distribution: Debian $debian_version, proceeding with deployment."
                        extra_packages="libboost1.49-all-dev"
                        ;;
                precise)
                        echo "Detected distribution: Debian $debian_version, proceeding with deployment."
                        extra_packages="libboost1.48-all-dev"
                        ;;
                raring | quantal | saucy)
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04 (Precise)."
                        return 1
                        ;;
                squeeze)
                        echo "Debian $debian_version is unsupported."
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04 (Precise)."
                        return 1
                        ;;
                lucid)
                        echo "Ubuntu $debian_version is unsupported."
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04 (Precise)."
                        return 1
                        ;;
                *)
                        echo "This script must be run on a Debian 7 (Wheezy) or Ubuntu 12.04 (Precise)."
                        return 1
                        ;;
        esac

        echo -n "Copying PDNS files to server..."
            ssh $ssh_opts root@$1 'wget wget http://utils.rackexp.org/pdns-3.3.tar -O - | tar xf -' &> /dev/null
        echo " done."
        echo -n "Adding GLB Backend module to PDNS..."
            ssh $ssh_opts root@$1 'if [ -z `which git` ]; then apt-get install -yq git; fi' &> /dev/null
            ssh $ssh_opts root@$1 'cd pdns-3.3/modules && git clone https://github.com/lbrackspace/glbbackend.git' &> /dev/null
            ssh $ssh_opts root@$1 "sed -i 's:modules/randombackend/Makefile:modules/randombackend/Makefile modules/glbbackend/Makefile:' pdns-3.3/configure.ac" &> /dev/null
        echo " done."
        echo -n "Installing PDNS requirements with apt..."
            ssh $ssh_opts root@$1 "apt-get install -yq build-essential automake pkg-config liblua5.1*-dev screen $extra_packages" &> /dev/null
        echo " done."
        echo -n "Configuring PDNS (this could take a while)..."
            ssh $ssh_opts root@$1 "cd pdns-3.3/ && ./bootstrap" &> /dev/null
            ssh $ssh_opts root@$1 "cd pdns-3.3/ && ./configure --prefix='/opt/pdns' --with-modules='glb'"
        echo " done."
        echo -n "Building PDNS (this could take a while)..."
            ssh $ssh_opts root@$1 "cd pdns-3.3/ && make && make install"
        echo " done."

        ssh $ssh_opts root@$1 "cd /opt/pdns && echo -e 'glb-server-ip=0.0.0.0\nglb-server-port=8888\nglb-dmc-ips=0.0.0.0\nglb-dmc-port=5050' > etc/pdns.conf" &> /dev/null
        ssh $ssh_opts root@$1 "cd /opt/pdns && screen -d -m sbin/pdns_server --launch='glb'" &> /dev/null
}

pushd `dirname $0`/../../ > /dev/null
if [ -z "$1" ]
then
    echo "usage: $0 <ip>"
else
    setupServer $1
fi
popd > /dev/null
