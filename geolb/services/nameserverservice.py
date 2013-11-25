from geolb.services.base import BaseService


class NameserversService(BaseService):

    def get_all(self, glb_id):
        #Logical validation and other operations
        nodes = self.na.gsp.get_all(glb_id)
        return nodes

    def create(self, glb_id, node):
        #Logical validation and other operations
        n = self.nodepersistence.nsp.create(glb_id, node.get('ip_address'), node.get('type'))
        return n


class NameserverService(BaseService):

    def get(self, account_id, id):
        #Logical validation and other operations
        node = self.nodepersistence.np.get(id)
        return node


class NameserverServiceOps(object):
    def __init__(self):
        self.ns = NameserversService()
        self.n = NameserverService()