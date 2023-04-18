import os
from flask import Flask

from server.api import api


def create():
    app = Flask(__name__, root_path=os.getcwd())
    app.register_blueprint(api)
    return app
