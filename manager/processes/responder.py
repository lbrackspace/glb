import time
import signal

from manager.models.dcstats import DCStatusModel as DCStats


class ResponderProcess():
    def __init__(self, priority, session, response_queue, tick, RUN):
        self.priority = priority
        self.session = session
        self.response_queue = response_queue
        self.tick_time = tick
        self.RUN = RUN
        print "Initialized Responder Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        while self.RUN.value:
            self.do_responding()
        signal.signal(signal.SIGINT, s)

    def do_responding(self):
        time.sleep(self.tick_time.value)
        if self.priority.value == 'M':
            print "=== Responder Process Tick - START ==="
            qi = ""
            try:
                qi = self.response_queue.get()
            except:
                #debug and error handling ...
                print "Something went wrong with the que"

            self.process_responses(qi)
            print "=== Responder Process Tick - STOP ==="

    def process_responses(self, responses):
        #have this handled in responder
        ## Should parse glbs list into list of string that follows protocol
        dc_stats = []
        ls = responses.split('\n')
        for l in ls:
            print l
            #build a factory of some sorts to clean up the parsing
            stat = DCStats()
            if "ADD_DOMAIN" in l:
                astatus = "ONLINE" if "PASSED" in l else "OFFLINE"
                al = l.split("glb_")
                al = al[1].split(".")
                stat.glb_id = al[0]