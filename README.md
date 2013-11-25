GLB API
=======
Currently the 'glb' application utilizes Flask, Flask-RESTful and SQLAlchemy to present a simple API.

Dependency installation
-------
pip install -r < requires.txt

Running the API in development mode
-------
python runServer.py

By default, the server will run on port 5000.
EX: GET http://localhost:5000/406271/glbs will return a list of global load balancers for user 406271.

Deploying the API to a remote machine (Debian 7/Ubuntu 12.04+)
-------
contrib/deployment/deployMaster.sh target-machine

By default, the server will run on port 80.
EX: GET http://target-machine/406271/glbs will return a list of global load balancers for user 406271.

Usage
-------
The endpoints or entry points are defined in api/__init__.py

Example requests will be located in contrib/examples


tbc...
