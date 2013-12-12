#!/usr/bin/env python
import requests
import time
import argparse

parser = argparse.ArgumentParser(
    description="Spam some create requests at the GLB API.")
parser.add_argument('node', help="IP Address of the API node")
parser.add_argument('-c', '--count', type=int, default=1000,
                    help="Number of create requests to make")
parser.add_argument('-u', '--user', default="1",
                    help="UserID used to submit create requests")
args = parser.parse_args()

post_url = 'http://%s/%s/glbs' % (args.node, args.user)
start = time.time()
for num in range(0, args.count):
    name = "myTestGLB%i" % (num,)
    postdata = """
{ 
    "glb": { 
        "name": "%s",
        "algorithm": "RANDOM",
        "nodes": [
            { 
                "ip_address": "10.1.1.2",
                "ip_type": "IPV4",
                "type": "ACTIVE",
                "monitor": { 
                    "interval": "30",
                    "threshold": "2"
                }
            },
            {
                "ip_address": "10.1.1.3",
                "ip_type": "IPV4",
                "type": "ACTIVE",
                "monitor": { 
                    "interval": "30",
                    "threshold": "2"
                }
            }

        ]
    }
}
""" % (name,)

    r = requests.post(post_url, data=postdata)
    if r.status_code != 200:
        break
        #if num % 500 == 0:
        #    print r.json()
end = time.time()

print "Performed %i creates in %d seconds." % (args.count, end - start)
