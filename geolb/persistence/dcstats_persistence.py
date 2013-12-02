from geolb.models.persistence import base, dcstats
from geolb.persistence.base import BaseService


class DCStatsPersistence(BaseService):
	def get_all(self, account_id, glb_id):
		glbs = dcstats.DCStatusModel.query.filter_by(
			glb_id=glb_id).all()
		return glbs

	def create(self, account_id, glb_id, in_stats):

		base.db.session.add(in_stats)
		base.db.session.commit()
		return in_stats


class DCStatPersistence(BaseService):
	def get(self, account_id, glb_id):
		pass

	def update(self, account_id, glb_id, in_glb):
		pass

	def delete(self, account_id, glb_id):
		pass


class DCStatsPersistenceOps(object):
	def __init__(self):
		self.dsp = DCStatsPersistence(self)
		self.dp = DCStatPersistence(self)
