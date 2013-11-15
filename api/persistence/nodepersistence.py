from api.models import base
from api.persistence.base import BaseService
from api.models import glb, node, monitor, nameservers


class NodesPersistence(BaseService):

    def get_all(self):
        nodes = node.NodeModel.query.all()
        node_list = [n.to_dict() for n in nodes]
        return node_list

    def create(self, account_id, name, algorithm):
        n = {"test":"TEST"}
        return n


class NodePersistence(BaseService):

    def get(self, id):
        n = node.NodeModel.query.filter_by(id_=id).first()
        return n


class NodePersistenceOps(object):
    def __init__(self):
        self.nsp = NodesPersistence(self)
        self.np = NodePersistence(self)
