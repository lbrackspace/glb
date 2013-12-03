import json
import time
import signal
import threading
import SocketServer
import socket
import subprocess

class HeartbeatProcess():
    def __init__(self, port, others, priority, tick, last_poll, RUN):
        self.port = port
        self.priority = priority
        self.tick_time = tick
        self.last_poll = last_poll
        self.RUN = RUN
        self.others = others
        p = subprocess.Popen('hostname', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        hostname, errors = p.communicate()
        self.server = SimpleServer((hostname.strip(), self.port), 
                        HeartbeatRequestHandler, self.priority, self.others, self.last_poll)
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
            if self.priority.value != 'A':
                for s in self.others.keys():
                    try:
                        sock = socket.create_connection((s, self.port), 5)
                        send_packet(sock, self.priority, self.last_poll)
                        message = recv_packet(sock)
                        sock.close()
                        self.others[message['ip']] = message
                    except:
                        #server = self.others.pop(s)
                        old_p = self.others[s]['priority']
                        self.others[s]['priority'] = 'D'
                        if old_p != 'D':
                            print "Failed to communicate with %s, discarding it." % (s,)
                        if old_p == 'M':
                            print "Old master dropped, autonegotiating..."
                            self.priority.value = 'A'
                            self.autonegotiate()
            else:
                servers = self.others.keys()
                print "Attempting to autonegotiate server priority with ", servers
                for s in servers:
                    try:
                        sock = socket.create_connection((s, self.port), 5)
                        send_packet(sock, self.priority, self.last_poll)
                        message = recv_packet(sock)
                        sock.close()
                        self.others[message['ip']] = message
                    except:
                        print "Failed to communicate with %s, discarding it." % (s,)
                        #self.others.pop(s)
                        self.others[s]['priority'] = 'D'
                if len(self.others) > 0:
                    if reduce(lambda x, y: x or self.others[y]['priority']=="M", self.others, False):
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

    def listen(self):
        while self.RUN.value:
            self.server.serve_forever()

    def do_heartbeat(self):
        time.sleep(self.tick_time.value)
        status = "<-- HEARTBEAT --> [ "
        for k in self.others.keys():
            status += k + " (" + self.others[k]['priority'] + "), "
        status = status[:-2] + ' ]'
        print status
        self.autonegotiate()
           
    def stop_heartbeat(self):
        self.server.shutdown()

class HeartbeatRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        message = recv_packet(self.request)
        if not self.server.others.has_key(message['ip']) or self.server.others[message['ip']]['priority'] == 'D':
            print "New server joined the pool: %s" % (message['ip'],)
        self.server.others[message['ip']] = message
        send_packet(self.request, self.server.priority, self.server.last_poll)
        #print "Received Heartbeat from %s." % (self.client_address[0],)
        return

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, priority, others, last_poll):
        self.priority = priority
        self.others = others
        self.last_poll = last_poll
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def send_packet(socket, priority, poll):
    packet = {  'ip': socket.getsockname()[0],
                'priority': priority.value, 
                'last_poll': poll.value }
    socket.send(json.dumps(packet)+"EOT")

def recv_packet(socket):
    message = ""
    while 1:
        data = socket.recv(1024)
        message += data
        if message.strip().endswith('EOT'):
            jm = json.loads(message.rstrip('EOT'))
            #print "Received: ", jm
            return jm
