from api import app
from flask import json, request, abort
from api.resources.base import BaseResource
from api.services import glbservice, nodeservice, monitorservice



class MonitorResource(BaseResource):

    def get(self, account_id, id):
        #Object validation, error handling etc...
        monitor = monitorservice.MonitorService().get(id)
        return json.dumps({'monitor': monitor.to_dict()}, indent=2)

    def post(self, account_id):
        json_body = self.get_request_body(request)
        mon_json = json_body.get('monitor')
        #Object validation, error handling etc...

        m = monitorservice.MonitorService().create(mon_json)
        return json.dumps({"monitor": m.to_dict()}, indent=2)

