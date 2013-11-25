from flask import jsonify, request
from geolb.api.pub.resources.base import BaseResource
from geolb.services import nodeservice


class NodesResource(BaseResource):

    def get(self, account_id, glb_id):
        #Object validation, error handling etc...
        nodes = nodeservice.NodesService().get_all()
        node_list = [n.to_dict() for n in nodes]
        nodes = {"nodes": node_list}
        return jsonify(nodes)

    def post(self, account_id, glb_id):
        json_body = self.get_request_body(request)
        nodes_json = json_body.get('nodes')
        #monitor_json = nodes_json.get('monitor')
        #Object validation, error handling etc...

        g = self.glbservice.g.get(glb_id)
        n = nodeservice.NodesService.create(g.get('id'),  nodes_json)
        #self.monitorservice.ms.create(monitor_json)

        n = {"node": n.to_dict}
        return jsonify(n)


class NodeResource(BaseResource):

    def get(self, id):
        #Object validation, error handling etc...
        node = nodeservice.NodeService.get(id)
        return jsonify({'node': node.to_dict()})

