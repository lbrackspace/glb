from api.models.persistence import base, glb
from api.persistence.base import BaseService


class GlobalLoadbalancersPersistence(BaseService):

    def get_all(self):
        glbs = glb.GlobalLoadbalancerModel.query.all()
        return glbs

    def create(self, account_id, name, algorithm):
        g = glb.GlobalLoadbalancerModel(account_id=account_id, name=name,
                           cname="", status="BUILD", algorithm=algorithm, nodes="")

        base.db.session.add(g)
        base.db.session.commit()

        #Status and cname will be updated once logical operations occur in service, update here for example purposes.
        g.status = 'ACTIVE'
        g.cname = '{0}.glb.lbaas.rackspace.net'.format(g.id_)
        base.db.session.commit()
        return g


class GlobalLoadbalancerPersistence(BaseService):

    def get(self, id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=id).first()
        return g


class GlbPersistenceOps(object):
    def __init__(self):
        self.gsp = GlobalLoadbalancersPersistence(self)
        self.gp = GlobalLoadbalancerPersistence(self)
