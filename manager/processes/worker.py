import time
import signal
import socket
import json
import traceback

from multiprocessing import Value
from ctypes import c_bool, c_char_p

from manager.models.glb import GlobalLoadbalancerModel as GLB
from manager.models.dcstats import DCStatusModel as DCStats


class WorkerProcess():
    def __init__(self, priority, sessionmaker, pdns_servers,
                 pdns_port, response_queue, tick, last_poll_time, config, RUN):
        self.priority = priority
        self.sessionmaker = sessionmaker
        self.response_queue = response_queue
        self.tick_time = tick
        self.last_poll_time = last_poll_time
        self.pdns_servers = pdns_servers
        self.pdns_port = pdns_port
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
                responses = {}
                servers = json.loads(self.pdns_servers.value)
                for server in servers:
                    try:
                        sdr = self.send_data_pdns(glbs, server)
                        if len(sdr) > 0:
                            responses[server] = sdr
                    except:
                        traceback.print_exc()
                        responses[server] = "" #Need to decide what to do here
                print "Got responses from %i pDNS servers." % (len(responses),)
                if len(responses) > 0:
                    self.response_queue.put(responses)

                self.update_poll_time(glbs[0].update_time.__str__())
            else:
                print "== Worker Process: No data to process, up-to-date! =="
            print "=== Worker Process Tick - STOP ==="
        session.close()

    def send_data_pdns(self, glbs, server):
        s = socket.create_connection((server, self.pdns_port))
        fp = s.makefile("rw")

        for glb in glbs:
            update_type = glb.update_type
            if update_type != 'NONE':
                if update_type == 'FULL':
                    self.del_domain(fp, glb.fqdn)
                    self.add_domain(fp, glb.fqdn, glb.algorithm)
                elif update_type == 'CREATE' or update_type is None:
                    self.add_domain(fp, glb.fqdn, glb.algorithm)
                self.add_snapshot(fp, glb)
        print glbs

        ret = self.process_resp(fp, s)
        return ret

    def add_domain(self, fp, fqdn, algo):
        fp.write("ADD_DOMAIN %s %s\n" % (fqdn, algo))

    def del_domain(self, fp, fqdn):
        fp.write("DEL_DOMAIN %s\n" % (fqdn))

    def add_snapshot(self, fp, glb):
        nlist = []
        for n in glb.nodes:
            nlist.append('%s-%s-%s-%s' % (n.ip_type.split('IPV')[1], 30, n.ip_address,
                                          n.weight))
        fp.write("SNAPSHOT %s %s\n" % (glb.fqdn, ' '.join(nlist)))

    def process_resp(self, fp, s):
        ret = ""
        fp.write("OVER\n")
        fp.flush()
        while True:
            line = fp.readline()
            if line == "OVER\n":
                break
            ret += line
        fp.close()
        s.close()
        return ret.strip('\n')

    def update_poll_time(self, lpt):
        self.last_poll_time = Value(c_char_p, lpt)
        self.config.set('manager', 'last_poll_time', lpt)
        self.config.write(open('config.cfg', 'wb'))
