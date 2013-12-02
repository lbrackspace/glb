from geolb.services.base import BaseService
from geolb.models.persistence import glb, node, monitor, region, dcstats


class GlobalLoadbalancersService(BaseService):
	def get_all(self, account_id):
		#Logical validation and other operations
		glbs = self.glbpersistence.gsp.get_all(account_id)
		return glbs

	def create(self, account_id, glb_json):
		#Logical validation and other operations
		#Call other services to do validation of child objects or do
		#All validation for 'one' call in the same place..
		nodes_json = glb_json.get('nodes')
		nlist = []
		if nodes_json is not None:
			for n in nodes_json:
				m = n.get('monitor')
				mm = monitor.MonitorModel(interval=m.get('interval'),
				                          threshold=m.get('threshold'))

				#tmp, working on region relations
				regions_json = n.get('regions')
				regions = []
				#:/
				if glb_json.get('algorithm') is 'GEOIP':
					if regions_json is not None:
						regs = self.regionpersistence.rsp.get_all()
						if regs is not None:
							for rj in regions_json:
								for r in regs:
									if rj.get('name') == r.name:
										regions.append(r)
					else:
						careg = self.regionpersistence.rp.get(1)
						regions.append(careg)
				if regions_json is not None:
					##need to handle validation ..
					pass

				#Weight defaults to 1
				weight = n.get('weight') if n.get('weight') is not None else 1
				nm = node.NodeModel(ip_address=n.get('ip_address'),
				                    type=n.get('type'),
				                    ip_type=n.get('ip_type'),
				                    monitor=mm, weight=weight, regions=regions)
				nlist.append(nm)
		dc_stats = []
		glbm = glb.GlobalLoadbalancerModel(
			account_id=account_id, name=glb_json.get('name'),
			dc_stats=dc_stats, algorithm=glb_json.get('algorithm'),
			nodes=nlist, status='BUILD')

		g = self.glbpersistence.gsp.create(account_id, glbm)

		return g


class GlobalLoadbalancerService(BaseService):
	def get(self, account_id, glb_id):
		#Logical validation and other operations
		glbs = self.glbpersistence.gp.get(account_id, glb_id)
		return glbs

	def update(self, account_id, glb_id, glb_json):
		#Logical validation and other operations
		##temp...
		g = self.glbpersistence.gp.get(account_id, glb_id)
		if glb_json.get('name') is not None:
			g.name = glb_json.get('name')
		if glb_json.get('algorithm') is not None:
			g.algorithm = glb_json.get('algorithm')
		if glb_json.get('dc_stats') is not None:
			statsList = []
			stats = glb_json.get('dc_stats')
			for s in stats:
				statsList.append(dcstats.DCStatusModel(
					location=s.get('location'),
					status=s.get('status')))
			g.dc_stats = statsList


		g = self.glbpersistence.gp.update(account_id, glb_id, g)
		return g

	def delete(self, account_id, glb_id):
		#Logical validation and other operations
		g = self.glbpersistence.gp.delete(account_id, glb_id)
		#delete nodes, monitors etc...
		return g


class GlbServiceOps(object):
	def __init__(self):
		self.gs = GlobalLoadbalancersService()
		self.g = GlobalLoadbalancerService()