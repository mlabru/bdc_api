# -*- coding: utf-8 -*-
"""
api_prc

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# flask
import flask

# pandas
import pandas as pd

# local
import bdc_api.api_bdc as db
import bdc_api.api_chk as ck
import bdc_api.api_defs as df

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def processa_pesquisa(fdct_parms: dict) -> pd.DataFrame:
    """
    processa request

    :param fdct_parms(dict): parâmetros

    :returns: a converted list of dictionaries to JSON
    """
    # logger
    M_LOG.info(">> processa_pesquisa")

    # valida parâmetros
    if not ck.check_params(fdct_parms):
        # return empty
        return {}

    # return a converted list of dictionaries to JSON
    return db.submit_query(fdct_parms)

# ---------------------------------------------------------------------------------------------
def processa_request(fdct_parms: dict, fs_view: str) -> str:
    """
    processa request

    :param fdct_parms(dict): parâmetros
    :param fs_view(str): view

    :returns: a converted list of dictionaries to JSON
    """
    # logger
    M_LOG.info(">> processa_request")

    # valida parâmetros
    if not ck.check_params(fdct_parms):
        # return empty
        return flask.jsonify([{}])

    # insert view
    fdct_parms[df.DS_KEY_VIEW] = fs_view

    # submit query
    l_data = db.submit_query(fdct_parms)

    # return a converted list of dictionaries to JSON
    return l_data.to_json(orient="records", force_ascii=False)

# < the end >----------------------------------------------------------------------------------
