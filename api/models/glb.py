import base
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref


class GlobalLoadbalancerModel(base.Base, base.BaseModel):
    __tablename__ = 'glb'
    __table_args__ = {"useexisting": True}

    TAG = 'glb'

    id_ = Column('id', Integer, primary_key=True)
    account_id = Column(Integer(32))
    name = Column(String(128))
    cname = Column(String(128))
    status = Column(String(32))
    algorithm = Column(String(32))
    nodes = relationship('NodeModel', backref='glb', lazy='dynamic', cascade="all,delete")

    def __init__(self, account_id=None, name=None, cname=None, status=None, algorithm=None, nodes=[]):
        self.account_id = account_id
        self.name = name
        self.cname = cname
        self.status = status
        self.algorithm = algorithm
        self.nodes = nodes

    def to_dict(self):
        glb_dict = {'id': self.id_, 'name': self.name, 'cname': self.cname,
                    'status': self.status, 'algorithm': self.algorithm}
        return glb_dict

    def __repr__(self):
        return '<GLB %r>' % self.name