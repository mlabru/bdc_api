# -*- coding: utf-8 -*-
"""
api_bdc

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import typing

# pandas
import pandas as pd

# postgres
import psycopg2

# local
import bdc_api.api_defs as df

# < logging >----------------------------------------------------------------------------------

M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.ERROR)

# ---------------------------------------------------------------------------------------------
def connect_bdc(fs_user: typing.Optional[str] = df.DS_BDC_USER,
                fs_pass: typing.Optional[str] = df.DS_BDC_PASS,
                fs_host: typing.Optional[str] = df.DS_BDC_HOST,
                fs_db: typing.Optional[str] = df.DS_BDC_DB):
    """
    connect to BDC

    :param fs_user (str): BDC user
    :param fs_pass (str): password
    :param fs_host (str): host
    :param fs_db (str): database

    :returns: BDC connections
    """
    # logger
    M_LOG.info(">> connect_bdc")

    # create connection
    l_bdc = psycopg2.connect(host=fs_host, database=fs_db, user=fs_user, password=fs_pass)
    assert l_bdc

    # return BDC connection
    return l_bdc

# ---------------------------------------------------------------------------------------------
def get_as_df(f_bdc, fs_query: str, flst_columns: list) -> pd.DataFrame:
    """
    get dataframe from BDC

    :param f_bdc: conexão com o BDC
    :param fs_query: query
    :param flst_columns: lista de títulos das colunas
    """
    # logger
    M_LOG.info(">> get_as_df")

    # create cursor
    l_cursor = f_bdc.cursor()
    assert l_cursor

    # execute query
    l_cursor.execute(fs_query)

    # convert to dataframe
    ldf_data = pd.DataFrame(l_cursor.fetchall(), columns=flst_columns)

    # set index
    ldf_data.set_index(flst_columns[0], drop=False)

    # return dataframe
    return ldf_data

# ---------------------------------------------------------------------------------------------
def get_from_bdc(f_bdc, fdct_parm: dict) -> pd.DataFrame:
    """
    get dataframe from BDC

    :param f_bdc: conexão com o BDC
    :param fdct_parm (str): query parameters
    """
    # logger
    M_LOG.info(">> get_from_bdc")

    # check input
    assert fdct_parm["view"] in list(df.DDCT_VIEWS.values())

    # data inicial
    ls_data_ini = fdct_parm["ini"]
    ls_data_ini = "{}-{}-{} {}:00".format(ls_data_ini[:4], 
                                          ls_data_ini[4:6],
                                          ls_data_ini[6:8],
                                          ls_data_ini[8:10])

    # data final
    ls_data_fim = fdct_parm["fim"]
    ls_data_fim = "{}-{}-{} {}:59".format(ls_data_fim[:4], 
                                          ls_data_fim[4:6],
                                          ls_data_fim[6:8],
                                          ls_data_fim[8:10])

    # precipitação ?
    if "vwm_unificado_precipitacao" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, durpreci, precip"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Duração", "Precipitação"]

    # pressão ?
    elif "vwm_unificado_pressao" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, qnh, qfe, qff, tendpressao, alt850hpa"
        # headers
        llst_headers = ["Horário", "Aeródromo", "QNH", "QFE", "QFF",
                        "Tendência da pressão", "Altitude 850hpa"]

    # RVR ?
    elif "vwm_unificado_rvr" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, cabeceira, rvr"
        # headers
        llst_headers = ["Horário", "Cabeceira", "RVR"]

    # temperatura ?
    elif "vwm_unificado_temperatura" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, pista, bseco, bumido, ur, temppista, temppo"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Pista", "Bulbo seco", "Bulbo úmido",
                        "Umidade relativa", "Temperatura da pista",
                        "Temperatura do ponto de orvalho"]

    # teto ?
    elif "vwm_unificado_teto" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, pista, teto"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Pista", "Teto"]

    # vento ?
    elif "vwm_unificado_vento" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, cabeceira, velvento, dirvento, rajada"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Cabeceira", "Velocidade do vento",
                        "Direção do vento", "Rajada"]

    # visibilidade ?
    elif "vwm_unificado_visibilidade" == fdct_parm["view"]:
        # colunas
        ls_columns = "hora_observacao, sigla, dirvisibmin, visibmin, visibpre"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Direção visibilidade mínima",
                        "Visibilidade mínima", "Visibilidade predominante"]

    # make query
    # pylint: disable=duplicate-string-formatting-argument, consider-using-f-string
    ls_query = "SELECT {} "\
               "FROM {} "\
               "WHERE sigla = '{}' "\
               "AND hora_observacao BETWEEN '{}' AND '{}'".format(
               ls_columns, fdct_parm["view"], fdct_parm["local"],
               ls_data_ini, ls_data_fim)               
    M_LOG.debug("ls_query: %s", str(ls_query))

    # return data as dataframe        
    return get_as_df(f_bdc, ls_query, llst_headers)
    
# < the end >----------------------------------------------------------------------------------
