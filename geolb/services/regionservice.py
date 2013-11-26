from geolb.services.base import BaseService
from geolb.models.persistence import region


class RegionsService(BaseService):

	def get_all(self):
		#Logical validation and other operations
		regions = self.regionpersistence.rsp.get_all()
		return regions

	def create(self, regions_json):
		#Logical validation and other operations
		if regions_json is not None:
			for rj in regions_json:
				r = region.RegionModel(name=rj.get('name'),
					code=rj.get('code'), description=rj.get('description'))
				r = self.regionpersistence.rsp.create(r)
		return r


class RegionService(BaseService):

	def get(self, region_id):
		#Logical validation and other operations
		region = self.regionpersistence.rp.get(region_id)
		return region

	def update(self, region_id, region_json):
		#Logical validation and other operations
		r = self.regionpersistence.rp.get(region_id)
		if region_json.get('name') is not None:
			r.name = region_json.get('name')
		if region_json.get('code') is not None:
			r.code = region_json.get('code')
		if region_json.get('description') is not None:
			r.description = region_json.get('description')
		r = self.regionpersistence.rp.update(region_id, r)
		return r

	def delete(self, region_id):
		#Logical validation and other operations
		g = self.regionpersistence.rp.delete(region_id)
		return g


class RegionServiceOps(object):
	def __init__(self):
		self.rs = RegionsService()
		self.r = RegionService()