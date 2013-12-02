import time

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
        while self.RUN.value:
            try:
                time.sleep(self.tick_time.value)
                if self.priority.value == 'M':
                    print "=== Worker Process Tick ==="
            except KeyboardInterrupt:
                pass #print "Responder caught interrupt."
