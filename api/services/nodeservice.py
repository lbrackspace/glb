from api import app
import json
from flask import request
from api.services.base import BaseService


class NodesService(BaseService):

    def get_all(self):
        #Logical validation and other operations
        glbs = self.glbpersistence.gsp.get_all()
        return glbs

    def create(self, account_id, glb):
        #Logical validation and other operations
        g = self.glbpersistence.gsp.create(account_id, glb.get('name'), glb.get('algorithm'))
        return g


class NodeService(BaseService):

    def get(self, id):
        #Logical validation and other operations
        glbs = self.glbpersistence.gp.get(id)
        return glbs


class NodeServiceOps(object):
    def __init__(self):
        self.ns = NodesService()
        self.n = NodeService()