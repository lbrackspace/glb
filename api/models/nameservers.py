import base
from sqlalchemy import Table, Column, Integer, ForeignKey, String


class NameserverModel(base.Base, base.BaseModel):
    __tablename__ = 'name_server'
    __table_args__ = {"useexisting": True}

    TAG = 'name_server'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(Integer(32))
    node_id = Column(Integer, ForeignKey('node.id'))

    def __init__(self, name=None, node_id=None):
        self.name = name
        self.node_id = node_id

    def to_dict(self):
        ns_dict = {'id': self.id_, 'name': self.name, 'node_id': self.node_id}
        return ns_dict

    def __repr__(self):
        return '<Monitor %r>' % self.threshold