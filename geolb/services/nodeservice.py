from geolb.services.base import BaseService
from geolb.models.persistence import glb, node, monitor, region


class NodesService(BaseService):
    def get_all(self, account_id, glb_id):
        #Logical validation and other operations
        nodes = self.nodepersistence.nsp.get_all(account_id, glb_id)
        return nodes

    def create(self, account_id, glb_id, nodes_json):
        #Logical validation and other operations
        if nodes_json is not None:
            nlist = []
            for n in nodes_json:
                m = n.get('monitor')
                mm = monitor.MonitorModel(
                    interval=m.get('interval'), threshold=m.get('threshold'))

                #tmp
                regions = [region.RegionModel(id_=1)]
                regions_json = n.get('regions')
                for r in regions_json:
                    rr = region.RegionModel(id_=r.get('id'))
                    regions.append(rr)

                #Weight defaults to 1
                weight = n.get('weight') if n.get('weight') is not None else 1
                nm = node.NodeModel(glb_id=glb_id,
                                    ip_address=n.get('ip_address'),
                                    type=n.get('type'),
                                    ip_type=n.get('ip_type'), monitor=mm,
                                    weight=weight, regions=regions)
                nlist.append(nm)

            g = self.nodepersistence.nsp.create(account_id, glb_id, nm)
        return g


class NodeService(BaseService):
    def get(self, account_id, glb_id, node_id):
        #Logical validation and other operations
        node = self.nodepersistence.np.get(account_id, glb_id, node_id)
        return node

    def update(self, account_id, glb_id, node_id, node_json):
        #Logical validation and other operations
        n = self.nodepersistence.np.get(node_id)
        if node_json.get('ip_address') is not None:
            n.ip_address = node_json.get('ip_address')
        if node_json.get('ip_type') is not None:
            n.ip_type = node_json.get('ip_type')
        if node_json.get('type') is not None:
            n.type = node_json.get('type')
        n = self.nodepersistence.np.update(account_id, glb_id, n)
        return n

    def delete(self, account_id, glb_id, node_id):
        #Logical validation and other operations
        g = self.nodepersistence.np.delete(account_id, glb_id, node_id)
        #delete monitors etc...
        return g


class NodeServiceOps(object):
    def __init__(self):
        self.ns = NodesService()
        self.n = NodeService()