import snap7
import time
import logging
from snap7 import util
from snap7.snap7types import *
import csv
import pandas as pd
logging.basicConfig(level=logging.INFO)

size = 10

df_init = pd.read_csv('configs/server init.csv').dropna()


server = snap7.server.Server()
globaldata = (wordlen_to_ctypes[S7WLByte]*size)()
outputs = (wordlen_to_ctypes[S7WLByte]*size)()
inputs = (wordlen_to_ctypes[S7WLByte]*size)()
dbs = (wordlen_to_ctypes[S7WLByte]*size)()

server.register_area(srvAreaPA, 0, outputs)
server.register_area(srvAreaMK, 0, globaldata)
server.register_area(srvAreaPE, 0, inputs)
server.register_area(srvAreaDB, 0, dbs)

server.start(tcpport=8088)

util.set_real(outputs, 0, 1.234)      # srvAreaPA
util.set_real(globaldata, 0, 2.234)   # srvAreaMK
util.set_real(inputs, 0, 3.234)       # srvAreaPE
util.set_real(dbs, 0, 31.1)
util.set_bool(dbs, 1, 0, True)
while True:
    while True:
        event = server.pick_event()
        if event:
            print (server.event_text(event))
        else:
            break
        time.sleep(.01)
server.stop()
server.destroy()