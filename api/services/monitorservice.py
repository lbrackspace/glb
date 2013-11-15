from api import app
import json
from flask import request
from api.services.base import BaseService


class MonitorService(BaseService):

    def get(self, id):
        #Logical validation and other operations
        monitor = self.monitorpersistence.mp.get(id)
        return monitor

    def create(self, account_id, monitor):
        #Logical validation and other operations
        m = self.monitorpersistence.mp.create(account_id,
                                              monitor.get('interval'),
                                              monitor.get('threshold'))
        return m


class MonitorServiceOps(object):
    def __init__(self):
        self.m = MonitorService()