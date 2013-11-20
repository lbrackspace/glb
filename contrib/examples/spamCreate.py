import requests
import time

batch = 1000

start = time.time()
for num in range(1, batch):
    name = "myTestGLB%i" % (num,)
    postdata = """
{ 
    "glb": { 
        "name": "%s",
        "algorithm": "RANDOM",
        "nodes": [
            { 
                "ip_address": "10.1.1.1",
                "type": "PASSIVE",
                "monitor": { 
                    "interval": "30",
                    "threshold": "70"
                }
            }
        ]
    }
}
""" % (name,)

    r = requests.post('http://198.101.242.5/1/glbs', data=postdata)
    if r.status_code != 200:
        break
    #if num % 500 == 0:
    #    print r.json()
end = time.time()

print "Performed %i creates in %d seconds." % (batch, end-start)
