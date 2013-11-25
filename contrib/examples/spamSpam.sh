#!/bin/bash

if [ -n "$1" -a -n "$2" ]
then
    api_node=$1
    clients=$2
else
    echo "ERROR: correct usage is: $0 <api_node_IP> <num_clients> [ <create_count> <user_id> ]"
    exit 1
fi

if [ -n "$3" ]
then
    count="-c $3"
fi

if [ -n "$4" ]
then
    user="-u $4"
fi


echo "Copying spamCreate.py to client servers..."
for i in `seq 1 $clients`
do
        scp `dirname $0`/spamCreate.py root@client$i:
done

echo -n "Executing spamCreate.py remotely on servers:"
for i in `seq 1 $(($clients - 1))`
do
        echo -n " client$i"
        ssh root@client$i python spamCreate.py $api_node $count $user &
done
echo " client$client"
ssh root@client$clients python spamCreate.py $api_node $count $user
