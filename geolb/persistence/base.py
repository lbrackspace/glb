from geolb.models.persistence import nameservers, glbstatus, glbstatus_enum, nodestatus, node, base, algorithm, monitor, glb, region


class BaseService(object):
	def __init__(self, operations):
		glb.GlobalLoadbalancerModel.query = base.db.session.query_property()
		node.NodeModel.query = base.db.session.query_property()
		monitor.MonitorModel.query = base.db.session.query_property()
		algorithm.AlgorithmModel.query = base.db.session.query_property()
		glbstatus.GlbStatusModel.query = base.db.session.query_property()
                glbstatus_enum.GlbStatusEnumModel.query = base.db.session.query_property()
		nodestatus.NodeStatusModel.query = base.db.session.query_property()
		nameservers.NameserverModel.query = base.db.session.query_property()
		region.RegionModel.query = base.db.session.query_property()
