from flask.ext.restful import Resource
from api.persistence.glbpersistence import GlbPersistenceOps
from api.persistence.nodepersistence import NodePersistenceOps
from api.persistence.monitorpersistence import MonitorPersistenceOps


class BaseService(Resource):

    def __init__(self):
        self.glbpersistence = GlbPersistenceOps()
        self.nodepersistence = NodePersistenceOps()
        self.monitorpersistence = MonitorPersistenceOps()