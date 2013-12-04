from geolb.models.persistence import base, monitor
from geolb.persistence.base import BaseService


class MonitorPersistence(BaseService):
    def get(self, account_id, glb_id, node_id):
        m = monitor.MonitorModel.query.filter_by(node_id=node_id).first()
        return m

    def create(self, account_id, glb_id, node_id, interval, threshold):
        m = monitor.MonitorModel(node_id=node_id, interval=interval,
                                 threshold=threshold)
        base.db.session.add(m)
        base.db.session.commit()
        return m

    def delete(self, account_id, glb_id, node_id):
        m = monitor.MonitorModel.query.filter_by(node_id=node_id).first()
        try:
            base.db.session.delete(m)
            #g.status = 'DELETED'
            base.db.session.commit()
            return m
        except:
            print "Delete glb %d failed..." % glb_id
            raise LookupError


class MonitorPersistenceOps(object):
    def __init__(self):
        self.mp = MonitorPersistence(self)