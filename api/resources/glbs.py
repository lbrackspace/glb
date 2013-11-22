from api import app
from flask import jsonify, request, abort
from flask.ext.restful import fields, marshal
from api.resources.base import BaseResource
from api.services import glbservice, nodeservice, monitorservice

node_fields = {
    'id': fields.String,
    'name': fields.String,
    'cname': fields.String,
    'algorithm': fields.String,
    'status': fields.String,
    'nodes': fields.Nested
}

glb_fields = {
    'id': fields.String,
    'name': fields.String,
    'cname': fields.String,
    'algorithm': fields.String,
    'status': fields.String,
    'nodes': fields.Nested
}

class GlobalLoadbalancersResource(BaseResource):

    def get(self, account_id):
        #Object validation, error handling etc...
        glbs = glbservice.GlobalLoadbalancersService().get_account(account_id)
        glb_list = [g.to_dict() for g in glbs]
        #glbs = {"glbs": marshal(glb_list, glb_fields)}
        glbs = {"glbs": glb_list}
        return glbs

    def post(self, account_id):
        json_body = self.get_request_body(request)
        glb_json = json_body.get('glb')
        nodes_json = glb_json.get('nodes')
        #monitor_json = nodes_json.get('monitor')


        #Object validation, error handling etc...
        ##Do hydrated object here calling each service to
        # validate and create object, or send hydrated glb to
        # service and let the services commuicate between eachother.
        g = glbservice.GlobalLoadbalancersService().create(account_id, glb_json)
        g = {"glb": g.to_dict()}
        return jsonify(g)


class GlobalLoadbalancerResource(BaseResource):

    def get(self, account_id, id):
        #Object validation, error handling etc...
        glb = glbservice.GlobalLoadbalancerService().get(id)
        return jsonify({'glb': glb.to_dict()})

