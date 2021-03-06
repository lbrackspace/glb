from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from manager.models import base, region

#its own class?
nodes_regions = Table('node_region', base.Base.metadata,
                      Column('node_id', Integer, ForeignKey('node.id')),
                      Column('region_id', Integer,
                             ForeignKey('enum_node_region.id'))
)


class NodeModel(base.Base, base.BaseModel):
    __tablename__ = 'node'
    __table_args__ = {"useexisting": True}

    TAG = 'node'

    id_ = Column('id', Integer, primary_key=True)
    ip_address = Column(String(32))
    type = Column(String(32))
    ip_type = Column(String(32))
    weight = Column(Integer(11))
    status = Column(String(128))
    glb_id = Column(Integer, ForeignKey('glb.id'))
    regions = relationship("RegionModel", secondary=nodes_regions)

    def __init__(self, ip_address=None, type=None, ip_type=None,
                 weight=None, status=None, glb_id=None,
                 regions=[]):
        self.ip_address = ip_address
        self.type = type
        self.ip_type = ip_type
        self.weight = weight
        self.status = status
        self.glb_id = glb_id
        self.regions = regions

    def to_dict(self):
        regions_dict = [item.to_dict() for item in self.regions
                        if item is not None]

        node_dict = {'id': self.id_, 'ip_address': self.ip_address,
                     'type': self.type, 'ip_type': self.ip_type,
                     'weight': self.weight, 'status': self.status,
                     'regions': regions_dict}
        return node_dict

    def __repr__(self):
        return '<Node %r>' % self.ip_address
