import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from multiprocessing import Process, Queue, current_process, Value
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
            config.get('api', 'username'), config.get('api', 'password'),
            config.get('api', 'address'), config.get('api', 'dbname'))
        self.config = config

        ### SQL ###
        self.engine = create_engine(self.sqlDB)
        self.sessionmaker = sessionmaker(bind=self.engine)

        ### SHARED DATA ###
        try:
            self.tick_time = Value('i', int(config.get('manager', 'tick_time')))
        except:
            self.tick_time = Value('i', 5)
        try:
            self.priority = Value('c', config.get('manager', 'priority', 0,
                                {'master': 'M', 'slave': 'S', 'auto': 'A'}))
        except:
            self.priority = Value('c', 'A')
        try:
            self.last_poll_time = Value(c_char_p, config.get('manager',
                                        'last_poll_time'))
        except:
            self.last_poll_time = Value(c_char_p, "2013-01-01 00:00:00")

        self.response_queue = Queue()
        self.RUN = Value(c_bool, True)

        ### PROCESSES ###
        self.heartbeat = Process(target=self.start_heartbeat,
                            args=(self.priority, self.tick_time, self.RUN))
        self.worker =    Process(target=self.start_worker, 
                            args=(self.priority, self.sessionmaker(),
                                self.response_queue, self.tick_time, 
                                self.last_poll_time, self.config, self.RUN))
        self.responder = Process(target=self.start_responder, 
                            args=(self.priority, self.sessionmaker(),
                                self.response_queue, self.tick_time, self.RUN))


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

    def start_heartbeat(self, priority, tick, RUN):
        heartbeat = HeartbeatProcess(priority, tick, RUN)
        heartbeat.run()

    def start_worker(self, priority, session, response_queue, tick,
                    last_poll_time, config, RUN):
        worker = WorkerProcess(priority, session, response_queue, tick,
                        last_poll_time, config, RUN)
        worker.run()

    def start_responder(self, priority, session, response_queue, tick, RUN):
        responder = ResponderProcess(priority, session, response_queue, 
                        tick, RUN)
        responder.run()

    ### Testing DB ###
    def get_glbs(self, time):
        session = self.sessionmaker()
        glbs = session.query(GlobalLoadbalancerModel).\
                    filter(GlobalLoadbalancerModel.update_time >= time).all()
        return glbs

