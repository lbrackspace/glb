clients=8

for i in `seq 1 $clients`
do
        scp spamCreate.py root@client$i:
done

for i in `seq 1 $clients`
do
        ssh root@client$i python spamCreate.py &
done
