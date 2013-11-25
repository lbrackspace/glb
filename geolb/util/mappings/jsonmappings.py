from flask.ext.restful import fields


class Mappings(object):
    MONITOR_FIELDS = {
        'id': fields.String,
        'interval': fields.String,
        'threshold': fields.String
    }

    NODE_FIELDS = {
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
    }
