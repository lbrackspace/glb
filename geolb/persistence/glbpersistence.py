from geolb.models.persistence import base, glb, nameservers
from geolb.persistence.base import BaseService
#temp


class GlobalLoadbalancersPersistence(BaseService):

    def get_all(self, account_id):
        glbs = glb.GlobalLoadbalancerModel.query.filter_by(account_id=account_id).all()
        #:/
        return glbs

    def create(self, account_id, in_glb):
        #nodes updated after validation, update here for example purposes.
        for n in in_glb.nodes:
            n.status = 'ONLINE'

        base.db.session.add(in_glb)
        base.db.session.commit()
        #Status and cname will be updated in service once logical
        # operations occur in service, update here for example purposes.
        in_glb.status = 'ACTIVE'
        in_glb.cname = '{0}.glbaas.rackspace.net'.format(in_glb.id_)
        base.db.session.commit()
        return in_glb


class GlobalLoadbalancerPersistence(BaseService):

    def get(self, id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=id).first()
        return g

    def update(self, in_glb):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=in_glb.id_).first()
        #Any other attributes...
        g.name = in_glb.name
        g.algorith = in_glb.algorithm
        base.db.session.commit()
        return g

    def delete(self, glb_id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=glb_id).first()
        try:
            #base.db.session.delete(g)
            g.status = 'DELETED'
            base.db.session.commit()
            return g
        except:
            print "Delete glb %d failed..." % glb_id
            raise LookupError


class GlbPersistenceOps(object):
    def __init__(self):
        self.gsp = GlobalLoadbalancersPersistence(self)
        self.gp = GlobalLoadbalancerPersistence(self)
