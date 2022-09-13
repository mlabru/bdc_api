# -*- coding: utf-8 -*-
"""
api_run

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import json
import logging
import sys

# flask
import flask

# local
import bdc_api.api_bdc as db
import bdc_api.api_defs as df

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
@lapp.route("/api/v1/data", methods=["GET"])
def api_filter():
    """
    api filter
    """
    # logger
    M_LOG.info(">> api_filter")

    # logger
    M_LOG.debug("request: %s", str(flask.request.args))

    # request parameters    
    ldct_params = flask.request.args

    # estação
    ls_estacao = ldct_params.get("estacao", None)

    if not valida_estacao(ls_estacao):
        # display an error in the browser
        M_LOG.error("'estacao' não fornecida ou inválida. Especifique uma estação.")
        # return
        return "'estacao' não fornecida ou inválida. Especifique uma estação."

    # data atual
    ldt_now = datetime.datetime.now()

    # data inicial
    ls_data_ini = ldct_params.get("data_ini", None)

    if not valida_data(ls_data_ini):
        # display an error in the browser
        M_LOG.error("'data_ini' não fornecida ou inválida. Assumindo data atual.")
        # assumindo data atual
        ls_data_ini = ldt_now.strftime("%Y%m%d") + "00"

    # data final
    ls_data_fim = ldct_params.get("data_fim", None)

    if not valida_data(ls_data_fim):
        # display an error in the browser
        M_LOG.error("'data_fim' não fornecida ou inválida. Assumindo data atual.")
        # assumindo data atual
        ls_data_fim = ldt_now.strftime("%Y%m%d") + "23"

    # connect BDC
    l_bdc = db.connect_bdc()
    assert l_bdc

    # query BDC
    llst_results = db.get_from_bdc(l_bdc, ls_estacao, ls_data_ini, ls_data_fim)
    M_LOG.debug("llst_results: %s", str(llst_results))

    # close connection
    l_bdc.close()

    # return a converted list of dictionaries
    return llst_results

# ---------------------------------------------------------------------------------------------
def dict_factory(f_cursor, f_row):
    """
    dict_factory
    """
    # logger
    M_LOG.info(">> dict_factory")

    # init temp dict
    ldct_tmp = {}

    # for all columns...
    for lidx, lcol in enumerate(f_cursor.description):
        # datetime ? 
        if isinstance(f_row[lidx], datetime.datetime):
            # format date
            ldct_tmp[lcol[0]] = f_row[lidx].strftime("%Y/%m/%d, %H:%M")

        # senão,...
        else:
            # keep format
            ldct_tmp[lcol[0]] = f_row[lidx]

    # return dictionary
    return ldct_tmp

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
def valida_data(fs_data: str):
    """
    valida data final
    """
    # logger
    M_LOG.info(">> valida_data")

    # não tem conteúdo ?
    if not fs_data:
        # return error
        return False

    try:
        # convert date
        # ldt_date = datetime.datetime.strptime(fs_data, '%Y%m%d%H')

        # split da data
        li_ano = int(fs_data[:4])
        li_mes = int(fs_data[4:6])
        li_dia = int(fs_data[6:8])
        li_hor = int(fs_data[8:10])

    # em caso de erro...
    except ValueError as lerr:
        # return error
        return False
        
    # ok
    lv_ok = True

    # valida os campos da data
    lv_ok &= 2000 <= li_ano <= datetime.date.today().year
    lv_ok &= 1 <= li_mes <= 12
    lv_ok &= 1 <= li_dia <= 31
    lv_ok &= 0 <= li_hor <= 23

    # return
    return lv_ok

# ---------------------------------------------------------------------------------------------
def valida_estacao(fs_estacao: str):
    """
    valida estação
    """
    # logger
    M_LOG.info(">> valida_estacao")

    # return
    return True if fs_estacao else False

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # logger
    M_LOG.info(">> main")

    # flask run
    lapp.run(host="172.18.30.30", port=7000)

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
