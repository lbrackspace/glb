from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from api.models.persistence import base


class NodeModel(base.Base, base.BaseModel):
    __tablename__ = 'node'
    __table_args__ = {"useexisting": True}

    TAG = 'node'

    id_ = Column('id', Integer, primary_key=True)
    ip_address = Column(String(32))
    type = Column(String(32))
    status = Column(String(128))
    glb_id = Column(Integer, ForeignKey('glb.id'))
    monitor = relationship("MonitorModel", uselist=False, backref="node")

    def __init__(self, ip_address=None, type=None, status=None, glb_id=None, monitor=None):
        self.ip_address = ip_address
        self.type = type
        self.status = status
        self.glb_id = glb_id
        self.monitor = monitor

    def to_dict(self):
        node_dict = {'id': self.id_, 'ip_address': self.ip_address,
                     'type': self.type, 'status': self.status,
                     'glb_id': self.glb_id,
                     'monitor': self.monitor.to_dict()}
        return node_dict

    def __repr__(self):
        return '<Node %r>' % self.ip_address