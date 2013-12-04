from flask import jsonify, request

from geolb.util.mappings.jsonmappings import Mappings
from flask.ext.restful import marshal
from geolb.api.pub.resources.base import BaseResource
from geolb.services import glbservice


class GlobalLoadbalancersResource(BaseResource):
    def get(self, account_id):
        #Object validation, error handling etc...
        glbs = glbservice.GlobalLoadbalancersService().get_all(account_id)
        glb_list = [g.to_dict() for g in glbs]
        glbs = {"glbs": marshal(glb_list, Mappings.GLB_FIELDS)}
        #glbs = {"glbs": glb_list}
        return glbs

    def post(self, account_id):
        json_body = self.get_request_body(request)
        glb_json = json_body.get('glb')
        nodes_json = glb_json.get('nodes')
        #monitor_json = nodes_json.get('monitor')

        #Object validation, error handling etc...
        ##Do hydrated object here calling each service to
        # validate and create object, or send hydrated glb to
        # service and let the services communicate between each other.
        glb = glbservice.GlobalLoadbalancersService() \
            .create(account_id, glb_json)
        glb = {"glb": marshal([glb.to_dict()], Mappings.GLB_FIELDS)}
        return jsonify(glb)


class GlobalLoadbalancerResource(BaseResource):
    def get(self, account_id, glb_id):
        #Object validation, error handling etc...
        glb = glbservice.GlobalLoadbalancerService().get(account_id, glb_id)
        return jsonify({"glb": marshal([glb.to_dict()], Mappings.GLB_FIELDS)})

    def put(self, account_id, glb_id):
        json_body = self.get_request_body(request)
        #Object validation, error handling etc...
        glb_json = json_body.get('glb')
        glb = glbservice.GlobalLoadbalancerService() \
            .update(account_id, glb_id, glb_json)
        return jsonify({"glb": marshal([glb.to_dict()], Mappings.GLB_FIELDS)})

    def delete(self, account_id, glb_id):
        #Object validation, error handling etc...
        glb = glbservice.GlobalLoadbalancerService().delete(account_id, glb_id)
        return jsonify({"glb": marshal([glb.to_dict()], Mappings.GLB_FIELDS)})

