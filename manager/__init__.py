import ConfigParser
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from multiprocessing import Process, Queue, Array, Value
from ctypes import c_bool, c_char_p

from manager.models.glb import GlobalLoadbalancerModel
from manager.processes.heartbeat import HeartbeatProcess
from manager.processes.worker import WorkerProcess
from manager.processes.responder import ResponderProcess

filename = 'config.cfg'


class Manager():
    def __init__(self):
        ### CONFIGURATION ###
        config = ConfigParser.SafeConfigParser()
        config.read([filename])
        self.sqlDB = 'mysql://%s:%s@%s/%s' % (
            config.get('manager', 'username'),
            config.get('manager', 'password'),
            config.get('manager', 'address'),
            config.get('manager', 'dbname'))
        self.config = config

        ### SQL ###
        self.engine = create_engine(self.sqlDB)
        self.sessionmaker = sessionmaker(bind=self.engine)

        ### SHARED DATA ###
        try:
            self.tick_time = Value('i', config.getint('manager', 'tick_time'))
        except:
            self.tick_time = Value('i', 5)
        try:
            self.priority = Value('c', config.get('manager', 'priority', 0,
                                                  {'master': 'M', 'slave': 'S',
                                                   'auto': 'A'}))
        except:
            self.priority = Value('c', 'A')
        try:
            self.last_poll_time = Value(c_char_p, config.get('manager',
                                                             'last_poll_time'))
        except:
            self.last_poll_time = Value(c_char_p, "2013-01-01 00:00:00")
        try:
            self.other_servers = {}
            servers = config.get('manager', 'other_servers')
            for s in servers.split(','):
                self.other_servers[s.strip()] = {'ip': s.strip(),
                                                 'priority': 'D'}
        except:
            pass
        try:
            self.port = config.getint('manager', 'port')
        except:
            self.port = 5050
        try:
            self.location = config.get('manager', 'location')
        except:
            self.location = "DEFAULT"
        self.api_node = {'host': config.get('manager', 'api_node'),
                         'auth': config.get('manager', 'api_auth'),
                         'path': config.get('manager', 'api_bulk')}
        try:
            self.pdns_port = config.getint('manager', 'pdns_port')
        except:
            self.pdns_port = 8888
        try:
            pdns_servers_raw = config.get('manager', 'pdns_servers'). \
                replace(" ", "").split(',')
            pdns_servers = []
            for server in pdns_servers_raw:
                pdns_servers.append({"ip":server.strip(), "mode":"NEW"})
        except:
            pdns_servers = []
        self.pdns_servers = Value(c_char_p, json.dumps(pdns_servers))

        self.response_queue = Queue()
        self.RUN = Value(c_bool, True)

        ### PROCESSES ###
        self.heartbeat = Process(target=self.start_heartbeat,
                                 args=(
                                     self.port, self.other_servers,
                                     self.pdns_servers, self.priority,
                                     self.tick_time, self.last_poll_time, self.RUN))
        self.worker = Process(target=self.start_worker,
                              args=(self.priority, self.sessionmaker,
                                    self.pdns_servers, self.pdns_port,
                                    self.response_queue, self.tick_time,
                                    self.last_poll_time, self.config, self.RUN))
        self.responder = Process(target=self.start_responder,
                                 args=(self.priority,
                                       self.response_queue, self.location,
                                       self.api_node, self.tick_time, self.RUN))


    def start_working(self):
        self.RUN.value = True
        self.heartbeat.start()
        self.worker.start()
        self.responder.start()

        while 1:
            try:
                self.heartbeat.join()
                self.worker.join()
                self.responder.join()
                break
            except KeyboardInterrupt:
                print "\nStopping..."
                self.stop_working()

        print "Done."

    def stop_working(self):
        self.RUN.value = False

    def start_heartbeat(self, port, other_servers, pdns_servers, priority,
                        tick, last_poll, RUN):
        heartbeat = HeartbeatProcess(port, other_servers, pdns_servers,
                                     priority, tick, last_poll, RUN)
        try:
            heartbeat.run()
        except:
            heartbeat.stop_heartbeat()

    def start_worker(self, priority, sessionmaker, pdns_servers, pdns_port,
                     response_queue, tick, last_poll_time, config, RUN):
        worker = WorkerProcess(priority, sessionmaker, pdns_servers, pdns_port,
                            response_queue, tick, last_poll_time, config, RUN)
        worker.run()

    def start_responder(self, priority, response_queue, location, api_node,
                        tick, RUN):
        responder = ResponderProcess(priority, response_queue,
                                     location, api_node, tick, RUN)
        responder.run()

    ### Testing DB ###
    def get_glbs(self, time):
        session = self.sessionmaker()
        glbs = session.query(GlobalLoadbalancerModel). \
            filter(GlobalLoadbalancerModel.update_time >= time).all()
        return glbs

