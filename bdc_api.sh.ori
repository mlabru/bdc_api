#!/bin/bash

# language
# export LANGUAGE=pt_BR

# BDC API directory
BDC_API=~/bdc_api

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M'`

# home directory exists ?
if [ -d ${BDC_API} ]; then
    # set home dir
    cd ${BDC_API}
fi

# set PYTHONPATH
export PYTHONPATH="$PWD/."

# ckeck if another instance os bdc_api is running
DI_PID_API=`ps ax | grep -w python3 | grep -w api_run.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_API" ]; then
    # log warning
    echo "[`date`]: process bdc_api is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_API
    # wait 3s
    sleep 3
fi

# log warning
echo "[`date`]: starting process api_run..."
# executa a aplicação (-OO)
python3 bdc_api/api_run.py > logs/api_run.$HOST.$TDATE.log 2>&1 &

# ckeck if another instance os bdc_api is running
DI_PID_GUI=`ps ax | grep -w streamlit | grep -w api_gui.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_GUI" ]; then
    # log warning
    echo "[`date`]: process api_gui is already running. Restarting..."
    # kill process
    kill -9 $DI_PID_GUI
    # wait 3s
    sleep 3
fi

# log warning
echo "[`date`]: starting process api_gui..."
# executa a aplicação (-OO)
streamlit run bdc_api/api_gui.py > logs/api_gui.$HOST.$TDATE.out 2>&1 &

# < the end >----------------------------------------------------------------------------------
