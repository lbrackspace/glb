from geolb.services.base import BaseService
from geolb.models.persistence import glb, node, monitor


class GlobalLoadbalancersService(BaseService):
	def get_all(self, account_id):
		#Logical validation and other operations
		glbs = self.glbpersistence.gsp.get_all(account_id)
		return glbs

	def create(self, account_id, glb_json):
		#Logical validation and other operations
		nodes_json = glb_json.get('nodes')
		nlist = []
		if nodes_json is not None:
			for n in nodes_json:
				m = n.get('monitor')
				mm = monitor.MonitorModel(
					interval=m.get('interval'), threshold=m.get('threshold'))
				nm = node.NodeModel(
					ip_address=n.get('ip_address'), type=n.get('type'),
					ip_type=n.get('ip_type'), monitor=mm)
				nlist.append(nm)

		glbm = glb.GlobalLoadbalancerModel(
				account_id=account_id, name=glb_json.get('name'),
				algorithm=glb_json.get('algorithm'), nodes=nlist)
		g = self.glbpersistence.gsp.create(account_id, glbm)
		return g


class GlobalLoadbalancerService(BaseService):

	def get(self, account_id, id):
		#Logical validation and other operations
		glbs = self.glbpersistence.gp.get(id)
		return glbs

	def update(self, account_id, glb_id, glb_json):
		#Logical validation and other operations
		##temp...
		g = self.glbpersistence.gp.get(glb_id)
		if glb_json.get('name') is not None:
			g.name = glb_json.get('name')
		if glb_json.get('algorithm') is not None:
			g.algorithm = glb_json.get('algorithm')
		g = self.glbpersistence.gp.update(g)
		return g

	def delete(self, account_id, glb_id):
		#Logical validation and other operations
		g = self.glbpersistence.gp.delete(glb_id)
		#delete nodes, monitors etc...
		return g


class GlbServiceOps(object):
	def __init__(self):
		self.gs = GlobalLoadbalancersService()
		self.g = GlobalLoadbalancerService()