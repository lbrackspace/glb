from geolb.models.persistence import base, node
from geolb.persistence.base import BaseService


class NodesPersistence(BaseService):

    def get_all(self):
        nodes = node.NodeModel.query.all()
        node_list = [n.to_dict() for n in nodes]
        return node_list

    def create(self, glb_id, ip_address, type):
        n = node.NodeModel(glb_id=glb_id, ip_address=ip_address, type=type)

        base.db.session.add(n)
        base.db.session.commit()
        return n


class NodePersistence(BaseService):

    def get(self, id):
        n = node.NodeModel.query.filter_by(id_=id).first()
        return n


class NodePersistenceOps(object):
    def __init__(self):
        self.nsp = NodesPersistence(self)
        self.np = NodePersistence(self)
