from api.models.persistence import base, glb, nameservers
from api.persistence.base import BaseService
#temp
from datetime import datetime


class GlobalLoadbalancersPersistence(BaseService):

    def get_all(self):
        glbs = glb.GlobalLoadbalancerModel.query.all()
        return glbs

    def get_account(self, aid):
        glbs = glb.GlobalLoadbalancerModel.query.filter(
                        glb.GlobalLoadbalancerModel.account_id == aid)
        return glbs

    def create(self, account_id, in_glb):
        ##Call service rather then persistence?
        for n in in_glb.nodes:
            n.status = 'ONLINE'

        ns = nameservers.NameserverModel.query.all()
        in_glb.name_servers = ns
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


class GlbPersistenceOps(object):
    def __init__(self):
        self.gsp = GlobalLoadbalancersPersistence(self)
        self.gp = GlobalLoadbalancerPersistence(self)
