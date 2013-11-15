from api.models import base, glb, node, monitor, algorithm, status, nameservers


class BaseService(object):
    def __init__(self, operations):
        glb.GlobalLoadbalancerModel.query = base.db.session.query_property()
        node.NodeModel.query = base.db.session.query_property()
        monitor.MonitorModel.query = base.db.session.query_property()
        algorithm.AlgorithmModel.query = base.db.session.query_property()
        status.StatusModel.query = base.db.session.query_property()
        nameservers.NameserverModel.query = base.db.session.query_property()
