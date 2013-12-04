from flask import jsonify, request
from geolb.util.mappings.jsonmappings import Mappings
from flask.ext.restful import marshal
from geolb.api.pub.resources.base import BaseResource
from geolb.services import nodeservice, glbservice, regionservice


class RegionsResource(BaseResource):
    def get(self, account_id):
        #Object validation, error handling etc...
        regions = regionservice.RegionsService().get_all()
        region_list = [r.to_dict() for r in regions]
        regions = {"regions": marshal(region_list, Mappings.REGION_FIELDS)}
        return jsonify(regions)

    #These should be mgmt ops, wip...
    def post(self, account_id):
        pass


class RegionResource(BaseResource):
    def get(self, account_id, glb_id):
        pass