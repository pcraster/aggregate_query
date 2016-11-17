from flask import jsonify
from . import api


@api.route("/ping")
def ping():
    return jsonify(response="pong"), 200
