from geolb.models.persistence import nameserver, dcstats, glbstatus_enum, nodestatus, node, base, algorithm, monitor, glb, region


class BaseService(object):
	def __init__(self, operations):
		glb.GlobalLoadbalancerModel.query = base.db.session.query_property()
		node.NodeModel.query = base.db.session.query_property()
		monitor.MonitorModel.query = base.db.session.query_property()
		algorithm.AlgorithmModel.query = base.db.session.query_property()
		dcstats.DCStatusModel.query = base.db.session.query_property()
                glbstatus_enum.GlbStatusEnumModel.query = base.db.session.query_property()
		nodestatus.NodeStatusModel.query = base.db.session.query_property()
		nameserver.NameserverModel.query = base.db.session.query_property()
		region.RegionModel.query = base.db.session.query_property()
