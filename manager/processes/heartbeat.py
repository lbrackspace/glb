import time
import signal

class HeartbeatProcess():
    def __init__(self, priority, tick, RUN):
        self.priority = priority
        self.tick_time = tick
        self.RUN = RUN
        print "Initialized Heartbeat Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        while self.RUN.value:
            self.do_heartbeat()
        signal.signal(signal.SIGINT, s)

    def do_heartbeat(self):
        with self.priority.get_lock():
            if self.priority.value == 'A':
                print "Taking over as autonegotiated master."
                self.priority.value = 'M'
        time.sleep(self.tick_time.value)
        print "<-- HEARTBEAT -->"
