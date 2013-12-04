from flask.ext.restful import fields


class Regionless(fields.Raw):
    def format(self, value):
        if value:
            return "wookie"
        else:
            return "wookie"


class Mappings(object):
    MONITOR_FIELDS = {
    'id': fields.String,
    'interval': fields.String,
    'threshold': fields.String
    }

    DC_STATS_FIELDS = {
    'id': fields.String,
    'location': fields.String,
    'updated': fields.String,
    'status': fields.String
    }

    REGION_FIELDS = {
    'name': fields.String,
    'description': fields.String
    }

    NODE_FIELDS = {
    'id': fields.String,
    'ip_address': fields.String,
    'ip_type': fields.String,
    'type': fields.String,
    'status': fields.String,
    'monitor': fields.Nested(MONITOR_FIELDS),
    'regions': fields.Nested(REGION_FIELDS)
    }

    NODE_FIELDS_NO_REGION = {
    'id': fields.String,
    'ip_address': fields.String,
    'ip_type': fields.String,
    'type': fields.String,
    'status': fields.String,
    'monitor': fields.Nested(MONITOR_FIELDS)
    }

    NAMESERVER_FIELDS = {
    'id': fields.String,
    'name': fields.String
    }

    GLB_FIELDS = {
    'id': fields.String,
    'name': fields.String,
    'cname': fields.String,
    'create_time': fields.String,
    'update_time': fields.String,
    'algorithm': fields.String,
    'status': fields.String,
    'nodes': fields.Nested(NODE_FIELDS),
    'dc_stats': fields.Nested(DC_STATS_FIELDS),
    }
