import ConfigParser

from flask import Flask
from geolb.models.persistence import base
from flask.ext.restful import Resource, Api

filename = 'config.cfg'
config = ConfigParser.SafeConfigParser()
config.read([filename])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (
    config.get('api', 'username'), config.get('api', 'password'),
    config.get('api', 'address'), config.get('api', 'dbname'))

api = Api(app)

#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#
#@app.teardown_appcontext
#def shutdown_session(exception=None):
#    base.db_session.remove()

from geolb.api.pub.resources import glbs

api.add_resource(glbs.GlobalLoadbalancersResource, '/<int:account_id>/glbs')
api.add_resource(glbs.GlobalLoadbalancerResource, '/<int:account_id>/glbs/<int:id>')

base.db.init_app(app)