# -*- coding: utf-8 -*-
"""
api_prc

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# local
import bdc_api.api_bdc as db
import bdc_api.api_chk as ck
import bdc_api.api_defs as df

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def processa_request(fdct_parms: dict, fs_view: str):
    """
    processa request

    :param fdct_parms(dict): parâmetros
    :param fs_view(str): view
    """
    # logger
    M_LOG.info(">> processa_request")

    # valida parâmetros
    if not ck.check_params(fdct_parms):
        # return empty
        return flask.jsonify({})

    # insert view
    fdct_parms[df.DS_KEY_VIEW] = fs_view

    # submit query
    l_data = db.submit_query(fdct_parms)

    # return a converted list of dictionaries to JSON
    return l_data.to_json(orient="records", force_ascii=False)

# < the end >----------------------------------------------------------------------------------
