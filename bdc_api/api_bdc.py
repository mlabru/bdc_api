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
def _connect_db(fs_user: typing.Optional[str] = df.DS_BDC_USER,
                fs_pass: typing.Optional[str] = df.DS_BDC_PASS,
                fs_host: typing.Optional[str] = df.DS_BDC_HOST,
                fs_db: typing.Optional[str] = df.DS_BDC_DB):
    """
    connect to BDC

    :param fs_user (str): BDC user
    :param fs_pass (str): password
    :param fs_host (str): host
    :param fs_db (str): database

    :returns: BDC connection
    """
    # logger
    M_LOG.info(">> _connect_db")

    # create connection
    l_bdc = psycopg2.connect(host=fs_host, database=fs_db, user=fs_user, password=fs_pass)
    assert l_bdc

    # return BDC connection
    return l_bdc

# ---------------------------------------------------------------------------------------------
def _get_as_df(f_bdc, fs_query: str, flst_columns: list) -> pd.DataFrame:
    """
    get dataframe from BDC

    :param f_bdc: conexão com o BDC
    :param fs_query: query
    :param flst_columns: lista de títulos das colunas

    :returns: dataframe com resultado da pesquisa no banco
    """
    # logger
    M_LOG.info(">> _get_as_df")

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
def _get_from_db(f_bdc, fdct_parm: dict) -> pd.DataFrame:
    """
    get dataframe from BDC

    :param f_bdc: conexão com o BDC
    :param fdct_parm (str): query parameters

    :returns: dataframe com resultado da pesquisa no banco
    """
    # logger
    M_LOG.info(">> _get_from_db")

    # check input
    assert fdct_parm[df.DS_KEY_VIEW] in list(df.DDCT_VIEWS.values())

    # data inicial
    ls_data_ini = fdct_parm[df.DS_KEY_DTINI]
    ls_data_ini = "{}-{}-{} {}:00".format(ls_data_ini[:4], 
                                          ls_data_ini[4:6],
                                          ls_data_ini[6:8],
                                          ls_data_ini[8:10])

    # data final
    ls_data_fim = fdct_parm[df.DS_KEY_DTFIM]
    ls_data_fim = "{}-{}-{} {}:59".format(ls_data_fim[:4], 
                                          ls_data_fim[4:6],
                                          ls_data_fim[6:8],
                                          ls_data_fim[8:10])

    # temperatura altitude nível padrão ?
    if "vwm_temperatura_altitude_nivelpadrao" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "data_hora_observacao"
        # colunas
        ls_columns = "data_hora_observacao, sigla, minuto_sondagem, segundo_sondagem, "\
                     "temperatura, umidade_relativa, ponto_orvalho, altitude, pressao"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Minuto", "Segundo", "Temperatura",
                        "Umidade relativa", "Ponto de orvalho", "Altitude", "Pressão"]

    # CGT ?
    elif "vwm_unificado_cgt" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, cgt_1, cgt_2, cgt_3"
        # headers
        llst_headers = ["Horário", "Aeródromo", "CGT 1", "CGT 2", "CGT 3"]

    # precipitação
    elif "vwm_unificado_precipitacao" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, durpreci, precip"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Duração", "Precipitação"]

    # pressão ?
    elif "vwm_unificado_pressao" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, qnh, qfe, qff, tendpressao, alt850hpa"
        # headers
        llst_headers = ["Horário", "Aeródromo", "QNH", "QFE", "QFF",
                        "Tendência da pressão", "Altitude 850hpa"]

    # RVR ?
    elif "vwm_unificado_rvr" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, cabeceira, rvr"
        # headers
        llst_headers = ["Horário", "Cabeceira", "RVR"]

    # temperatura ?
    elif "vwm_unificado_temperatura" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, pista, bseco, bumido, ur, temppista, temppo"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Pista", "Bulbo seco", "Bulbo úmido",
                        "Umidade relativa", "Temperatura da pista",
                        "Temperatura do ponto de orvalho"]

    # teto ?
    elif "vwm_unificado_teto" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, pista, teto"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Pista", "Teto"]

    # vento ?
    elif "vwm_unificado_vento" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, cabeceira, velvento, dirvento, rajada"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Cabeceira", "Velocidade do vento",
                        "Direção do vento", "Rajada"]

    # visibilidade ?
    elif "vwm_unificado_visibilidade" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "hora_observacao"
        # colunas
        ls_columns = "hora_observacao, sigla, dirvisibmin, visibmin, visibpre"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Direção visibilidade mínima",
                        "Visibilidade mínima", "Visibilidade predominante"]

    # vento altitude nível padrão ?
    elif "vwm_vento_altitude_nivelpadrao" == fdct_parm[df.DS_KEY_VIEW]:
        # key
        ls_key = "data_hora_observacao"
        # colunas
        ls_columns = "data_hora_observacao, sigla, minuto_sondagem, "\
                     "segundo_sondagem, velocidade_vento, direcao_vento, altitude, pressao"
        # headers
        llst_headers = ["Horário", "Aeródromo", "Minuto", "Segundo",
                        "Velocidade do vento", "Direção do Vento", "Altitude", "Pressão"]

    # make query
    # pylint: disable=duplicate-string-formatting-argument, consider-using-f-string
    ls_query = "SELECT {} "\
               "FROM {} "\
               "WHERE sigla = '{}' "\
               "AND {} BETWEEN '{}' AND '{}'".format(ls_columns,
               fdct_parm[df.DS_KEY_VIEW], fdct_parm[df.DS_KEY_LOCAL],
               ls_key, ls_data_ini, ls_data_fim)               

    # return data as dataframe        
    return _get_as_df(f_bdc, ls_query, llst_headers)
    
# ---------------------------------------------------------------------------------------------
def submit_query(fdct_parm: dict) -> pd.DataFrame:
    """
    submete a query ao banco de dados

    :param fdct_parm (dict): parâmetros

    :returns: dataframe com resultado da pesquisa no banco
    """
    # logger
    M_LOG.debug("submit_query >>")

    # connect BDC
    l_bdc = _connect_db()
    assert l_bdc

    # query BDC
    ldf_data = _get_from_db(l_bdc, fdct_parm)

    # close connection
    l_bdc.close()

    # return dataframe
    return ldf_data

# < the end >----------------------------------------------------------------------------------
