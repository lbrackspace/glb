import time
import signal

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
                print "=== Responder Process Tick ==="
