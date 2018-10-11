# -*- coding: utf-8 -*-

import numpy as np

from ctypes import *
import os
#import dicttoxml
#import xmltodict
import time
import xml.etree.ElementTree as ET

callback_func = WINFUNCTYPE(c_bool, c_char_p)

@callback_func
def callback(msg):
    root = ET.fromstring(msg)
    #print("root: %s" % root.tag)
    if root.tag=="server_status":
        print("server_status:")
        print(msg)
    elif root.tag=="error":
        print("error:")
        print(msg)
    elif root.tag=='securities':
        #print("root: %s" % root.tag)
        #'''
        for child in root:
            seccode = child.find('seccode').text
            if seccode=="SBER":
                print("!!!!! %s" % seccode)
                for child_2 in child:
                    print child_2.tag, child_2.attrib, child_2.text
        #'''
    #data = xml_to_dict(msg)
    #if "portfolio_tplus" in msg:
    #    print("callback:")
    #    print(msg)
    #if "candlekinds" in msg:
    #    print("candlekinds:")
    #    print(msg)
    if "candles" in msg:
        print("candles:")
        print(msg)
    #    print(data)
    """
    Функция, вызываемая коннектором при входящих сообщениях.
    :param msg:
        Входящее сообщение Транзака.
    :return:
        True если все обработал.
    """
    '''
    obj = parse(msg.decode('utf8'))
    if isinstance(obj, Error):
        log.error(u"Траблы: %s" % obj.text)
        raise TransaqException(obj.text.encode(encoding))
    elif isinstance(obj, ServerStatus):
        log.info(u"Соединен с серваком: %s" % obj.connected)
        if obj.connected == 'error':
            log.warn(u"Ёпта, ошибка соединения: %s" % obj.text)
        log.debug(obj)
    else:
        log.info(u"Получил объект типа %s" % str(type(obj)))
        log.debug(obj)
    if global_handler:
        global_handler(obj)
    '''
    return True

class Connector:
    def __init__(self, login, password):
        self.logsdir = "./logs"
        self.loglevel = 3

        self.ip = "78.41.199.12"
        self.port = 3900
        self.rqdelay = 120
        self.session_timeout = 10
        self.request_timeout = 5

        self.login = login
        self.password = password

        dllfilename = os.path.dirname(os.path.abspath(__file__))+"/dll/x64/txmlconnector64.dll"

        #self.txml = WinDLL("./tc/dll/x64/txmlconnector64.dll")
        self.txml = WinDLL(dllfilename)
        _res = None
        try:
            _res = self.txml.Initialize(self.logsdir, self.loglevel)
        except:
            print("!!! Initialize error !!!")

        print("!!! Initialize res: >>>%s<<< !!!" % _res)

        if not self.txml.SetCallback(callback):
            raise Exception(u"Коллбэк не установился")


    def connect(self):
        rez = self.txml.SendCommand('''
            <command id="connect">
                <login>%(login)s</login>
                <password>%(password)s</password>
                <host>%(host)s</host>
                <port>%(port)s</port>
                <language>en</language>
                <autopos>true</autopos>
                <rqdelay>%(rqdelay)s</rqdelay>
                <session_timeout>%(session_timeout)s</session_timeout>
                <request_timeout>%(request_timeout)s</request_timeout>
                <push_pos_equity>0</push_pos_equity>
            </command>
            ''' % ({
                'login': self.login,
                'password': self.password,
                'host': self.ip,
                'port': self.port,
                'rqdelay': self.rqdelay,
                'session_timeout': self.session_timeout,
                'request_timeout': self.request_timeout,
                })
            )
        rez_str = string_at(rez)
        print("connect: %s" % rez_str)
        #ret = rez_str and 'true' in rez_str
        #self.txml.FreeMemory(rez)
        #return ret
        return True

    def disconnect(self):
        rez = self.txml.SendCommand('''<command id="disconnect"/>''')
        rez_str = string_at(rez)
        print("disconnect: %s" % rez_str)
        #ret = rez_str and 'true' in rez_str
        #self.txml.FreeMemory(rez)
        #return ret
        return True

    def get_securities(self):
        rez = self.txml.SendCommand('''<command id="get_securities"/>''')
        rez_str = string_at(rez)
        print("get_securities: %s" % rez_str)
        #ret = rez_str and 'true' in rez_str
        #self.txml.FreeMemory(rez)
        #return ret
        return True

    def get_portfolio(self, client):
        rez = self.txml.SendCommand("<command id='get_portfolio' client='%s'></command>" % client)
        self.txml.FreeMemory(rez)
        return True

    def get_history_data(self, board, seccode, period=1, count=10, reset=True):
        rez = self.txml.SendCommand('''
            <command id="gethistorydata">
                <security>
                    <board>%(board)s</board>
                    <seccode>%(seccode)s</seccode>
                </security>
                <period>%(period)s</period>
                <count>%(count)s</count>
                <reset>true</reset>
            </command>
            ''' % ({
                'board': board,
                'seccode': seccode,
                'period': period,
                'count': count,
                'reset': True #reset
                })
            #    <reset>%(reset)s</reset>
        )
        rez_str = string_at(rez)
        print("get_history_data: %s" % rez_str)
        #self.txml.FreeMemory(rez)
        return True

