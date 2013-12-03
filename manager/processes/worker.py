import time
import signal
from manager.models.glb import GlobalLoadbalancerModel as GLB

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
            # Do work here (worry about paging the SQL query later)
            glbs = self.session.query(GLB).\
                      filter(GLB.update_time > self.last_poll_time.value).all()
            # Send the data to pDNS
            # Push response data into self.response_queue
            # Update self.last_poll_time, self.config.set last_poll_time as well
            print "=== Worker Process Tick ==="
