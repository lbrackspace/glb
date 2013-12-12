import time
import signal
import socket
import json
import traceback
import datetime

from multiprocessing import Value
from ctypes import c_bool, c_char_p
from sqlalchemy import or_

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
        if self.priority.value == 'M':
            session = self.sessionmaker()
            print "=== Worker Process Tick - START ==="
            # Do work here (worry about paging the SQL query later)
            glbs = session.query(GLB). \
                filter(GLB.update_time > self.last_poll_time.value). \
                filter(GLB.update_type != "NONE").order_by(GLB.update_time. \
                desc()).all()

            new_servers, inc_servers = [], []
            responses = {}
            with self.pdns_servers.get_lock():
                try:
                    servers = json.loads(self.pdns_servers.value)
                except:
                    print "WTF"
                    servers = []

                for server in servers:
                    if server['mode'].upper() == "NEW":
                        new_servers.append(server)
                    else:
                        inc_servers.append(server)

                #print "New pDNS Servers:", new_servers
                #print "Incremental pDNS Servers:", inc_servers

                if new_servers:
                    print "== Worker Process: Processing new servers: %d  ==" \
                          % len(new_servers)
                    all_glbs = session.query(GLB). \
                        filter(or_(GLB.status == "BUILD",
                                   GLB.status == "ACTIVE")) \
                        .all()
                    for server in new_servers: #This may need to be threaded
                        try:
                            sdr = self.send_data_to_pdns(all_glbs, server[
                                'ip'], new=True)
                            if sdr:
                                responses[server['ip']] = sdr
                            server['mode'] = "INCREMENTAL"
                        except:
                            #Need to decide what to do here
                            traceback.print_exc()
                            responses[server['ip']] = ""
                    self.pdns_servers.value = json.dumps(servers)

            if glbs:
                print "== Worker Process: Processing %d glbs ==" % len(glbs)
                # Send the data to pDNS
                for server in inc_servers: #This may need to be threaded
                    try:
                        sdr = self.send_data_to_pdns(glbs, server['ip'])
                        if sdr:
                            responses[server['ip']] = sdr
                    except:
                        #Need to decide what to do here
                        traceback.print_exc()
                        responses[server['ip']] = ""
                print "Got responses from %i pDNS servers." % (len(responses),)
                if responses: #NEED TO REVIEW THIS
                    self.update_poll_time(glbs[0].update_time.__str__())
            else:
                print "== Worker Process: No glbs to process, up-to-date! " \
                      "Polled at %s ==" % datetime.datetime.utcnow(). \
                          strftime("%Y-%m-%d %H:%M:%S")
            if len(responses) > 0:
                self.response_queue.put(responses)
            print "=== Worker Process Tick - STOP ==="
            session.close()

    def send_data_to_pdns(self, glbs, server, new = False):
        command = ""
        if new:
            command += self.write_soa()
        for glb in glbs: # Possibly needs a try/catch within loop to allow
        # processing to continue
            update_type = glb.update_type
            if update_type != 'NONE' or new:
                if update_type == 'CREATE' or update_type is None or new:
                    command += self.add_domain(glb.fqdn, glb.algorithm)
                elif update_type == 'FULL':
                    command += self.del_domain(glb.fqdn)
                    command += self.add_domain(glb.fqdn, glb.algorithm)
                command += self.add_snapshot(glb)
        print "pDNS %s Processing GLBS: " % server, glbs
        print "pDNS %s Command: " % server, command.strip("\n")

        if command: # Possibly needs a try/catch
            command += "OVER\n"
            pDNS_socket = socket.create_connection((server, self.pdns_port), 2)
            pDNS_socketFile = pDNS_socket.makefile("rw")
            pDNS_socketFile.write(command)
            pDNS_socketFile.flush()
            response_data = self.process_response(pDNS_socketFile)
            pDNS_socketFile.close()
            pDNS_socket.close()
            return response_data

    def add_domain(self, fqdn, algo):
        return "ADD_DOMAIN %s %s\n" % (fqdn, algo)

    def del_domain(self, fqdn):
        return "DEL_DOMAIN %s\n" % (fqdn)

    def add_snapshot(self, glb):
        node_list = []
        for n in glb.nodes:
            node_list.append('%s-%s-%s-%s' % (n.ip_type.split('IPV')[1], 30, n.ip_address,
                                          n.weight))
        return "SNAPSHOT %s %s\n" % (glb.fqdn, ' '.join(node_list))

    def write_soa(self):
        return "SET_SOA glb.rackspace.com ns1.rackspace.net. root.rackspace" \
               ".net. 2013102907 28800 14400 3600000 300\n"

    def process_response(self, pDNS_socketFile):
        ret = ""
        while True: # Possibly needs a try/catch
            line = pDNS_socketFile.readline()
            if line == "OVER\n":
                break
            ret += line
        return ret.strip('\n')

    def update_poll_time(self, lpt):
        self.last_poll_time = Value(c_char_p, lpt)
        self.config.set('manager', 'last_poll_time', lpt)
        self.config.write(open('config.cfg', 'wb'))
