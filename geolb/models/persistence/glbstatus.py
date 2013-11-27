from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from geolb.models.persistence import base


class GlbStatusModel(base.Base, base.BaseModel):
    #This model may not be needed
    __tablename__ = 'glb.status'
    __table_args__ = {"useexisting": True}

    TAG = 'glb.status'

    id_ = Column('id', Integer, primary_key=True)
    glb_id = Column(Integer, ForeignKey("glb.id"))
    time = Column(DateTime(timezone=True))
    location = Column(String(16))
    status = Column(String(16))

    def __init__(self, glb_id=None, time=None, location=None, status=None):
        self.glb_id = glb_id
        self.time = time
        self.location = location
        self.status = status

    def to_dict(self):
        stat_dict = {'id': self.id_, 'glb_id': self.glb_id,'time': self.time, 
                        'location': self.location, 'status': self.status}
        return stat_dict

    def __repr__(self):
        return '<GlbStatus %d (%s / %s): %s>' % (self.glb_id,
                        self.time, self.location, self.status)
