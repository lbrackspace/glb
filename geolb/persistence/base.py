from geolb.models.persistence import nameservers, status, node, base, algorithm, monitor, glb


class BaseService(object):
    def __init__(self, operations):
        glb.GlobalLoadbalancerModel.query = base.db.session.query_property()
        node.NodeModel.query = base.db.session.query_property()
        monitor.MonitorModel.query = base.db.session.query_property()
        algorithm.AlgorithmModel.query = base.db.session.query_property()
        status.StatusModel.query = base.db.session.query_property()
        nameservers.NameserverModel.query = base.db.session.query_property()
