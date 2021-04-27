"""
For convenience and security, it is possible to separate out configuration from the program that runs the Flask app.
It's not essential but useful to hide some elements such as database connection strings and secret keys.
"""
import os
from datetime import timedelta

# Anything that requires encryption (for safe-keeping against tampering by attackers) requires the secret key to be set.
# For just Flask itself, that 'anything' is the Session object, but other extensions can make use of the same secret.
SECRET_KEY = os.urandom(16)

# Database connection string
# for postgresql (change as appropriate) e.g.
# SQLALCHEMY_DATABASE_URI = "postgresql://userid:password@host:port/databasename"

# SQLite - we create an SQLite database in our project
#Unix/Mac (note the four leading slashes for absolute path or three for relative path)
SQLALCHEMY_DATABASE_URI = 'sqlite:///wk11db.db'

#Windows (note 3 leading forward slashes and backslash escapes)
# sqlite:///C:\\absolute\\path\\to\\foo.db

# Tell Flask-SQLAlchemy to track database schema changes using 'Migrate'.
SQLALCHEMY_TRACK_MODIFICATIONS = True

# JSON Web Tokens (JWT)
# Tokens are generated on 'log in' and passed back to allow access to 'protected' resources. This is a bit like getting
# a 'visitors badge' to allow you to enter an office building. The badge confers temporary privileges and expires or is
# handed back when no longer needed.
JWT_SECRET_KEY = os.urandom(16)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
