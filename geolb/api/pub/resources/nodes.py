from flask import jsonify, request
from geolb.util.mappings.jsonmappings import Mappings
from flask.ext.restful import marshal
from geolb.api.pub.resources.base import BaseResource
from geolb.services import nodeservice, glbservice


class NodesResource(BaseResource):
	def get(self, account_id, glb_id):
		#Object validation, error handling etc...
		nodes = nodeservice.NodesService().get_all(account_id, glb_id)
		node_list = [n.to_dict() for n in nodes]
		nodes = {"nodes": marshal(node_list, Mappings.NODE_FIELDS)}
		return jsonify(nodes)

	def post(self, account_id, glb_id):
		json_body = self.get_request_body(request)
		nodes_json = json_body.get('nodes')
		#monitor_json = nodes_json.get('monitor')
		#Object validation, error handling etc...

		g = glbservice.GlobalLoadbalancerService().get(account_id, glb_id)
		n = nodeservice.NodesService().create(account_id, g.id_, nodes_json)
		n = {"node": n.to_dict()}
		return jsonify(n)


class NodeResource(BaseResource):

	def get(self, account_id, glb_id, node_id):
		#Object validation, error handling etc...
		node = nodeservice.NodeService().get(account_id, glb_id, node_id)
		return jsonify({'node': node.to_dict()})

	def put(self, account_id, glb_id, node_id):
		json_body = self.get_request_body(request)
		#Object validation, error handling etc...
		node_json = json_body.get('glb')
		node = nodeservice.NodeService()\
			.update(account_id, glb_id, node_id, node_json)
		return jsonify({"node": node.to_dict()})

	def delete(self, account_id, glb_id, node_id):
		#Object validation, error handling etc...
		glb = nodeservice.NodeService().delete(account_id, glb_id, node_id)
		return jsonify({"glb": glb.to_dict()})

