import time
import signal

from multiprocessing import Value
from ctypes import c_bool, c_char_p

from manager.models.glb import GlobalLoadbalancerModel as GLB
from manager.models.dcstats import DCStatusModel as DCStats


class WorkerProcess():
    def __init__(self, priority, session, response_queue,
                 tick, last_poll_time, config, RUN):
        self.priority = priority
        self.session = session
        self.response_queue = response_queue
        self.tick_time = tick
        self.last_poll_time = last_poll_time
        self.config = config
        self.RUN = RUN
        print "Initialized Worker Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        while self.RUN.value:
            self.do_work()
        signal.signal(signal.SIGINT, s)

    def do_work(self):
        time.sleep(self.tick_time.value)
        if self.priority.value == 'M':
            print "=== Worker Process Tick - START ==="
            # Do work here (worry about paging the SQL query later)
            glbs = self.session.query(GLB). \
                filter(GLB.update_time > self.last_poll_time.value). \
                order_by(GLB.update_time.desc()).all()

            if glbs:
                print "== Worker Process: Processing %d glbs ==" % len(glbs)
                # Send the data to pDNS
                resp = self.send_data_pdns(glbs)

                #reponder will handle the response
                self.response_queue.put(resp)

                self.update_poll_time(glbs[0].update_time.__str__())
            else:
                print "== Worker Process: No data to process, up-to-date! =="
            print "=== Worker Process Tick - STOP ==="

    def send_data_pdns(self, glbs):
        #data should be strings of required information following the
        # custom protocol found here:
        # https://one.rackspace.com/display/
        # compute/Data+Controller+Message+Processing

        #do stuff

        return "ADD_DOMAIN PASSED: glb_13.rackexp.org\n " \
               "SNAPSHOT PASSED: glb_13.rackexp.org  a4-30-10.1.1.1-1"

    def update_poll_time(self, lpt):
        self.last_poll_time.value = lpt
        self.config.set('manager', 'last_poll_time', lpt)
        self.config.write(open('config.cfg', 'wb'))