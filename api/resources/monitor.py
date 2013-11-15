from api import app
from flask import json, request, abort
from api.resources.base import BaseResource


class MonitorResource(BaseResource):

    def get(self, account_id, id):
        #Object validation, error handling etc...
        monitor = self.monitorservice.g.get(id)
        return json.dumps({'monitor': monitor.to_dict()}, indent=2)

    def post(self, account_id):
        json_body = self.get_request_body(request)
        #glb_json = json_body.get('glb')
        #nodes_json = glb_json.get('nodes')
        #monitor_json = nodes_json.get('members')
        #Object validation, error handling etc...

        #n = self.nodeservice.ns.create(account_id, node_json)
        #self.monitorservice.ms.create(monitor_json)

        n = {"monitor": "monitor"}
        return json.dumps(n, indent=2)

