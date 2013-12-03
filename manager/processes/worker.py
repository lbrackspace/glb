import time
import signal

class WorkerProcess():
    def __init__(self, priority, session, work_queue, response_queue, 
                    tick, RUN):
        self.priority = priority
        self.session = session
        self.work_queue = work_queue
        self.response_queue = response_queue
        self.tick_time = tick
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
            print "=== Worker Process Tick ==="
