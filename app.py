"""
This is the program that runs our Flask app. Flask is a 'minimal' framework that just handles 'routing' - the parsing
of URL strings and passing 'requests' to some piece of functionality - a function or a class.
"""

# Import the Flask stuff
#
# Flask - the framework
# Flask is a web application framework written in Python. A Web Application Framework or a simply a Web Framework
# represents a collection of libraries and modules that enable web application developers to write applications without
# worrying about low-level details such as protocol, thread management, and so on. Flask is based on the Werkzeg WSGI
# toolkit and the Jinja2 template engine. The Web Server Gateway Interface (Web Server Gateway Interface, WSGI) has been
# used as a standard for Python web application development. WSGI is the specification of a common interface between web
# servers and web applications. Werkzeug is a WSGI toolkit that implements requests, response objects, and utility
# functions. This enables a web frame to be built on it. The Flask framework uses Werkzeg as one of its bases.
#
# request - makes the 'request' object available any logic so that (e.g.) data can be extracted from it.
# To access incoming request data, you can use the global request object. Flask parses incoming request data for you and
# gives you access to it through that global object.
#
# Migrate - Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using
# 'Alembic'. Alembic is a database migrations tool written by the author of SQLAlchemy. A migrations tool offers the
# following functionality:
# * Can emit ALTER statements to a database in order to change the structure of tables and other constructs
# * Provides a system whereby "migration scripts" may be constructed; each script indicates a particular series of steps
#   that can "upgrade" a target database to a new version, and optionally a series of steps that can "downgrade"
#   similarly, doing the same steps in reverse.
# * Allows the scripts to execute in some sequential manner.
# Flask-Migrate configures Alembic in the proper way to work with your Flask and Flask-SQLAlchemy application. In terms
# of the actual database migrations, everything is handled by Alembic so you get exactly the same functionality.
#
# Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs. It is a lightweight
# abstraction that works with your existing ORM/libraries. Flask-RESTful encourages best practices with minimal setup.
# If you are familiar with Flask, Flask-RESTful should be easy to pick up.
# Resource - The main building block provided by Flask-RESTful are resources. Resources are built on top of Flask
# pluggable views, giving you easy access to multiple HTTP methods just by defining methods on your resource.
#

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api

# Import our database-related from our models.py files. This is an alternative to putting everything in this app.py
# program.
from models import db
from models import User

# Import basic stuff from the standard library
import json
import datetime

# make a Flask instance
app = Flask(__name__)

# Configure Flask from a file - this is an alternative to including the config information in this app.py file.
app.config.from_pyfile("config.py", silent=True)

# Connect our SQLAlchemy instance to our Flask instance.
db.init_app(app)
# Handle database migrations through Flask-Migrate
migrate = Migrate(app, db)

# With the above application you can create a migration repository with the following command:
#   flask db init
# This will add a migrations folder to your application. The contents of this folder need to be added to version control
# along with your other source files. You can then generate an initial migration:
#   flask db migrate -m "Initial migration."
# The migration script may need to be reviewed and edited, as Alembic currently does not detect every change you make
# to your models. In particular, Alembic is currently unable to detect table name changes, column name changes, or
# anonymously named constraints. A detailed summary of limitations can be found in the Alembic autogenerate
# documentation. Once finalized, the migration script also needs to be added to version control.
# Then you can apply the migration to the database:
#   flask db upgrade
# Then each time the database models change repeat the migrate and upgrade commands.

# Connect our Flask-RESTful API to our Flask instance.
api = Api(app)


def check_incoming_data(request):
    """
    Take an incoming request object object and look for data as json or in 'request.data'. In either case return
    JSON-encoded data as a Python dictionary. This function just checks for the presence of incoming data. The
    specifics of what's expected is up to you.

    :param request: The incoming request object
    :return: The data as dictionary
    """
    try:
        if request.get_json():
            incoming_data = request.get_json()
        else:
            incoming_data = request.data.decode(encoding="utf-8")
            incoming_data = json.dumps(incoming_data)

        return incoming_data
    except Exception as e:
        return False


# In a minimal Flask app we use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def hello_everyone():
    """
    The basic idea here is that an incoming URL pattern (not including the protocol/host/port part) is matched against
    'routs' and if a match is found the associated function is fired. Essentially, a 'request' object is handed to the
    function and a 'response' object must be returned by it. What happens between request and response is up to you.

    At its most basic, this is the essence of Flask. As we can see, in this program, there are other related services
    added to our app but basic Flask just deals with routing and passing back responses. Depending on the nature of the
    response, Flask makes intelligent decisions regarding type. In this example, as we are returning a Python
    dictionary, it is serialized to JSON. If, for example, it was plain text it would be returned as type 'text/plain'.

    :return: A response object and associated status code.
    """
    return {"message": f'Welcome to my World! It is now {datetime.datetime.now().isoformat()}'}, 200


# Flask-RESTful resources give you easy access to multiple HTTP methods (among other things).
class UserResource(Resource):
    def get(self):
        """
        Respond to a GET request on this resource and return a Response object in JSON format. Also send back a status
        code of 200 (all went well) or 400 (an error occurred).

        In our example we are going to interact with the database to retrieve data for all users and return this as
        JSON,

        :return:
        """
        try:
            users_list = []

            # Query the database and grab all users. Then append these to a list
            users = db.session.query(User).all()
            for user in users:
                users_list.append(user.as_dictionary)

            db.session.close()
            # 'users_list' is now a list of dictionary objects. This structure will be automatically serialized to
            # JSON.
            return users_list, 200

        except Exception as e:
            # We don't really care, at this stage, what sort of error occurred. In a 'real' system, you shouldn't do
            # this, but trap specific errors and react accordingly. At the very least, you should send back friendlier
            # error messages.
            return {"error": f"{e}"}, 400

    def post(self):
        """
        Respond to a POST request on this resource and return a Response object in JSON format. Also send back a status
        code of 200 (all went well) or 400 (an error occurred).

        This function makes a new user from data supplied in the request object.

        :return: Data and/or error message with status code.
        """
        try:
            # Grab the incoming data from the request object and check that it seems reasonable.
            incoming = check_incoming_data(request)
            if not incoming:
                raise ValueError("Invalid or missing User data")

            # Create a new 'User' object - an instance of User - based on the incoming data. If this is incorrect or
            # incomplete an error will be thrown.
            new_user = User(**incoming)

            # Add this to the database session. We could add multiple database operations with a view to comitting them
            # all at once.
            db.session.add(new_user)

            # 'Commit' the db actions. The database is not updated until this happens.
            db.session.commit()

            # Return status code 201. This tells us that the request was successful and that a new database resource was
            # created.
            return "", 201

        except Exception as e:
            return {"error": f"{e}"}, 400


class UserResourceId(Resource):
    """
    This is very similar to the UserResource class except that we handle User Id in the URL pattern. The GET request
    gets a specific record only. The DELETE request should be self-explanatory.
    """

    def get(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"Couldn't find user with id, {user_id}")

            return user.as_dictionary, 200
        except Exception as e:
            return {"error": f"{e}"}, 400

    def delete(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            if not user:
                raise ValueError(f"Couldn't find user with id, {user_id}")

            db.session.delete(user)
            db.session.commit()

            return "", 204
        except Exception as e:
            return {"error": f"{e}"}, 400


api.add_resource(UserResource, "/user/")
api.add_resource(UserResourceId, "/user/<int:user_id>/")

if __name__ == '__main__':
    app.run()
