from flask import jsonify, request

from geolb.util.mappings.jsonmappings import Mappings
from flask.ext.restful import marshal
from geolb.api.pub.resources.base import BaseResource
from geolb.services import dcstatsservice


class MgmtDCStatsResource(BaseResource):
    def get(self):
        pass

    def post(self):
        #Add many new stats to different glbs
        pass

    def put(self):
        #Update many new stats to different glbs
        json_body = self.get_request_body(request)
        #Object validation, error handling etc...
        stats_json = json_body.get('dc_stats')
        dcstatsservice.DCStatsService().update(stats_json)
        return json_body, 202


class MgmtDCStatResource(BaseResource):
    def get(self, stat_id):
        pass

    def put(self, stat_id):
        pass
