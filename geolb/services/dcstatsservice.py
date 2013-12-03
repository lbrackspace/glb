from geolb.services.base import BaseService
from geolb.models.persistence import glb, node, monitor, region, dcstats


class DCStatsService(BaseService):
	def get_all(self):
		#Will be heavy, needs pagination if this call is needed.
		stats = self.dcstatspersistence.dsp.get_all()
		return stats

	def create(self, stats_json):
		#Logical validation and other operations
		#Call other services to do validation of child objects or do
		#All validation for 'one' call in the same place..

		dc_stats = []
		if stats_json is not None:
			for s in stats_json:
				dc_stats.append(dcstats.DCStatModel(
					location=s.get('location'),status=s.get('status'),
					glb_id=s.get('glb_id')))

		dc_stats = self.dcstatspersistence.dsp.create(dc_stats)
		return dc_stats

	def update(self, stats_json):
		#Batch update..., heavy
		dc_stats = []
		if stats_json is not None:
			for s in stats_json:
				cstat = self.dcstatspersistence.dsp.get(s.get('id'))
				cstat.location = s.get('location')
				cstat.status = s.get('status')
				self.dcstatspersistence.dsp.update()
		return True

class DCStatsServiceOps(object):
	def __init__(self):
		self.ds = DCStatsService()