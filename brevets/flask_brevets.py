"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import os
import json
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

client = MongoClient("mongodb://" + os.environ["DB_HOSTNAME"], 27017)
db = client.mydb

###
# Backend functions
###

def retrieve_data():
    # Inspired by https://stackoverflow.com/questions/62295223/pymongo-query-to-get-the-latest-document-from-the-collection-in-mongodb-using-py
    brevet = db.brevets.find().sort("_id", -1).limit(1)

    for i in brevet:
        return i

    return None

def set_data(data):

    # I'm being explicit about the data structure here for ease of reading
    data = {
        "begin_date": data["begin_date"],
        "brevet_distance": data["brevet_distance"],
        "items": data["items"],
    }

    db.brevets.insert_one(data)
    
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
    if brevet is not None:
        return flask.jsonify(
            begin_date=brevet["begin_date"],
            brevet_distance=brevet["brevet_distance"],
            items=brevet["items"],
        )

    return json.dumps({"success": False}), 404, {"ContentType": "application/json"}


@app.route("/set-calc", methods=["POST"])
def set_brevet():
    data = request.get_json()

    result = set_data(data)

    # https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
