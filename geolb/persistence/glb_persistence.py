from geolb.models.persistence import base, glb, nameserver, dcstats
from geolb.persistence.base import BaseService
#temp


class GlobalLoadbalancersPersistence(BaseService):
    def get_all(self, account_id):
        glbs = glb.GlobalLoadbalancerModel.query.filter_by(
            account_id=account_id).all()
        return glbs

    def create(self, account_id, in_glb):
        #nodes updated after validation, update here for example purposes.
        for n in in_glb.nodes:
            #monitoring will handle this...
            n.status = 'ONLINE'

        base.db.session.add(in_glb)
        base.db.session.flush()
        #Status and cname will be updated in service once logical
        # operations occur in service, update here for example purposes.
        in_glb.cname = 'glb_{0}.rackspace.net'.format(in_glb.id_)
        base.db.session.commit()
        return in_glb


class GlobalLoadbalancerPersistence(BaseService):
    def get(self, account_id, glb_id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=glb_id).first()
        return g

    def get_online_dcstats(self, account_id, glb_id):
        os = glb.GlobalLoadbalancerModel.query\
            .join(glb.dc_stats).filter(glb.id_)\
            .filter(glb.dc_stats.any(dcstats.status.in_(['ONLINE']))).first()
        return os

    def get_error_dcstats(self, account_id, glb_id):
        os = glb.GlobalLoadbalancerModel.query\
            .join(glb.dc_stats).filter(glb.id_)\
            .filter(glb.dc_stats.any(dcstats.status.in_(['ERROR']))).first()
        return os

    def update(self, account_id, glb_id, in_glb):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=glb_id).first()
        #Any other attributes...
        #g.name = in_glb.name
        #g.algorith = in_glb.algorithm
        #g.dc_status = in_glb.dc_status
        #g.status = in_glb.status
        #g.create_time = in_glb.create_time
        #g.update_time = in_glb.update_time
        g = in_glb
        base.db.session.commit()
        return g

    def delete(self, account_id, glb_id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=glb_id).first()
        try:
            #base.db.session.delete(g)
            g.status = 'DELETED'
            g.update_type = 'DELETE'
            base.db.session.commit()
            return g
        except:
            print "Delete glb %d failed..." % glb_id
            raise LookupError


class GlbPersistenceOps(object):
    def __init__(self):
        self.gsp = GlobalLoadbalancersPersistence(self)
        self.gp = GlobalLoadbalancerPersistence(self)
