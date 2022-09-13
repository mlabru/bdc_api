# -*- coding: utf-8 -*-
"""
api_gui

2022.jun  mlabru  remove rabbitmq cause of timeout problems, remove graylog
2022.may  mlabru  rabbitmq connection timeout
2022.apr  mlabru  graylog log management
2021.nov  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import io
import json
import logging
import pathlib
import time

# pandas
import pandas as pd

# streamlit
import streamlit as st

# local
import bdc_api.api_bdc as db
import bdc_api.api_defs as df

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def pag_superficie():
    """
    página de execução do OpenBDC
    """
    # logger
    M_LOG.debug("pag_superficie >>")

    # top image
    st.image("openbdc.jpg")

    # título da página
    st.title("Dados de Superfície")

    # seleção do tipo de dado
    ls_view = st.selectbox("Tipo de dado:", df.DDCT_VIEWS.keys())

    # seleção da localidade
    ls_loc = st.selectbox("Localidade:", df.DDCT_LOCAL.keys())

    # cria 2 colunas
    lwd_col1, lwd_col2 = st.columns(2)

    # na coluna 1...
    with lwd_col1:
        # data início
        ldt_ini = st.date_input("Data Inicial (AAAA/MM/DD):",
                                min_value=datetime.date(2000, 1, 1),
                                max_value=datetime.datetime.now())
        # data final
        ldt_fim = st.date_input("Data Final (AAAA/MM/DD):",
                                min_value=datetime.date(2000, 1, 1),
                                max_value=datetime.datetime.now())
        # midia de saída
        ls_midia = st.selectbox("Mídia de saída:", df.DLST_MIDIAS)

    # na coluna 2...
    with lwd_col2:
        # hora início
        li_hora_ini = st.number_input("Hora Inicial:",
                                      min_value=0, max_value=23, format="%02d")
        # hora início
        li_hora_fim = st.number_input("Hora Final:",
                                      min_value=0, max_value=23, format="%02d",
                                      value=23)
        # saída em arquivo ?
        if df.DS_MID_ARQ == ls_midia:
            # formato de saída
            ls_fmt = st.selectbox("Formato de saída:", df.DLST_FORMATS)

        # senão,...
        else:
            # formato de saída padrão
            ls_fmt = df.DS_FMT_JSON

    # data início
    ls_data_ini = ldt_ini.strftime("%Y%m%d") + "{:02d}".format(li_hora_ini)
    # data final
    ls_data_fim = ldt_fim.strftime("%Y%m%d") + "{:02d}".format(li_hora_fim)

    # gera parâmetros
    ldct_parm = {"view": df.DDCT_VIEWS[ls_view], "local": df.DDCT_LOCAL[ls_loc],
                 "ini": ls_data_ini, "fim": ls_data_fim}

    # submit button
    lv_submit = st.button("Pesquisar")

    if lv_submit:
        # show message
        with st.spinner("Aguarde..."):
            # submit query
            l_data = submit_query(ldct_parm)

        # saída em arquivo ?
        if df.DS_MID_ARQ == ls_midia:
            # build filename
            ls_fname = "{}_{}_{}".format(ls_view, df.DDCT_LOCAL[ls_loc], 
                       ls_data_ini).lower().replace("ç", "c").replace("ã", "a")
            M_LOG.debug("ls_fname: %s", str(ls_fname))

            # output to file
            out_file(l_data, ls_fmt, ls_fname)

        # senão,...
        else:
            # precipitação ?                                                                            
            if "vwm_unificado_precipitacao" == ldct_parm["view"]:                                       
                # convert "Precipitação" from string to float
                l_data["Precipitação"] = l_data["Precipitação"].astype(float)
                # style format
                # l_data.style.format("{:.2f}")
                l_data.style.format({"Precipitação": "{:.2f}"})
                                                                                                        
            # pressão ?                                                                                 
            elif "vwm_unificado_pressao" == ldct_parm["view"]:                                          
                # convert multiple columns to float
                l_data = l_data.astype({"QNH": "float", "QFE": "float", "QFF": "float"})
                # style format
                # l_data.style.format("{:.2f}")
                l_data.style.format(subset=["QNH"], formatter="{:.2f}")
                                                                                                        
            # RVR ?                                                                                     
            elif "vwm_unificado_rvr" == ldct_parm["view"]:                                              
                # colunas                                                                               
                ls_columns = "hora_observacao, cabeceira, rvr"                                          
                                                                                                        
            # temperatura ?                                                                             
            elif "vwm_unificado_temperatura" == ldct_parm["view"]:                                      
                # convert multiple columns to float
                l_data = l_data.astype({"Bulbo seco": "float", "Bulbo úmido": "float",
                                        "Temperatura da pista": "float",
                                        "Temperatura do ponto de orvalho": "float"})

            # teto ?                                                                                    
            elif "vwm_unificado_teto" == ldct_parm["view"]:                                             
                # ["Horário", "Aeródromo", "Pista", "Teto"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))

            # vento ?                                                                                   
            elif "vwm_unificado_vento" == ldct_parm["view"]:                                            
                # ["Horário", "Aeródromo", "Cabeceira", "Velocidade do vento", "Direção do vento", "Rajada"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))
                                                                                                        
            # visibilidade ?                                                                            
            elif "vwm_unificado_visibilidade" == ldct_parm["view"]:                                     
                # ["Horário", "Aeródromo", "Direção visibilidade mínima", "Visibilidade mínima", "Visibilidade predominante"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))
            
            # output to display
            st.dataframe(l_data)

# ---------------------------------------------------------------------------------------------
def out_file(f_dataframe, fs_fmt: str, fs_fname: str):
    """
    send output to file

    :param f_dataframe: dataframe
    :param fs_fmt (str): output format
    :param fs_fname (str): file name
    """
    # logger
    M_LOG.debug("out_file >>")

    M_LOG.debug("head: %s", str(f_dataframe.head())) 

    # output CSV ?
    if df.DS_FMT_CSV == fs_fmt:
        # filename
        fs_fname += ".csv"
        # convert to CSV
        l_data = f_dataframe.to_csv(index=False).encode("utf-8")

    # output Excel ?
    elif df.DS_FMT_XLS == fs_fmt:
        # create buffer
        l_buffer = io.BytesIO()

        # create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter(l_buffer, engine="xlsxwriter") as l_writer:
            # write dataframe to worksheet
            f_dataframe.to_excel(l_writer, sheet_name=fs_fname)

            # output the excel file to the buffer
            l_writer.save()

            # download button
            st.download_button("Download", data=l_buffer,
                               file_name=fs_fname + ".xlsx",
                               mime="application/vnd.ms-excel")
        # return
        return
        
    # senão,...
    else:
        # filename
        fs_fname += ".json"
        # convert to JSON
        l_data = f_dataframe.to_json(orient="records", force_ascii=False)

    # ok ?
    if l_data:
        # download button
        lv_download = st.download_button("Download", l_data, file_name=fs_fname)

    # senão,...
    else:
        # show error message 
        st.error("Erro na geração do arquivo")

# ---------------------------------------------------------------------------------------------
def submit_query(fdct_parm: dict) -> pd.DataFrame:
    """
    gera o arquivo de configuração do job

    :param fdct_parm (dict): parâmetros
    """
    # logger
    M_LOG.debug("submit_query >>")

    # connect BDC
    l_bdc = db.connect_bdc()
    assert l_bdc

    M_LOG.debug("fdct_parm: %s", str(fdct_parm))

    # query BDC
    ldf_data = db.get_from_bdc(l_bdc, fdct_parm)
    M_LOG.debug("ldf_data: %s", str(ldf_data))

    # close connection
    l_bdc.close()

    # return
    return ldf_data

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.info("main >>")

    # app title
    st.sidebar.title("OpenBDC")
    # app selection
    ls_pg_sel = st.sidebar.selectbox("Selecione o aplicativo", ["Dados de Superfície"])

    # dados de superfície ?
    if "Dados de Superfície" == ls_pg_sel:
        # call BDC page
        pag_superficie()

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M",
                        format="%(asctime)s %(message)s",
                        level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxint)

    # run application
    main()

# < the end >----------------------------------------------------------------------------------
