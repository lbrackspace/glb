import json

import flask

from flask.ext.restful import Resource


class MgmtBaseResource(Resource):

    def __init__(self):
        #Can set configurations and other resource options here...
        pass

    def get_request_body(self, req):
        try:
            #JSON Validation
            raw_json = req.stream.read(req.content_length)
        except Exception:
            raise flask.abort(500)
        try:
            #JSON Validation
            json_body = json.loads(raw_json, 'utf-8')
        except ValueError:
            raise flask.abort(400)
        return json_body