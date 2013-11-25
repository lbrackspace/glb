from sqlalchemy import Column, Integer, String

from geolb.models.persistence import base


class RegionModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'regions'
    __table_args__ = {"useexisting": True}

    TAG = 'glb_status'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(32))
    code = Column(String(32))
    description = Column(String(128))

    def __init__(self, name=None, code=None, description=None):
        self.name = name
        self.code = code
        self.description = description

    def to_dict(self):
        stat_dict = {'id': self.id_, 'name': self.name,
                     'code': self.code, 'description': self.description}
        return stat_dict

    def __repr__(self):
        return '<Algorithm %r>' % self.name