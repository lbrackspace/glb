from sqlalchemy import Column, Integer, String

from manager.models import base


class RegionModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'enum_node_region'
    __table_args__ = {"useexisting": True}

    TAG = 'enum_node_region'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(32))
    code = Column(String(32))
    description = Column(String(128))

    def __init__(self, id_=None, name=None, code=None, description=None):
        self.id_ = id_
        self.name = name
        self.code = code
        self.description = description

    def to_dict(self):
        stat_dict = {'id': self.id_, 'name': self.name,
                     'code': self.code, 'description': self.description}
        return stat_dict

    def __repr__(self):
        return '<Region %r>' % self.name
