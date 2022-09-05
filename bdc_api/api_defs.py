# -*- coding: utf-8 -*-
"""
api_defs

2022.aep  mlabru  initial version (Linux/Python)
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
DS_HOST = os.getenv("DS_HOST")
DS_USER = os.getenv("DS_USER")
DS_PASS = os.getenv("DS_PASS")
DS_DB = os.getenv("DS_DB")

# < defines >----------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.DEBUG

# < the end >----------------------------------------------------------------------------------
