from geolb.models.persistence import nameserver, dcstats, glbstatus_enum, \
	nodestatus_enum, node, base, algorithm, monitor, glb, region, \
	dclocation_enum


class BaseService(object):
	def __init__(self, operations):
		glb.GlobalLoadbalancerModel.query = base.db.session.query_property()
		node.NodeModel.query = base.db.session.query_property()
		monitor.MonitorModel.query = base.db.session.query_property()
		algorithm.AlgorithmModel.query = base.db.session.query_property()
		dcstats.DCStatModel.query = base.db.session.query_property()
		glbstatus_enum.GlbStatusEnumModel.query = base.db.session.query_property()
		nodestatus_enum.NodeStatusModel.query = base.db.session.query_property()
		nameserver.NameserverModel.query = base.db.session.query_property()
		region.RegionModel.query = base.db.session.query_property()
		dclocation_enum.DCLocationModel.query = base.db.session.query_property()