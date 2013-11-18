import requests

for num in range(1, 10000):
    name = "myTestGLB%i" % (num,)
    postdata = '{"glb": {"name": "%s","algorithm": "RANDOM","nodes": ' \
               '[{"ip_address": "10.1.1.1","type": "PASSIVE","monitor": ' \
               '{"interval": "30","threshold": "70"}}]}}' % (name,)
    r = requests.post('http://localhost:5000/1/glbs', data=postdata)
    if r.status_code != 200:
        break
    if num % 500 == 0:
        print r.json()

