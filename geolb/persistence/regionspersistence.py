from geolb.models.persistence import base, node, glb, region
from geolb.persistence.base import BaseService


class RegionsPersistence(BaseService):
	def get_all(self):
		regions = region.RegionModel.query.all()
		return regions

	def create(self, region_id, in_region):
		base.db.session.add(in_region)
		base.db.session.commit()

		base.db.session.commit()
		return in_region


class RegionPersistence(BaseService):

	def get(self, region_id):
		r = region.RegionModel.query.filter_by(id_=region_id).first()
		return r

	def update(self, region_id, in_region):
		r = region.RegionModel.query.filter_by(id_=region_id).first()
		#Any other attributes...
		r.ip_address = in_region.ip_address
		r.ip_type = in_region.ip_type
		r.type = in_region.type
		base.db.session.commit()
		return r

	def delete(self, account_id, glb_id, node_id):
		n = node.NodeModel.query.filter_by(id_=node_id).first()
		try:
			base.db.session.delete(n)
			return n
		except:
			print "Delete node %d failed..." % node_id
			raise LookupError


class RegionPersistenceOps(object):
	def __init__(self):
		self.rsp = RegionsPersistence(self)
		self.rp = RegionPersistence(self)