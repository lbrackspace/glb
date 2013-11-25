from geolb.models.persistence import base, monitor
from geolb.persistence.base import BaseService


class MonitorPersistence(BaseService):

    def get(self, id):
        m = monitor.MonitorModel.query.filter_by(id_=id).first()
        return m

    def create(self, node_id, interval, threshold):
        m = monitor.MonitorModel(node_id=node_id, interval=interval, threshold=threshold)

        base.db.session.add(m)
        base.db.session.commit()
        return m


class MonitorPersistenceOps(object):
    def __init__(self):
        self.mp = MonitorPersistence(self)