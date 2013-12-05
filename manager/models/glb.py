import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from manager.models import base, dcstats, node


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
    update_type = Column(String(32))
    dc_stats = relationship('DCStatusModel', backref='glb', lazy='dynamic')
    create_time = Column(DateTime(timezone=True))
    update_time = Column(DateTime(timezone=True))
    nodes = relationship('NodeModel', backref='glb', lazy='dynamic',
                         cascade="all,delete")

    def __init__(self, account_id=None, name=None, cname=None, status=None,
                 update_type=None, dc_stats=[], algorithm=None,
                 create_time=None, update_time=None, nodes=[]):
        self.account_id = account_id
        self.name = name
        self.cname = cname
        self.algorithm = algorithm
        self.status = status
        self.update_type = update_type
        self.dc_stats = dc_stats
        if create_time is None:
            self.create_time = datetime.datetime.utcnow()
        else:
            self.create_time = create_time
        if update_time is None:
            self.update_time = datetime.datetime.utcnow()
        else:
            self.update_time = update_time
        self.nodes = nodes

    def to_dict(self):
        dc_stats_dict = [item.to_dict() for item in self.dc_stats
                         if item is not None]

        nodes_dict = [item.to_dict() for item in self.nodes
                      if item is not None]

        glb_dict = {'id': self.id_, 'name': self.name, 'cname': self.cname,
                    'algorithm': self.algorithm,
                    'status': self.status,
                    'update_type': self.update_type,
                    'create_time':
                        self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'update_time':
                        self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'nodes': nodes_dict,
                    'dc_stats': dc_stats_dict}
        return glb_dict

    def __repr__(self):
        return '<GLB %r - %r >' % (self.name, self.cname)
