import time

class HeartbeatProcess():
    def __init__(self, priority, tick, RUN):
        self.priority = priority
        self.tick_time = tick
        self.RUN = RUN
        print "Initialized Heartbeat Process."

    def run(self):
        while self.RUN.value:
            try:
                with self.priority.get_lock():
                    if self.priority.value == 'A':
                        print "Taking over as autonegotiated master."
                        self.priority.value = 'M'
                time.sleep(self.tick_time.value)
                print "<-- HEARTBEAT -->"
            except KeyboardInterrupt:
                pass #print "Heartbeat caught interrupt."
