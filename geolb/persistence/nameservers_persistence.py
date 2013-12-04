from geolb.models.persistence import base, nameserver
from geolb.persistence.base import BaseService


class NameServersPersistence(BaseService):
    def get_all(self):
        ns = nameserver.NameserverModel.query.all()
        ns_list = [n.to_dict() for n in ns]
        return ns_list

    def create(self, name):
        n = nameserver.NameserverModel(name=name)

        base.db.session.add(n)
        base.db.session.commit()
        return n


class NameServerPersistence(BaseService):
    def get(self, id):
        n = nameserver.NameserverModel.query.filter_by(id_=id).first()
        return n


class NameserverPersistenceOps(object):
    def __init__(self):
        self.nsp = NameServersPersistence(self)
        self.np = NameServerPersistence(self)
