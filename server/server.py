import os
from flask import Flask
from pathlib import Path

from server.api import api


def create():
    app = Flask(__name__, root_path=os.getcwd(), template_folder=(Path(os.getcwd()) / Path('views')))
    app.register_blueprint(api)
    return app
