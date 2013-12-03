from geolb.models.persistence import base, dcstats, dclocation_enum
from geolb.persistence.base import BaseService


class DCStatsPersistence(BaseService):
	def get_all(self):
		glbs = dcstats.DCStatModel.query.filter_by().all()
		return glbs

	def get(self, stat_id):
		glbs = dcstats.DCStatModel.query.filter_by(id_=stat_id).first()
		return glbs

	def create(self, in_stats):
		base.db.session.add(in_stats)
		base.db.session.commit()
		return in_stats

	def update(self):
		#:/
		base.db.session.commit()
		pass

	def delete(self, stat_id):
		pass

	def get_all_locations(self):
		return dclocation_enum.DCLocationModel.query.all()


class DCStatsPersistenceOps(object):
	def __init__(self):
		self.dsp = DCStatsPersistence(self)