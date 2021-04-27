"""
We separate our data model and any logic directly related to the specification and manipulation of data. This results in
the "database stuff" being stored in this file - models.py

"""
# Import the Flask-related variant of SQL Alchemy. Flask-SQLAlchemy is an extension for Flask that adds support for
# SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra
# helpers that make it easier to accomplish common tasks.
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance. Note that this has not yet been associated with the Flask app.
db = SQLAlchemy()


# Specify our models from here. These will map to tables in our database. Note that these are just Python classes and,
# as such, can contain methods specific to data handling or 'property' attributes ('virtual' attributes).
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))

    @property
    def email(self):
        return f"{self.first_name}.{self.last_name}@tudublin.ie"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def as_dictionary(self):
        """
        This 'virtual' property returns a JSON-friendly (i.e. dictionary) representation of the User.
        Note the inclusion of other 'virtual' attributes.

        The use of a dictionary object here is just to keep things simple. In a real app, you would use a serializer
        method to create a representation of the user.

        :return: A dictionary representing the User.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.name,
            "email": self.email
        }

    def __str__(self):
        return self.name
