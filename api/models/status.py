import base
from sqlalchemy import Table, Column, Integer, ForeignKey, String


class StatusModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'glb_status'
    __table_args__ = {"useexisting": True}

    TAG = 'glb_status'

    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(128))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def to_dict(self):
        stat_dict = {'id': self.id_, 'name': self.name,
                     'description': self.description}
        return stat_dict

    def __repr__(self):
        return '<Algorithm %r>' % self.name