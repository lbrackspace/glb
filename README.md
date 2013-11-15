Currently the 'glb' application utilizes Flask, Flask-restful and SqlAlchemy to accomplish a simple api.

In order to run you must have flask, flask-restful and flask-sqlalchemy installed.

Run:

python runserver.py


The server will run on port 5000. The endpoints or entry points are defined in api/__init__.py

EX: GET http://localhost:5000/406271/glbs will return list of global load balancers.

Example requests will be located in contrib/examples


tbc...