import time
import signal
import socket

from multiprocessing import Value
from ctypes import c_bool, c_char_p

from manager.models.glb import GlobalLoadbalancerModel as GLB
from manager.models.dcstats import DCStatusModel as DCStats


class WorkerProcess():
    def __init__(self, priority, sessionmaker, response_queue,
                 tick, last_poll_time, config, RUN):
        self.priority = priority
        self.sessionmaker = sessionmaker
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
        session = self.sessionmaker()
        if self.priority.value == 'M':
            print "=== Worker Process Tick - START ==="
            # Do work here (worry about paging the SQL query later)
            glbs = session.query(GLB). \
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
        session.close()

    def send_data_pdns(self, glbs):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8888))
        fp = s.makefile("rw")

        ret = ""
        for glb in glbs:
            update_type = glb.update_type
            if update_type != 'NONE':
                if update_type == 'FULL':
                    self.del_domain(fp, glb.cname)
                    self.add_domain(fp, glb.cname, glb.algorithm)
                if update_type == 'CREATE' or update_type is None:
                    self.add_domain(fp, glb.cname, glb.algorithm)
                self.add_snapshot(fp, glb)

        fp.write("OVER\n")
        fp.flush()
        while True:
            line = fp.readline()
            ret += line
            if line == "OVER\n":
                break
        print glbs
        return ret

    def add_domain(self, fp, cname, algo):
        fp.write("ADD_DOMAIN %s %s\n" % (cname, algo))

    def del_domain(self, fp, cname):
        fp.write("DEL_DOMAIN %s\n" % (cname))

    def add_snapshot(self, fp, glb):
        nlist = []
        for n in glb.nodes:
            nlist.append('%s-%s-%s-%s' % (n.ip_type.split('IPV')[1], 30, n.ip_address,
                                          n.weight))
        fp.write("SNAPSHOT %s %s\n" % (glb.cname, ' '.join(nlist)))

    def update_poll_time(self, lpt):
        self.last_poll_time = Value(c_char_p, lpt)
        self.config.set('manager', 'last_poll_time', lpt)
        self.config.write(open('config.cfg', 'wb'))