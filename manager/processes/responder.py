import time
import signal
import requests
import json

from manager.models.dcstats import DCStatusModel as DCStats


class ResponderProcess():
    def __init__(self, priority, session, response_queue, location, api_node, tick, RUN):
        self.priority = priority
        self.session = session
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
            except:
                #debug and error handling ...
                print "Something went wrong with the queue: ", qi if 'qi' in locals() else "BAD_QUEUE_GET"

            print "=== Responder Process Tick - STOP ==="

    def process_responses(self, responses):
        #have this handled in responder
        ## Should parse glbs list into list of string that follows protocol
        dc_stats = []
        responses = responses.split('\n')
        dcstats = { "dc_stats": [] }
        for resp in responses:
            print resp
            #build a factory of some sorts to clean up the parsing
            stat = {}

            if resp.startswith("SNAPSHOT"):
                stat['status'] = "ONLINE" if "SNAPSHOT PASSED:" in resp else "OFFLINE"
                stat['glb_id'] = resp[resp.find("glb_")+4:resp.find(".")]
                stat['location'] = self.location
                dcstats["dc_stats"].append(stat)

        api_url = ''.join((self.api_node['host'], self.api_node['path']))
        headers = {'X-Auth-Token': self.api_node['auth'] }
        print "%s -- %s -- %s" % (api_url, headers, json.dumps(dcstats))
        r = requests.put(api_url, data=json.dumps(dcstats), headers=headers)
        r.raise_for_status()