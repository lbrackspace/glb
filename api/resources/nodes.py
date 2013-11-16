from api import app
from flask import json, request, abort
from api.resources.base import BaseResource


class NodesResource(BaseResource):

    def get(self, account_id, glb_id):
        #Object validation, error handling etc...
        nodes = self.nodeservice.ns.get_all()
        node_list = [n.to_dict() for n in nodes]
        nodes = {"nodes": node_list}
        return json.dumps(nodes, indent=2)

    def post(self, account_id, glb_id):
        json_body = self.get_request_body(request)
        nodes_json = json_body.get('nodes')
        #monitor_json = nodes_json.get('monitor')
        #Object validation, error handling etc...

        g = self.glbservice.g.get(glb_id)
        n = self.nodeservice.ns.create(g.get('id'),  nodes_json)
        #self.monitorservice.ms.create(monitor_json)

        n = {"node": n.to_dict}
        return json.dumps(n, indent=2)


class NodeResource(BaseResource):

    def get(self, id):
        #Object validation, error handling etc...
        node = self.nodeservice.g.get(id)
        return json.dumps({'node': node.to_dict()}, indent=2)

