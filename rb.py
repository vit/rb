# -*- coding: utf-8 -*-

import numpy as np

#from ctypes import *
#from os import getcwd, _exit
#import sys
import time
import os

from datetime import datetime
from threading import Timer


from tc.connector import Connector


login = os.environ['RB_LOGIN']
password = os.environ['RB_PASSWORD']

conn = Connector(login, password)

def on_tick():
    print "got tick:"
    print datetime.today()
    conn.get_history_data('TQBR', 'SBER', period=1, count=15)

try:
    conn.disconnect()
    time.sleep(2)
    conn.connect()
    #time.sleep(5)
    #print conn.send_command({'id': "server_status"})
    print("*"*50)
    #print conn.get_portfolio({'client': "FZTC8450A"})

    #time.sleep(3)

#    conn.get_securities()

    time.sleep(5)
    #conn.get_history_data('TQBR', 'SBER', period=1, count=15)
    conn.subscribe('TQBR', 'SBER')
    #conn.get_servtime_difference()

    jobs = []
    current_time=datetime.today()
    current_minute = current_time.minute
    final_time = current_time.replace(hour=18, minute=45, second=0)
    #job_time = current_time.replace(minute=current_minute+1, second=45)
    job_time = current_time.replace(minute=current_minute+1, second=50)
    while job_time < final_time:
        #jobs.append(job_time)
        job_timer = Timer( (job_time-current_time).seconds, on_tick )
        job_timer.daemon = True
        job_timer.start()
        jobs.append( job_timer )
        next_minute = (job_time.minute+1) % 60
        next_hour = job_time.hour + int((job_time.minute+1) // 60)
        job_time = job_time.replace( minute=next_minute, hour=next_hour )
    #print(">"*50)
    #print(jobs)
    #print(len(jobs))
    #print("<"*50)


    #conn.disconnect()
except KeyboardInterrupt:
    print("W: interrupt received")
except Exception as e:
    print(e)

while True:
    time.sleep(1)

