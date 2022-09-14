# -*- coding: utf-8 -*-
"""
api_run

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import socket
import sys

# flask
import flask

# local
import bdc_api.api_defs as df
import bdc_api.api_prc as pr

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
# flask initialize
#
lapp = flask.Flask(__name__)
assert lapp

# flask setup
lapp.config["DEBUG"] = True

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/precipitacao", methods=["GET"])
def api_precipitacao():
    """
    api precipitacao
    """
    # logger
    M_LOG.info(">> api_precipitacao")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_precipitacao")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/pressao", methods=["GET"])
def api_pressao():
    """
    api pressao
    """
    # logger
    M_LOG.info(">> api_pressao")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_pressao")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/rvr", methods=["GET"])
def api_rvr():
    """
    api rvr
    """
    # logger
    M_LOG.info(">> api_rvr")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_rvr")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/temperatura", methods=["GET"])
def api_temperatura():
    """
    api temperatura
    """
    # logger
    M_LOG.info(">> api_temperatura")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_temperatura")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/teto", methods=["GET"])
def api_teto():
    """
    api teto
    """
    # logger
    M_LOG.info(">> api_teto")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_teto")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/vento", methods=["GET"])
def api_vento():
    """
    api vento
    """
    # logger
    M_LOG.info(">> api_vento")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_vento")

# ---------------------------------------------------------------------------------------------
@lapp.route("/api/v1/visibilidade", methods=["GET"])
def api_visibilidade():
    """
    api visibilidade
    """
    # logger
    M_LOG.info(">> api_visibilidade")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args.to_dict()))

    # return a converted list of dictionaries (JSON)
    return pr.processa_request(flask.request.args.to_dict(), "vwm_unificado_visibilidade")

# ---------------------------------------------------------------------------------------------
@lapp.route("/", methods=["GET"])
def home():
    """
    home
    """
    # logger
    M_LOG.info(">> home")

    # return data
    return """<h1>BDC API</h1>
<p>A prototype API for BDC meteorological data.</p>"""

# ---------------------------------------------------------------------------------------------
@lapp.errorhandler(404)
def page_not_found(err):
    """
    page not found
    """
    # logger
    M_LOG.info(">> page_not_found")

    # return data
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # logger
    M_LOG.info(">> main")

    # hostname
    ls_hostname = socket.gethostname()
    # ip address
    ls_addr = socket.gethostbyname(ls_hostname)

    # flask run
    lapp.run(host=ls_addr, port=7000)

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
