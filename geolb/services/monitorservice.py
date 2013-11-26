from geolb.services.base import BaseService


class MonitorService(BaseService):
	#Should we follow convention and use mon_id instead.
	# Only one monitor per node, no sense in making user find the id for it :/
	def get(self, account_id, glb_id, node_id):
		#Logical validation and other operations
		monitor = self.monitorpersistence.mp.get(account_id, glb_id, node_id)
		return monitor

	def create(self, account_id, glb_id, node_id, mon_json):
		##POST should be a method not allowed, should only be able to update
		#an existing monitor on the node specified.
		#Logical validation and other operations
		m = self.monitorpersistence.mp.create(account_id, glb_id, node_id,
		                                      mon_json.get('interval'),
		                                      mon_json.get('threshold'))
		return m

	def update(self, account_id, glb_id, node_id, mon_json):
		mon = self.monitorpersistence.mp.get(account_id, glb_id, node_id)
		if mon_json.get('interval') is not None:
			mon.interval = mon_json.get('interval')
		if mon_json.get('threshold') is not None:
			mon.threshold = mon_json.get('threshold')
		mon = self.monitorpersistence.mp.update(account_id, glb_id, node_id, mon)
		return mon

	def delete(self, account_id, glb_id, node_id):
		#Logical validation and other operations
		m = self.monitorpersistence.mp.delete(node_id)
		#delete nodes, monitors etc...
		return m


	class MonitorServiceOps(object):
		def __init__(self):
			self.m = MonitorService()