# -*- coding: utf-8 -*-
"""
api_gui

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import io
import json
import logging
import pathlib
import time
import unicodedata

# pandas
import pandas as pd

# streamlit
import streamlit as st

# local
import bdc_api.api_bdc as db
import bdc_api.api_defs as df

# < constants >--------------------------------------------------------------------------------

# shared labels
DS_LBL_VIEW = "View de dados:"
DS_LBL_PESQ = "Pesquisar"
DS_LBL_WAIT = "Aguarde..."

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def build_filename(fs_view: str, fs_loc: str, fs_data: str):
    """
    build file name

    :param fs_view (str): tipo de pesquisa
    :param fs_loc (str): localidade
    :param fs_data (str): data

    :returns: filename
    """
    # logger
    M_LOG.debug(">> build_filename")

    # filename
    ls_fname = f"{fs_view}_{fs_loc}_{fs_data_ini}"

    # convert to lowercase & replace spaces
    ls_fname = ls_fname.lower().replace(" ", "_")

    # remove accents
    ls_fname = ''.join(c for c in unicodedata.normalize("NFD", ls_fname)
                       if unicodedata.category(c) != "Mn")

    # return filename
    return ls_fname

# ---------------------------------------------------------------------------------------------
def out_file(f_dataframe, fs_fmt: str, fs_fname: str):
    """
    send output to file

    :param f_dataframe: dataframe
    :param fs_fmt (str): output format
    :param fs_fname (str): file name
    """
    # logger
    M_LOG.debug(">> out_file")

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

        # create a Pandas Excel Writer using XlsxWriter as the engine
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
def pag_altitude():
    """
    página de execução de dados de altitude
    """
    # logger
    M_LOG.debug(">> pag_altitude")

    # top image
    st.image("openbdc.jpg")

    # título da página
    st.title("Dados de Altitude")

    # seleção da view de dados
    ls_view = st.selectbox(DS_LBL_VIEW, df.DDCT_VIEWS_ALT.keys())
    
    # create parameters
    ldct_parm = {df.DS_KEY_VIEW: df.DDCT_VIEWS_ALT[ls_view]}
    
    # widget de localidade e data
    ls_midia, ls_fmt = wid_loc_dat(ldct_parm)

    # submit button
    lv_submit = st.button(DS_LBL_PESQ)

    if lv_submit:
        # show message
        with st.spinner(DS_LBL_WAIT):
            # submit query
            l_data = db.submit_query(ldct_parm)

        # saída em arquivo ?
        if df.DS_MID_ARQ == ls_midia:
            # build filename
            ls_fname = build_filename(ls_view, df.DDCT_LOCAL[ls_loc], ls_data_ini)
            M_LOG.debug("ls_fname: %s", ls_fname)

            # output to file
            out_file(l_data, ls_fmt, ls_fname)

        # senão,...
        else:
            # temperatura altitude nível padrão ?
            if "vwm_temperatura_altitude_nivelpadrao" == ldct_parm[df.DS_KEY_VIEW]:
                # convert multiple columns to float
                l_data = l_data.astype({"Temperatura": "float", "Umidade relativa": "int",
                                        "Ponto de orvalho": "float", "Altitude": "float"})
            # vento altitude nível padrão ?
            elif "vwm_vento_altitude_nivelpadrao" == ldct_parm[df.DS_KEY_VIEW]:
                # convert multiple columns to float
                l_data = l_data.astype({"Velocidade do vento": "float", "Altitude": "float"})

            # output to display
            st.write(l_data)

# ---------------------------------------------------------------------------------------------
def pag_superficie():
    """
    página de execução de dados de superfície
    """
    # logger
    M_LOG.debug(">> pag_superficie")

    # top image
    st.image("openbdc.jpg")

    # título da página
    st.title("Dados de Superfície")

    # seleção do tipo de dado
    ls_view = st.selectbox(DS_LBL_VIEW, df.DDCT_VIEWS_SUP.keys())

    # create parameters
    ldct_parm = {df.DS_KEY_VIEW: df.DDCT_VIEWS_ALT[ls_view]}
    
    # widget de localidade e data
    ls_midia, ls_fmt = wid_loc_dat(ldct_parm)
    
    # submit button
    lv_submit = st.button(DS_LBL_PESQ)

    if lv_submit:
        # show message
        with st.spinner(DS_LBL_WAIT):
            # submit query
            l_data = db.submit_query(ldct_parm)

        # saída em arquivo ?
        if df.DS_MID_ARQ == ls_midia:
            # build filename
            ls_fname = build_filename(ls_view, df.DDCT_LOCAL[ls_loc], ls_data_ini)
            M_LOG.debug("ls_fname: %s", str(ls_fname))

            # output to file
            out_file(l_data, ls_fmt, ls_fname)

        # senão,...
        else:
            # CGT ?
            if "vwm_unificado_cgt" == ldct_parm[df.DS_KEY_VIEW]:
                # ["Horário", "Aeródromo", "CGT 1", "CGT 2", "CGT 3"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))

            # precipitação ?                                                                            
            elif "vwm_unificado_precipitacao" == ldct_parm[df.DS_KEY_VIEW]:                                       
                # convert "Precipitação" from string to float
                l_data["Precipitação"] = l_data["Precipitação"].astype(float)

                # style format
                # l_data.style.format("{:.2f}")
                # l_data.style.format({"Precipitação": "{:.2f}"})
                                                                                                        
            # pressão ?                                                                                 
            elif "vwm_unificado_pressao" == ldct_parm[df.DS_KEY_VIEW]:                                          
                # convert multiple columns to float
                l_data = l_data.astype({"QNH": "float", "QFE": "float", "QFF": "float"})

                # style format
                # l_data.style.format("{:.2f}")
                # l_data.style.format(subset=["QNH"], formatter="{:.2f}")
                                                                                                        
            # RVR ?                                                                                     
            elif "vwm_unificado_rvr" == ldct_parm[df.DS_KEY_VIEW]:                                              
                # ["Horário", "Aeródromo", "Pista", "Teto"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))
                                                                                                        
            # temperatura ?                                                                             
            elif "vwm_unificado_temperatura" == ldct_parm[df.DS_KEY_VIEW]:                                      
                # convert multiple columns to float
                l_data = l_data.astype({"Bulbo seco": "float", "Bulbo úmido": "float",
                                        "Temperatura da pista": "float",
                                        "Temperatura do ponto de orvalho": "float"})
            # teto ?                                                                                    
            elif "vwm_unificado_teto" == ldct_parm[df.DS_KEY_VIEW]:                                             
                # ["Horário", "Aeródromo", "Pista", "Teto"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))

            # vento ?                                                                                   
            elif "vwm_unificado_vento" == ldct_parm[df.DS_KEY_VIEW]:                                            
                # ["Horário", "Aeródromo", "Cabeceira", "Velocidade do vento", "Direção do vento", "Rajada"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))
                                                                                                        
            # visibilidade ?                                                                            
            elif "vwm_unificado_visibilidade" == ldct_parm[df.DS_KEY_VIEW]:                                     
                # ["Horário", "Aeródromo", "Direção visibilidade mínima", "Visibilidade mínima", "Visibilidade predominante"]
                M_LOG.debug("df.dtypes: %s", str(l_data.dtypes))

            # output to display
            st.write(l_data)

# ---------------------------------------------------------------------------------------------
def wid_loc_dat(fdct_parm: dict):
    """
    widgets de localidade, data, mídia e formato de saída

    :param fdct_parm (dict): parâmetros

    :returns: mídia e formato de saída
    """
    # logger
    M_LOG.info(">> wid_loc_dat")

    # seleção da localidade
    ls_loc = st.selectbox("Localidade:", df.DDCT_LOCAL.keys())
    # update parameters
    fdct_parm[df.DS_KEY_LOCAL] = df.DDCT_LOCAL[ls_loc]

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
    fdct_parm[df.DS_KEY_DTINI] = ldt_ini.strftime("%Y%m%d") + "{:02d}".format(li_hora_ini)
    # data final
    fdct_parm[df.DS_KEY_DTFIM] = ldt_fim.strftime("%Y%m%d") + "{:02d}".format(li_hora_fim)

    # return mídia & formato de saída
    return ls_midia, ls_fmt

# ---------------------------------------------------------------------------------------------
def main():
    """
    drive app
    """
    # logger
    M_LOG.info(">> main")

    # app title
    st.sidebar.title("OpenBDC")
    # app selection
    ls_pg_sel = st.sidebar.selectbox("Selecione a pesquisa", DLST_PESQUISA)

    # dados de altitude ?
    if df.DS_PSQ_ALT == ls_pg_sel:
        # call BDC page
        pag_altitude()

    # dados de superfície ?
    elif df.DS_PSQ_SUP == ls_pg_sel:
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
