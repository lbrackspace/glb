from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from api.models.persistence import base


class GlobalLoadbalancerModel(base.Base, base.BaseModel):
    __tablename__ = 'glb'
    __table_args__ = {"useexisting": True}

    TAG = 'glb'

    id_ = Column('id', Integer, primary_key=True)
    account_id = Column(Integer(32))
    name = Column(String(128))
    cname = Column(String(128))
    algorithm = Column(String(32))
    status = Column(String(32))
    create_time = Column(DateTime(timezone=True))
    update_time = Column(DateTime(timezone=True))
    nodes = relationship('NodeModel', backref='glb', lazy='dynamic', cascade="all,delete")
    name_servers = []

    def __init__(self, account_id=None, name=None, cname=None, status=None,
                 algorithm=None, create_time=None, update_time=None, nodes=[], name_servers=[]):
        self.account_id = account_id
        self.name = name
        self.cname = cname
        self.status = status
        self.algorithm = algorithm
        if create_time is None:
            self.create_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.create_time = create_time
        if update_time is None:
            self.update_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.update_time = update_time
        self.nodes = nodes
        self.name_servers = name_servers

    def to_dict(self):
        ns_dict = [item.to_dict() for item in self.name_servers
                      if item is not None]

        nodes_dict = [item.to_dict() for item in self.nodes
                      if item is not None]

        glb_dict = {'id': self.id_, 'name': self.name, 'cname': self.cname,
                    'algorithm': self.algorithm, 'status': self.status,
                    #'create_time': self.create_time, 'update_time': self.update_time,
                    'nodes': nodes_dict, 'name_servers': ns_dict}
        return glb_dict

    def __repr__(self):
        return '<GLB %r>' % self.name