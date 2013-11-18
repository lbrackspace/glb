from api import app
import json
from flask import request
from api.services.base import BaseService
from api.models.persistence import glb, node, monitor


class GlobalLoadbalancersService(BaseService):

    def get_all(self):
        #Logical validation and other operations
        glbs = self.glbpersistence.gsp.get_all()
        return glbs

    def create(self, account_id, glb_json):
        #Logical validation and other operations
        ##temp...
        nodes_json = glb_json.get('nodes')
        if nodes_json is not None:
            #nodeservice.NodesService.create(nodes_json)
            #monitorservice.MonitorService.create(monitor_json)
            nlist = []
            for n in nodes_json:
                m = n.get('monitor')
                mm = monitor.MonitorModel(interval=m.get('interval'), threshold=m.get('threshold'))
                nm = node.NodeModel(ip_address=n.get('ip_address'), type=n.get('type'), monitor=mm)
                nlist.append(nm)

            glbm = glb.GlobalLoadbalancerModel(account_id=account_id, name=glb_json.get('name'),
                                    cname=None, status=None, algorithm=glb_json.get('algorithm'),
                                    nodes=nlist)
            g = self.glbpersistence.gsp.create(account_id, glbm)
        return g


class GlobalLoadbalancerService(BaseService):

    def get(self, id):
        #Logical validation and other operations
        glbs = self.glbpersistence.gp.get(id)
        return glbs


class GlbServiceOps(object):
    def __init__(self):
        self.gs = GlobalLoadbalancersService()
        self.g = GlobalLoadbalancerService()