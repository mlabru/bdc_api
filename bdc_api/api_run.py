# -*- coding: utf-8 -*-
"""
api_run

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import json
import logging
import sys

# flask
import flask
from flask import request, jsonify

# local
import bdc_api.api_bdc as db
import bdc_api.api_defs as df

# < defines >----------------------------------------------------------------------------------

# create some test data for our catalog in the form of a list of dictionaries.
DLST_DATA = [
    {"id": 0,
     "title": "A Fire Upon the Deep",
     "author": "Vernor Vinge",
     "first_sentence": "The coldsleep itself was dreamless.",
     "year_published": "1992"},

    {"id": 1,
     "title": "The Ones Who Walk Away From Omelas",
     "author": "Ursula K. Le Guin",
     "first_sentence": "With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.",
     "published": "1973"},

    {"id": 2,
     "title": "Dhalgren",
     "author": "Samuel R. Delany",
     "first_sentence": "to wound the autumnal city.",
     "published": "1975"}
]

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
# Flask init
#
lapp = flask.Flask(__name__)
assert lapp

# flask setup
lapp.config["DEBUG"] = True

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/data/all", methods=["GET"])
def api_all():
    """
    api_all
    """
    # return data
    return jsonify(DLST_DATA)

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/data", methods=["GET"])
def api_id():
    """
    api_id
    """
    # an ID was provided as part of the URL ?
    if "id" in request.args:
        # assign it to a variable
        li_id = int(request.args["id"])

    # senão,...
    else:
        # display an error in the browser
        M_LOG.error("no id field provided. Please specify an id.")
        # return
        return None
        
    # create an empty list for results
    llst_results = []

    # loop through the data and match results that fit the requested ID
    for book in DLST_DATA:
        # IDs are unique, but other fields might return many results
        if book["id"] == li_id:
            llst_results.append(book)

    # return a converted list of dictionaries
    return jsonify(llst_results)

# ---------------------------------------------------------------------------------------------
@lapp.route("/", methods=["GET"])
def home():
    return """<h1>BDC API</h1>
<p>A prototype API for BDC meteorological data.</p>"""

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # connect BDC
    # l_bdc = db.connect_bdc()
    # assert l_bdc

    # flask run
    lapp.run()

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(level=df.DI_LOG_LEVEL)
    
    # disable logging
    # logging.disable(sys.maxsize)
    
    # run application
    main()

    # exit ok
    sys.exit(0)

# < the end >----------------------------------------------------------------------------------
