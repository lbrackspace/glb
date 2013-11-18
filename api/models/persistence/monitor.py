from sqlalchemy import Column, Integer, ForeignKey

from api.models.persistence import base


class MonitorModel(base.Base, base.BaseModel):
    __tablename__ = 'monitor'
    __table_args__ = {"useexisting": True}

    TAG = 'monitor'

    id_ = Column('id', Integer, primary_key=True)
    interval = Column(Integer(11))
    threshold = Column(Integer(11))
    node_id = Column(Integer, ForeignKey('node.id'))

    def __init__(self, interval=None, threshold=None, node_id=None):
        self.interval = interval
        self.threshold = threshold
        self.node_id = node_id

    def to_dict(self):
        mon_dict = {'id': self.id_, 'interval': self.interval,
                    'threshold': self.threshold}
        return mon_dict

    def __repr__(self):
        return '<Monitor %r>' % self.threshold