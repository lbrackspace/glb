from flask.ext.restful import Resource
from geolb.persistence.glb_persistence import GlbPersistenceOps
from geolb.persistence.node_persistence import NodePersistenceOps
from geolb.persistence.monitor_persistence import MonitorPersistenceOps
from geolb.persistence.nameservers_persistence import NameserverPersistenceOps
from geolb.persistence.regions_persistence import RegionPersistenceOps
from geolb.persistence.dcstats_persistence import DCStatsPersistenceOps


class BaseService(Resource):
    def __init__(self):
        self.glbpersistence = GlbPersistenceOps()
        self.nodepersistence = NodePersistenceOps()
        self.monitorpersistence = MonitorPersistenceOps()
        self.nameserverservice = NameserverPersistenceOps()
        self.regionpersistence = RegionPersistenceOps()
        self.dcstatspersistence = DCStatsPersistenceOps()