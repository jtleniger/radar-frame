import logging
from flask import Flask, send_file
import os

def create(config):
    app = Flask(__name__, root_path=os.getcwd())

    @app.route('/frame')
    def frame():
        return send_file(config['files']['output_img'], mimetype='image/png')

    return app