import flask
import json
from api import app
import werkzeug.exceptions as ex
from flask import Flask, abort

from api.services.base import BaseService


class BaseResource(object):

    def __init__(self):
        #Can set configurations and other resource options here...
        self.glbservice = BaseService.GlbServiceOps()
        self.nodeservice = BaseService.NodeServiceOps()
        self.monitorservice = BaseService.MonitorServiceOps()

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