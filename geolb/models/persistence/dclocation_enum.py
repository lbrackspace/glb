from sqlalchemy import Column, Integer, String

from geolb.models.persistence import base


class DCLocationModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'enum_dc_location'
    __table_args__ = {"useexisting": True}

    TAG = 'enum_dc_location'

    name = Column(String(32), primary_key=True)
    description = Column(String(128))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def to_dict(self):
        stat_dict = {'name': self.name,
                     'description': self.description}
        return stat_dict

    def __repr__(self):
        return '<DCLocation %r>' % self.name
