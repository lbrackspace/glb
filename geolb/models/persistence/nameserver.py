from sqlalchemy import Column, Integer

from geolb.models.persistence import base


class NameserverModel(base.Base, base.BaseModel):
    __tablename__ = 'name_server'
    __table_args__ = {"useexisting": True}

    TAG = 'name_server'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(Integer(32))

    def __init__(self, name=None):
        self.name = name

    def to_dict(self):
        ns_dict = {'id': self.id_, 'name': self.name}
        return ns_dict

    def __repr__(self):
        return '<NameServer %r>' % self.name
