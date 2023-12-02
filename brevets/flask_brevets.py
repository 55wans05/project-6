"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import requests
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import os
import json

import logging

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = 5000 if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)
API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api"

###
# Backend functions
###

def retrieve_data():
    brevets = requests.get(f"{API_URL}/brevets").json()

    if len(brevets) == 0:
        return {}

    return brevets[-1]

def set_data(data):
    data = requests.post(f"{API_URL}/brevets", json=data) 
    # Placeholder for error checking
    return True

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template("calc.html")


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template("404.html"), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get("km", 999, type=float)
    dist = request.args.get("dist", 200, type=int)
    begin = request.args.get("begin", 200, type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, dist, arrow.get(begin)).format(
        "YYYY-MM-DDTHH:mm"
    )
    close_time = acp_times.close_time(km, dist, arrow.get(begin)).format(
        "YYYY-MM-DDTHH:mm"
    )
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/get-calc")
def get_calc():
    brevet = retrieve_data()
    
    return brevet, 200



@app.route("/set-calc", methods=["POST"])
def set_brevet():
    data = request.get_json()

    result = set_data(data)

    # https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


#############

if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(port_num))
    app.run(port=port_num, host="0.0.0.0")
