import json
import time
import signal
import threading
import SocketServer
import socket
import random
import subprocess
import traceback

class HeartbeatProcess():
    def __init__(self, port, others, pdns, priority, tick, last_poll, RUN):
        self.port = port
        self.priority = priority
        self.tick_time = tick
        self.last_poll = last_poll
        self.RUN = RUN
        self.others = others
        self.pdns = pdns
        self.server = SimpleServer(('', self.port),
                                   HeartbeatRequestHandler, self.priority,
                                   self.others, self.pdns, self.last_poll)
        if len(self.others) == 0:
            self.priority.value = 'M'
        print "Initialized Heartbeat Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        threading.Thread(target=self.listen).start()
        self.auto_negotiate()

        while self.RUN.value:
            self.do_heartbeat()
        self.server.shutdown()
        signal.signal(signal.SIGINT, s)

    def auto_negotiate(self):
        if self.priority.value == "A":
            time.sleep(random.uniform(0,2))
        with self.priority.get_lock():
            auto_add_heartbeat = {}
            #auto_add_pdns = {}
            servers = self.others.keys()

            if self.priority.value == 'A':
                print "Attempting to negotiate server priority with ", servers

            for s in servers:
                try:
                    sock = socket.create_connection((s, self.port), 2)
                    my_ip = sock.getsockname()[0]
                    send_packet(sock, self.priority, self.last_poll,
                                self.others, self.pdns)
                    message = recv_packet(sock)
                    sock.close()
                    new_heartbeats = message.pop('known_others')
                    new_heartbeats.pop(my_ip)
                    for n in new_heartbeats:
                        auto_add_heartbeat[n] = new_heartbeats[n]
                    #new_pdns = message.pop('known_pdns')
                    #for n in new_pdns:
                    #    auto_add_pdns[n['ip']] = n
                    self.others[message['ip']] = message
                except Exception as e:
                    #print traceback.format_exc()
                    old_p = self.others[s]['priority']
                    self.others[s]['priority'] = 'D'
                    self.others[s]['ip'] = s
                    if old_p != 'D':
                        print "Failed to communicate with %s, marking it " \
                                  "as down." % (s,)
                    if self.priority.value != 'A' and old_p == 'M':
                        print "Old master dropped, autonegotiating..."
                        self.priority.value = 'A'
                        self.auto_negotiate()
                        return

            if self.priority.value == 'A':
                if len(self.others) > 0:
                    if reduce(
                            lambda x, y: x or self.others[y]['priority'] == "M",
                            self.others, False):
                        print "Master already taken, becoming a slave."
                        self.priority.value = 'S'
                    else:
                        print "No other masters, becoming master."
                        self.priority.value = 'M'
                    print "Servers:"
                    for s in self.others:
                        print "\t%s: %s" % (s, self.others[s]['priority'])
                else:
                    self.priority.value = 'M'
                    print "No other heartbeat servers, becoming master."

            for n in auto_add_heartbeat:
                if n not in self.others:
                    self.others[n] = { 'priority': auto_add_heartbeat[n], 'ip': n }
                    if auto_add_heartbeat[n] == 'M':
                        print "New master joined the pool: %s, reverting to " \
                              "slave mode." % (n,)
                        self.priority.value = 'S'

            #if auto_add_pdns:
            #    with self.pdns.get_lock():
            #        old_pdns = json.loads(self.pdns.value)
            #        for o in old_pdns:
            #            try:
            #                auto_add_pdns.pop(o['ip'])
            #            except:
            #                pass
            #        mode = "NEW" if self.priority.value == 'M' else \
            #            "INCREMENTAL"
            #        for n in auto_add_pdns:
            #            old_pdns.append({'ip': n, 'mode': mode})
            #        #self.pdns.value = json.dumps(old_pdns)
            #        self.pdns.value = json.dumps({'ip':"1.1.1.1", 'mode':
            #            "NEW"})
            #        print "HEARTBEAT notset pdns servers to ", self.pdns.value

    def listen(self):
        while self.RUN.value:
            self.server.serve_forever()

    def do_heartbeat(self):
        time.sleep(self.tick_time.value)
        status = "<-- HEARTBEAT --> [ "
        for k in self.others:
            status += k + " (" + self.others[k]['priority'] + "), "
        status = status[:status.rfind(",")] + ' ]'
        print status#, self.pdns.value
        self.auto_negotiate()

    def stop_heartbeat(self):
        self.server.shutdown()

class HeartbeatRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        message = recv_packet(self.request)

        if type in message and message['type'].upper() == "PDNS":
            #mode = "NEW" if self.priority.value == "M" else "INCREMENTAL"
            #with self.server.pdns.get_lock():
            #    pdns = json.loads(self.server.pdns.value)
            #    pdns.append({"ip": self.request.getpeername()[0],
            #                 "mode": mode })
            #    self.server.pdns.value = json.dumps(pdns)
            return

        if message['ip'] not in self.server.others:
            if message['priority'] == "M":
                self.server.priority.value = "S"
                print "New master joined the pool: %s, reverting to slave " \
                      "mode." % (message['ip'],)
            else:
                print "New server joined the pool: %s" % (message['ip'],)
        elif self.server.others[message['ip']]['priority'] == 'D':
            print "Offline server rejoined the pool: %s" % (message['ip'],)
        message.pop('known_others')
        self.server.others[message['ip']] = message
        send_packet(self.request, self.server.priority, self.server.last_poll,
                    self.server.others, self.server.pdns)
        #print "Received Heartbeat from %s." % (self.client_address[0],)
        return

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, priority, others,
                 pdns, last_poll):
        self.priority = priority
        self.others = others
        self.pdns = pdns
        self.last_poll = last_poll
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)

def send_packet(socket, priority, poll, others, pdns):
    others_list = {}
    #pdns_list = []
    for o in others:
        #print socket.getpeername(), others[o]
        others_list[others[o]['ip']] = others[o]['priority']
    #for p in json.loads(pdns.value):
    #    pdns_list.append(p['ip'])
    packet = {  'ip': socket.getsockname()[0],
                'priority': priority.value,
                'last_poll': poll.value,
                'known_others': others_list }
                #'known_pdns': json.loads(pdns.value) }
    socket.sendall(json.dumps(packet)+"EOT")

def recv_packet(socket):
    message = ""
    while 1:
        data = socket.recv(2048)
        message += data
        if message.strip().endswith('EOT'):
            jm = json.loads(message.rstrip('EOT'))
            #print "Received: ", jm
            return jm
