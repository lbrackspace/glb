import time
import signal
import requests
import json
import traceback
import re

class ResponderProcess():
    def __init__(self, priority, response_queue, location, api_node, tick, RUN):
        self.priority = priority
        self.response_queue = response_queue
        self.location = location
        self.api_node = api_node
        self.tick_time = tick
        self.RUN = RUN
        print "Initialized Responder Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        while self.RUN.value:
            self.do_responding()
        signal.signal(signal.SIGINT, s)

    def do_responding(self):
        #time.sleep(self.tick_time.value)
        while self.priority.value == 'M' and not self.response_queue.empty():
            print "=== Responder Process Tick - START ==="
            try:
                qi = self.response_queue.get()
                self.process_responses(qi)
            except requests.HTTPError as httpe:
                print "API Returned error code %i -- message: %r" % \
                        (httpe.response.status_code, httpe.message)
            except requests.ConnectionError:
                self.response_queue.add(qi)
                time.sleep(1)
            except Exception:
                #debug and error handling ...
                traceback.print_exc()
                print "Something went wrong with the queue: ", \
                        qi if 'qi' in locals() else "BAD_QUEUE_GET"

            print "=== Responder Process Tick - STOP ==="

    def aggregate_responses(self, responses):
        #Some sort of decision has to be made to aggregate this data
        #Right now, I'll just return the first server's response
        return responses.values()[0]

    def process_responses(self, responses):
        #have this handled in responder
        ## Should parse glbs list into list of string that follows protocol
        responses = self.aggregate_responses(responses)
        responses = responses.split('\n')
        dcstats = {"dc_stats": []}
        for resp in responses:
            print resp
            resp = json.loads(resp)
            stat = {}

            if "type" in resp and resp['type'] == "SNAPSHOT":
                stat['status'] = "ONLINE" if resp['status'] == "PASSED" else \
                    "ERROR"
                stat['glb_id'] = resp['fqdn'][4:resp['fqdn'].find(".")]
                stat['location'] = self.location

                if resp['status'] == "FAILED":
                    messages = []
                    pattern = "r-([46])-([0-9]*)-(.*?)-([0-9]*)-(.*)"
                    for vname in resp['vnames']:
                        match = re.match(pattern, vname)
                        #iptype = match.group(1)
                        #ttl = match.group(2)
                        ip = match.group(3)
                        #weight = match.group(4)
                        message = match.group(5)
                        messages.append("%s -- %r" % (ip, message))
                    stat['response'] = ' / '.join(messages)

                dcstats["dc_stats"].append(stat)
                #Need to handle error and 'response'

        api_url = ''.join((self.api_node['host'], self.api_node['path']))
        headers = {'X-Auth-Token': self.api_node['auth']}
        print "%s -- %s -- %s" % (api_url, headers, json.dumps(dcstats))
        r = requests.put(api_url, data=json.dumps(dcstats), headers=headers)
        r.raise_for_status()