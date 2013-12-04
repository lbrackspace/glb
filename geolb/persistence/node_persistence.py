from geolb.models.persistence import base, node, glb
from geolb.persistence.base import BaseService


class NodesPersistence(BaseService):
    def get_all(self, account_id, glb_id):
        nodes = node.NodeModel.query.filter_by(glb_id=glb_id).all()
        return nodes

    def create(self, account_id, glb_id, in_node):
        base.db.session.add(in_node)
        in_node.status = 'ONLINE'
        base.db.session.commit()

        ##Have service method update status...
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=glb_id).first()
        g.status = 'ACTIVE'
        base.db.session.commit()
        return in_node


class NodePersistence(BaseService):
    def get(self, account_id, glb_id, node_id):
        n = node.NodeModel.query.filter_by(id_=node_id).first()
        return n

    def update(self, account_id, glb_id, in_node):
        n = node.NodeModel.query.filter_by(id_=in_node.id_).first()
        #Any other attributes...
        n.ip_address = in_node.ip_address
        n.ip_type = in_node.ip_type
        n.type = in_node.type
        base.db.session.commit()
        return n

    def delete(self, account_id, glb_id, node_id):
        n = node.NodeModel.query.filter_by(id_=node_id).first()
        try:
            base.db.session.delete(n)
            return n
        except:
            print "Delete node %d failed..." % node_id
            raise LookupError


class NodePersistenceOps(object):
    def __init__(self):
        self.np = NodePersistence(self)
        self.nsp = NodesPersistence(self)