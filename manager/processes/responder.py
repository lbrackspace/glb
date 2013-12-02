import time

class ResponderProcess():
    def __init__(self, priority, session, response_queue, tick, RUN):
        self.priority = priority
        self.session = session
        self.response_queue = response_queue
        self.tick_time = tick
        self.RUN = RUN
        print "Initialized Responder Process."

    def run(self):
        while self.RUN.value:
            try:
                time.sleep(self.tick_time.value)
                if self.priority.value == 'M':
                    print "=== Responder Process Tick ==="
            except KeyboardInterrupt:
                pass #print "Responder caught interrupt."
