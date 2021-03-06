from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from geolb.models.persistence import base


class DCStatModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'dc_stat'
    __table_args__ = {"useexisting": True}

    TAG = 'dc_stat'

    id_ = Column('id', Integer, primary_key=True)
    glb_id = Column(Integer, ForeignKey("glb.id"))
    updated = Column(DateTime(timezone=True))
    location = Column(String(16))
    status = Column(String(16))
    response = Column(String(128))

    def __init__(self, glb_id=None, updated=None, location=None, status=None,
                 response=None):
        self.glb_id = glb_id
        self.updated = updated
        self.location = location
        self.status = status
        self.response = response

    def to_dict(self):
        stat_dict = {'id': self.id_, 'glb_id': self.glb_id,
                     'updated': self.updated.strftime("%Y-%m-%d %H:%M:%S"),
                     'location': self.location, 'status': self.status,
                     'response': self.response}
        return stat_dict

    def __repr__(self):
        return '<dc_status %s (%s / %s): %s %s>' % (self.glb_id,
                                                    self.updated.strftime(
                                                        "%Y-%m-%d %H:%M:%S"),
                                                    self.location, self.status,
                                                    self.response)
