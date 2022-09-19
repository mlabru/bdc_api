# -*- coding: utf-8 -*-
"""
api_defs

2022.sep  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os

# dotenv
import dotenv

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# DB connection
DS_BDC_HOST = os.getenv("DS_BDC_HOST")
DS_BDC_USER = os.getenv("DS_BDC_USER")
DS_BDC_PASS = os.getenv("DS_BDC_PASS")
DS_BDC_DB = os.getenv("DS_BDC_DB")

# API keys
DLST_API_KEYS = os.getenv("DLST_API_KEYS")

# < constants >--------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.WARNING

# tipo de pesquisa
DS_PSQ_ALT = "Dados de Altitude"
DS_PSQ_SUP = "Dados de Superfície"

# tipos de pesquisa válidos
DLST_PESQUISA = [DS_PSQ_ALT, DS_PSQ_SUP]

# formatos de saída
DS_FMT_CSV = "CSV"
DS_FMT_XLS = "Excel"
DS_FMT_JSON = "JSON"

# formatos de saída válidos
DLST_FORMATS = [DS_FMT_CSV, DS_FMT_XLS, DS_FMT_JSON]

# mídias de saída
DS_MID_ARQ = "Arquivo"
DS_MID_DSP = "Tela"

# mídias de saída válidos
DLST_MIDIAS = [DS_MID_ARQ, DS_MID_DSP]

# data keys
DS_KEY_API = "api_key"
DS_KEY_DTFIM = "data_fim"
DS_KEY_DTINI = "data_ini"
DS_KEY_LOCAL = "local"
DS_KEY_VIEW = "view"

# views de dados de altitude
DDCT_VIEWS_ALT = {"Temperatura Altitude Nível Padrão": "vwm_temperatura_altitude_nivelpadrao",
                  "Vento Altitude Nível Padrão": "vwm_vento_altitude_nivelpadrao"}

# views de dados de superfície
DDCT_VIEWS_SUP = {"CGT": "vwm_unificado_cgt",
                  "Precipitação": "vwm_unificado_precipitacao",
                  "Pressão": "vwm_unificado_pressao",
                  "RVR": "vwm_unificado_rvr",
                  "Temperatura": "vwm_unificado_temperatura",
                  "Teto": "vwm_unificado_teto",
                  "Vento": "vwm_unificado_vento",
                  "Visibilidade": "vwm_unificado_visibilidade"}

# todas as views
DDCT_VIEWS = DDCT_VIEWS_ALT | DDCT_VIEWS_SUP

# lista de localidades
DDCT_LOCAL = {"Congonhas": "SBSP", 
              "Guarulhos": "SBGR", 
              "São José dos Campos": "SBSJ",
              "SBAA": "SBAA",
              "SBAC": "SBAC",
              "SBAE": "SBAE",
              "SBAF": "SBAF",
              "SBAN": "SBAN",
              "SBAR": "SBAR",
              "SBAT": "SBAT",
              "SBAX": "SBAX",
              "SBBE": "SBBE",
              "SBBG": "SBBG",
              "SBBH": "SBBH",
              "SBBI": "SBBI",
              "SBBP": "SBBP",
              "SBBR": "SBBR",
              "SBBU": "SBBU",
              "SBBV": "SBBV",
              "SBBW": "SBBW",
              "SBCA": "SBCA",
              "SBCB": "SBCB",
              "SBCC": "SBCC",
              "SBCF": "SBCF",
              "SBCG": "SBCG",
              "SBCH": "SBCH",
              "SBCI": "SBCI",
              "SBCJ": "SBCJ",
              "SBCN": "SBCN",
              "SBCO": "SBCO",
              "SBCP": "SBCP",
              "SBCR": "SBCR",
              "SBCT": "SBCT",
              "SBCX": "SBCX",
              "SBCY": "SBCY",
              "SBCZ": "SBCZ",
              "SBDB": "SBDB",
              "SBDN": "SBDN",
              "SBDO": "SBDO",
              "SBEG": "SBEG",
              "SBEK": "SBEK",
              "SBEN": "SBEN",
              "SBES": "SBES",
              "SBFI": "SBFI",
              "SBFL": "SBFL",
              "SBFN": "SBFN",
              "SBFZ": "SBFZ",
              "SBGL": "SBGL",
              "SBGO": "SBGO",
              "SBGV": "SBGV",
              "SBGW": "SBGW",
              "SBHT": "SBHT",
              "SBIC": "SBIC",
              "SBIH": "SBIH",
              "SBIL": "SBIL",
              "SBIP": "SBIP",
              "SBIZ": "SBIZ",
              "SBJA": "SBJA",
              "SBJD": "SBJD",
              "SBJE": "SBJE",
              "SBJI": "SBJI",
              "SBJP": "SBJP",
              "SBJR": "SBJR",
              "SBJU": "SBJU",
              "SBJV": "SBJV",
              "SBKG": "SBKG",
              "SBKP": "SBKP",
              "SBLB": "SBLB",
              "SBLE": "SBLE",
              "SBLJ": "SBLJ",
              "SBLO": "SBLO",
              "SBLP": "SBLP",
              "SBMA": "SBMA",
              "SBME": "SBME",
              "SBMG": "SBMG",
              "SBMK": "SBMK",
              "SBML": "SBML",
              "SBMM": "SBMM",
              "SBMN": "SBMN",
              "SBMO": "SBMO",
              "SBMQ": "SBMQ",
              "SBMT": "SBMT",
              "SBMY": "SBMY",
              "SBNF": "SBNF",
              "SBNM": "SBNM",
              "SBNT": "SBNT",
              "SBOI": "SBOI",
              "SBPA": "SBPA",
              "SBPB": "SBPB",
              "SBPF": "SBPF",
              "SBPG": "SBPG",
              "SBPJ": "SBPJ",
              "SBPK": "SBPK",
              "SBPL": "SBPL",
              "SBPP": "SBPP",
              "SBPS": "SBPS",
              "SBPV": "SBPV",
              "SBRB": "SBRB",
              "SBRD": "SBRD",
              "SBRF": "SBRF",
              "SBRJ": "SBRJ",
              "SBRP": "SBRP",
              "SBSC": "SBSC",
              "SBSG": "SBSG",
              "SBSL": "SBSL",
              "SBSM": "SBSM",
              "SBSN": "SBSN",
              "SBSO": "SBSO",
              "SBSR": "SBSR",
              "SBST": "SBST",
              "SBSV": "SBSV",
              "SBTA": "SBTA",
              "SBTD": "SBTD",
              "SBTE": "SBTE",
              "SBTF": "SBTF",
              "SBTG": "SBTG",
              "SBTK": "SBTK",
              "SBTT": "SBTT",
              "SBTU": "SBTU",
              "SBUA": "SBUA",
              "SBUG": "SBUG",
              "SBUL": "SBUL",
              "SBUR": "SBUR",
              "SBVC": "SBVC",
              "SBVG": "SBVG",
              "SBVH": "SBVH",
              "SBVT": "SBVT",
              "SBYS": "SBYS",
              "SBZM": "SBZM",
              "SDAG": "SDAG",
              "SDIY": "SDIY",
              "SNBR": "SNBR",
              "SNDV": "SNDV",
              "SNGI": "SNGI",
              "SNHS": "SNHS",
              "SNPD": "SNPD",
              "SNRU": "SNRU",
              "SNTF": "SNTF",
              "SNVB": "SNVB",
              "SNZR": "SNZR",
              "SSKW": "SSKW",
              "SSUM": "SSUM",
              "SWEI": "SWEI",
              "SWGN": "SWGN",
              "SWKO": "SWKO",
              "SWLC": "SWLC",
              "SWPI": "SWPI"}

# < the end >----------------------------------------------------------------------------------
