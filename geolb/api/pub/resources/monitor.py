from flask import jsonify, request
from geolb.api.pub.resources.base import BaseResource
from geolb.services import monitorservice



class MonitorResource(BaseResource):

    def get(self, account_id, id):
        #Object validation, error handling etc...
        monitor = monitorservice.MonitorService().get(id)
        return jsonify({'monitor': monitor.to_dict()})

    def post(self, account_id):
        json_body = self.get_request_body(request)
        mon_json = json_body.get('monitor')
        #Object validation, error handling etc...

        m = monitorservice.MonitorService().create(mon_json)
        return jsonify({"monitor": m.to_dict()})
