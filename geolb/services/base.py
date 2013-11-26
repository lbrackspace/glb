from flask.ext.restful import Resource
from geolb.persistence.glbpersistence import GlbPersistenceOps
from geolb.persistence.nodepersistence import NodePersistenceOps
from geolb.persistence.monitorpersistence import MonitorPersistenceOps
from geolb.persistence.nameserverspersistence import NameserverPersistenceOps
from geolb.persistence.regionspersistence import RegionPersistenceOps


class BaseService(Resource):

    def __init__(self):
        self.glbpersistence = GlbPersistenceOps()
        self.nodepersistence = NodePersistenceOps()
        self.monitorpersistence = MonitorPersistenceOps()
        self.nameserverservice = NameserverPersistenceOps()
        self.regionpersistence = RegionPersistenceOps()