# -*- coding: utf-8 -*-

import numpy as np

from ctypes import *
import os
#import dicttoxml
#import xmltodict
import time
import xml.etree.ElementTree as ET
from datetime import datetime


quotation = {}


def predict_buy(data):
    #return model_buy.predict(data)[0]
    return False
def predict_buy_close(data):
    #return model_buy_close.predict(data)[0]
    return False


def on_candles(candles):
    print("candles:")
    print candles
    print datetime.today()
    close_p = [c['close'] for c in candles]
    close_p.append(quotation['last'])

    do_buy = predict_buy(close_p)
    do_buy_close = predict_buy_close(close_p)
    if do_buy:
        pass
    elif do_buy_close:
        pass

    print close_p
    print quotation

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
    elif root.tag=="quotations":
        #print("quotations:")
        #print(msg)
        qq = parse_quotations(msg)
        quotation.update(qq[0])
        print quotation
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
    if "candles" in msg:
        #print("candles:")
        #print(msg)
        candles = parse_candles(msg)
        on_candles(candles)
    return True

def parse_candles(msg):
    root = ET.fromstring(msg)
    candles = []
    for child in root:
        #child.attrib['close']
        attr = child.attrib
        attr['low'] = float(attr['low'])
        attr['high'] = float(attr['high'])
        attr['open'] = float(attr['open'])
        attr['close'] = float(attr['close'])
        attr['volume'] = int(attr['volume'])
        attr['date'] = datetime.strptime(attr['date'], '%d.%m.%Y %H:%M:%S')
        candles.append(attr)
        #seccode = child.find('seccode').text
        #if seccode=="SBER":
    return candles

def parse_quotations(msg):
    root = ET.fromstring(msg)
    qlst = []
    for child in root:
        q = {}
        vv = child.findtext('last')
        if vv:
           q['last'] = float(vv)

        vv = child.findtext('bid')
        if vv:
           q['bid'] = float(vv)
        vv = child.findtext('offer')
        if vv:
           q['offer'] = float(vv)

        vv = child.findtext('numbids')
        if vv:
           q['numbids'] = int(vv)
        vv = child.findtext('numoffers')
        if vv:
           q['numoffers'] = int(vv)
        vv = child.findtext('biddepth')
        if vv:
           q['biddepth'] = int(vv)
        vv = child.findtext('offerdepth')
        if vv:
           q['offerdepth'] = int(vv)

        vv = child.findtext('biddepth')
        if vv:
           q['biddepth'] = int(vv)
        vv = child.findtext('time')
        if vv:
           q['time'] = (vv)

        vv = child.findtext('tradingstatus')
        if vv:
           q['tradingstatus'] = (vv)
        vv = child.findtext('status')
        if vv:
           q['status'] = (vv)

        vv = child.findtext('buydeposit')
        if vv:
           q['buydeposit'] = float(vv)
        vv = child.findtext('selldeposit')
        if vv:
           q['selldeposit'] = float(vv)


        qlst.append(q)
        #print q
    return qlst


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

    def get_servtime_difference(self):
        rez = self.txml.SendCommand('''<command id="get_servtime_difference"/>''')
        rez_str = string_at(rez)
        print("get_servtime_difference: %s" % rez_str)
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

    def subscribe(self, board, seccode):
        rez = self.txml.SendCommand('''
            <command id="subscribe">
                <!--alltrades>
                    <security>
                        <board>%(board)s</board>
                        <seccode>%(seccode)s</seccode>
                    </security>
                </alltrades-->
                <quotations>
                    <security>
                        <board>%(board)s</board>
                        <seccode>%(seccode)s</seccode>
                    </security>
                </quotations>
                <!--quotes>
                    <security>
                        <board>%(board)s</board>
                        <seccode>%(seccode)s</seccode>
                    </security>
                </quotes-->
            </command>
            ''' % ({
                'board': board,
                'seccode': seccode
                })
            #    <reset>%(reset)s</reset>
        )
        rez_str = string_at(rez)
        print("subscribe: %s" % rez_str)
        #self.txml.FreeMemory(rez)
        return True

