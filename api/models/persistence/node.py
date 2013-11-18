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
    name_servers=[]

    def __init__(self, ip_address=None, type=None, status=None,
                 glb_id=None, monitor=None, name_servers=[]):
        self.ip_address = ip_address
        self.type = type
        self.status = status
        self.glb_id = glb_id
        self.monitor = monitor
        self.name_servers = name_servers

    def to_dict(self):
        ns_dict = [item.to_dict() for item in self.name_servers
                      if item is not None]
        node_dict = {'id': self.id_, 'ip_address': self.ip_address,
                     'type': self.type, 'status': self.status,
                     'monitor': self.monitor.to_dict(), 'name_servers': ns_dict}
        return node_dict

    def __repr__(self):
        return '<Node %r>' % self.ip_address