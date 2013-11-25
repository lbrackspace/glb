from geolb.services.base import BaseService


class NodesService(BaseService):

    def get_all(self, glb_id):
        #Logical validation and other operations
        nodes = self.nodepersistence.gsp.get_all(glb_id)
        return nodes

    def create(self, glb_id, node):
        #Logical validation and other operations
        n = self.nodepersistence.nsp.create(glb_id, node.get('ip_address'), node.get('type'))
        return n


class NodeService(BaseService):

    def get(self, account_id, id):
        #Logical validation and other operations
        node = self.nodepersistence.np.get(id)
        return node


class NodeServiceOps(object):
    def __init__(self):
        self.ns = NodesService()
        self.n = NodeService()