from flask import jsonify, request

from geolb.util.mappings.jsonmappings import Mappings
from flask.ext.restful import marshal
from geolb.api.pub.resources.base import BaseResource
from geolb.services import glbservice


class MgmtDCStatsResource(BaseResource):

    def get(self, account_id):
        pass

    def post(self, account_id):
        pass


class MgmtDCStatResource(BaseResource):

    def get(self, account_id, glb_id):
        pass

    def put(self, account_id, glb_id):
        json_body = self.get_request_body(request)
        #Object validation, error handling etc...
        stats_json = json_body.get('dc_stats')
        glb = glbservice.GlobalLoadbalancerService()\
            .update(account_id, glb_id, json_body)
        return jsonify({"glb": glb.to_dict()})

    def delete(self, account_id, glb_id):
        pass

