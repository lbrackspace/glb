from api.models.persistence import base, glb, nameservers
from api.persistence.base import BaseService


class GlobalLoadbalancersPersistence(BaseService):

    def get_all(self):
        glbs = glb.GlobalLoadbalancerModel.query.all()
        return glbs

    def create(self, account_id, glb):
        #g = glb.GlobalLoadbalancerModel(account_id=account_id, name=name,
        #                   cname="", status="BUILD", algorithm=algorithm, nodes="")

        base.db.session.add(glb)
        base.db.session.commit()

        #Status and cname will be updated once logical operations occur in service, update here for example purposes.
        glb.status = 'ACTIVE'
        glb.cname = '{0}.glbaas.rackspace.net'.format(glb.id_)
        ##Call service rather then persistence?
        ns = nameservers.NameserverModel.query.all()
        for n in glb.nodes:
            n.status = 'ONLINE'
            n.name_servers = ns

        base.db.session.commit()
        return glb


class GlobalLoadbalancerPersistence(BaseService):

    def get(self, id):
        g = glb.GlobalLoadbalancerModel.query.filter_by(id_=id).first()
        return g


class GlbPersistenceOps(object):
    def __init__(self):
        self.gsp = GlobalLoadbalancersPersistence(self)
        self.gp = GlobalLoadbalancerPersistence(self)
