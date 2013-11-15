from api.models import base
from api.persistence.base import BaseService
from api.models import glb, node, monitor, nameservers


class MonitorPersistence(BaseService):

    def get(self, id):
        m = monitor.MonitorModel.query.filter_by(id_=id).first()
        return m

    def create(self, account_id, monitor):
        m = {"test":"TEST"}
        return m


class MonitorPersistenceOps(object):
    def __init__(self):
        self.mp = MonitorPersistence(self)