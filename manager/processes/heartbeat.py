import json
import time
import signal
import threading
import SocketServer
import socket
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
                                   self.others, self.last_poll)
        if len(self.others) == 0:
            self.priority.value = 'M'
        print "Initialized Heartbeat Process."

    def run(self):
        s = signal.signal(signal.SIGINT, signal.SIG_IGN)
        threading.Thread(target=self.listen).start()
        self.autonegotiate()

        while self.RUN.value:
            self.do_heartbeat()
        self.server.shutdown()
        signal.signal(signal.SIGINT, s)

    def autonegotiate(self):
        with self.priority.get_lock():
            auto_add = {}
            if self.priority.value != 'A':
                servers = self.others.keys()
                for s in servers:
                    try:
                        sock = socket.create_connection((s, self.port), 5)
                        myip = sock.getsockname()[0]
                        send_packet(sock, self.priority, self.last_poll,
                                    self.others)
                        message = recv_packet(sock)
                        sock.close()
                        new = message.pop('known_others')
                        new.pop(myip)
                        self.others[message['ip']] = message
                        for n in new.keys():
                            auto_add[n] = new[n]
                    except Exception as e:
                        #print traceback.format_exc()
                        old_p = self.others[s]['priority']
                        self.others[s]['priority'] = 'D'
                        self.others[s]['ip'] = s
                        if old_p != 'D':
                            print "Failed to communicate with %s, discarding " \
                                  "it." % (s,)
                        if old_p == 'M':
                            print "Old master dropped, autonegotiating..."
                            self.priority.value = 'A'
                            self.autonegotiate()
            else:
                servers = self.others.keys()
                print "Attempting to autonegotiate server priority with ", \
                    servers
                for s in servers:
                    try:
                        sock = socket.create_connection((s, self.port), 5)
                        myip = sock.getsockname()[0]
                        send_packet(sock, self.priority, self.last_poll,
                                    self.others)
                        message = recv_packet(sock)
                        sock.close()
                        new = message.pop('known_others')
                        new.pop(myip)
                        self.others[message['ip']] = message
                        for n in new.keys():
                            auto_add[n] = new[n]
                    except Exception as e:
                        #print traceback.format_exc()
                        print "Failed to communicate with %s, discarding it."\
                              % (s,)
                        self.others[s]['priority'] = 'D'
                        self.others[s]['ip'] = s
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
            for n in auto_add.keys():
                if n not in self.others:
                    self.others[n] = { 'priority': auto_add[n], 'ip': n }
                    if auto_add[n] == 'M':
                        print "New master joined the pool: %s, reverting to " \
                              "slave mode." % (n,)
                        self.priority.value = 'S'

    def listen(self):
        while self.RUN.value:
            self.server.serve_forever()

    def do_heartbeat(self):
        time.sleep(self.tick_time.value)
        status = "<-- HEARTBEAT --> [ "
        for k in self.others.keys():
            status += k + " (" + self.others[k]['priority'] + "), "
        status = status[:status.rfind(",")] + ' ]'
        print status
        self.autonegotiate()

    def stop_heartbeat(self):
        self.server.shutdown()

class HeartbeatRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        message = recv_packet(self.request)
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
                    self.server.others)
        #print "Received Heartbeat from %s." % (self.client_address[0],)
        return

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, priority, others,
                 last_poll):
        self.priority = priority
        self.others = others
        self.last_poll = last_poll
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)

def send_packet(socket, priority, poll, others):
    others_list = {}
    for o in others.keys():
        #print socket.getpeername(), others[o]
        others_list[others[o]['ip']] = others[o]['priority']
    packet = {  'ip': socket.getsockname()[0],
                'priority': priority.value,
                'last_poll': poll.value,
                'known_others': others_list }
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
