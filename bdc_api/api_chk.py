# -*- coding: utf-8 -*-
"""
api_chk

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import logging

# local
import bdc_api.api_defs as df

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def _check_date(fs_data: str) -> bool:
    """
    valida data

    :param fs_data (str): data

    :returns: True if ok, False otherwise
    """
    # logger
    M_LOG.info(">> _check_date")

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
def _check_local(fs_local: str) -> bool:
    """
    valida localidade

    :param fs_local (str): localidade

    :returns: True if ok, False otherwise
    """
    # logger
    M_LOG.info(">> _check_local")

    # empty string ?
    if not fs_local:
        # return error
        return False

    # return
    return fs_local.upper() in df.DDCT_LOCAL.values()

# ---------------------------------------------------------------------------------------------
def check_params(fdct_parms: dict) -> bool:
    """
    valida parâmetros

    :param fdct_parms (dict): parâmetros

    :returns: True if, ok False otherwise
    """
    # logger
    M_LOG.info(">> check_params")

    # API key
    ls_key = fdct_parms.get(df.DS_KEY_API, None)

    if not ls_key in df.DLST_API_KEYS:
        # display an error in the browser
        M_LOG.error("API key (%s) não fornecida ou inválida.", str(ls_key))
        # return
        return False

    # estação
    ls_local = fdct_parms.get(df.DS_KEY_LOCAL, None)

    if not _check_local(ls_local):
        # display an error in the browser
        M_LOG.error("localidade (%s) não fornecida ou inválida.", str(ls_local))
        # return
        return False

    # data atual
    ldt_now = datetime.datetime.now()

    # data inicial
    ls_data_ini = fdct_parms.get(df.DS_KEY_DTINI, None)

    if not _check_date(ls_data_ini):
        # logger
        M_LOG.warning("data inicial (%s) não fornecida ou inválida.", str(ls_data_ini))
        # assumindo data atual
        fdct_parms[df.DS_KEY_DTINI] = ldt_now.strftime("%Y%m%d") + "00"

    # data final
    ls_data_fim = fdct_parms.get(df.DS_KEY_DTFIM, None)

    if not _check_date(ls_data_fim):
        # logger
        M_LOG.warning("data final (%s) não fornecida ou inválida.", str(ls_data_fim))
        # assumindo data atual
        fdct_parms[df.DS_KEY_DTFIM] = ldt_now.strftime("%Y%m%d") + "23"

    # verifica intervalo de 1 ano
    _check_1year(fdct_parms)

    # return
    return True

# ---------------------------------------------------------------------------------------------
def _check_1year(fdct_parms: dict):
    """
    valida intervalo menor que 1 ano

    :param fdct_parms (dict): parâmetros
    """
    # logger
    M_LOG.info(">> _check_1year")

    # datetime inicial
    ldt_ini = datetime.datetime.strptime(fdct_parms[df.DS_KEY_DTINI], "%Y%m%d%H")
    # datetime final
    ldt_fim = datetime.datetime.strptime(fdct_parms[df.DS_KEY_DTFIM], "%Y%m%d%H")

    # calcula a diferença entre datas
    ldt_diff = ldt_fim - ldt_ini
    # total number of seconds between dates
    lf_diff_in_s = ldt_diff.total_seconds()

    # duration in years (seconds in a year = 365*24*60*60 = 31536000)
    lf_years = lf_diff_in_s / 31536000

    if lf_years > 1:
        try:
            # add 1 year to initial date
            ldt_fim = ldt_ini.replace(year=ldt_ini.year + 1)

        # em caso de erro,...
        except ValueError:
            # preseve calendar day (if Feb 29th doesn't exist, set to 28th)
            ldt_fim = ldt_ini.replace(year=ldt_ini.year + years, day=28)

        # nova data final
        fdct_parms[df.DS_KEY_DTFIM] = ldt_fim.strftime("%Y%m%d") + "23"

        # logger
        M_LOG.warning("request ultrapassa 1 ano. Data: %s", str(fdct_parms[df.DS_KEY_DTFIM]))
        print("request ultrapassa 1 ano. Data:", str(fdct_parms[df.DS_KEY_DTFIM]))

# < the end >----------------------------------------------------------------------------------
