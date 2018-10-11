# -*- coding: utf-8 -*-

import numpy as np

#from ctypes import *
#from os import getcwd, _exit
#import sys
import time
import os

from tc.connector import Connector


login = os.environ['RB_LOGIN']
password = os.environ['RB_PASSWORD']

conn = Connector(login, password)

try:
    #conn.disconnect()
    #time.sleep(3)
    conn.connect()
    time.sleep(5)
    #print conn.send_command({'id': "server_status"})
    print("*"*50)
    #print conn.get_portfolio({'client': "FZTC8450A"})

    #time.sleep(3)

#    conn.get_securities()
    conn.get_history_data('TQBR', 'SBER', period=1, count=10)

    time.sleep(5)

    conn.disconnect()

except Exception as e:
    print(e)


