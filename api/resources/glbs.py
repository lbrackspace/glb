from api import app
from flask import json, request, abort
from api.resources.base import BaseResource


class GlobalLoadbalancersResource(BaseResource):

    def get(self, account_id):
        #Object validation, error handling etc...
        glbs = self.glbservice.gs.get_all()
        glb_list = [g.to_dict() for g in glbs]
        glbs = {"glbs": glb_list}
        return json.dumps(glbs, indent=2)

    def post(self, account_id):
        json_body = self.get_request_body(request)
        glb_json = json_body.get('glb')
        #nodes_json = glb_json.get('nodes')
        #monitor_json = nodes_json.get('members')
        #Object validation, error handling etc...

        g = self.glbservice.gs.create(account_id, glb_json)
        #self.nodeservice.ns.create(nodes_json)
        #self.monitorservice.ms.create(monitor_json)

        g = {"glb": g.to_dict()}
        return json.dumps(g, indent=2)


class GlobalLoadbalancerResource(BaseResource):

    def get(self, account_id, id):
        #Object validation, error handling etc...
        glb = self.glbservice.g.get(id)
        return json.dumps({'glb': glb.to_dict()}, indent=2)

