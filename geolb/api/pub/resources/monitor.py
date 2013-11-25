from flask import jsonify, request
from geolb.api.pub.resources.base import BaseResource
from geolb.services import monitorservice



class MonitorResource(BaseResource):

    def get(self, account_id, glb_id, node_id):
        #Object validation, error handling etc...
        monitor = monitorservice.MonitorService().get(account_id, glb_id, node_id)
        return jsonify({'monitor': monitor.to_dict()})

    def post(self, account_id, glb_id, node_id):
        json_body = self.get_request_body(request)
        mon_json = json_body.get('monitor')
        #Object validation, error handling etc...

        m = monitorservice.MonitorService().create(account_id, glb_id, node_id, mon_json)
        return jsonify({"monitor": m.to_dict()})

    def put(self, account_id, glb_id, node_id, mon_json):
        json_body = self.get_request_body(request)
        #Object validation, error handling etc...
        monitor = monitorservice.MonitorService()\
            .update(account_id, glb_id, node_id, mon_json)
        return jsonify({"monitor": monitor.to_dict()})

    def delete(self, account_id, glb_id, node_id):
        #Object validation, error handling etc...
        monitor = monitorservice.MonitorService().delete(account_id,  glb_id, node_id)
        return jsonify({"monitor": monitor.to_dict()})

