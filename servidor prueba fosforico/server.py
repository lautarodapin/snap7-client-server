import snap7
import time
import logging
import ctypes
from snap7.util import *
from extras import *
from snap7 import snap7types
import csv
import pandas as pd
logging.basicConfig(level=logging.INFO)

server = snap7.server.Server()


areas = pd.read_csv('server config/server areas.csv')
AREAS = {}
for i in range(0, len(areas)):
    area = getattr(snap7types, areas.iloc[i,0])
    numero = areas.iloc[i,1]
    nombre = areas.iloc[i,2]
    size = areas.iloc[i,3]
    AREAS[nombre]= (snap7types.wordlen_to_ctypes[snap7types.S7WLByte]*size)()
    server.register_area(area, int(numero), AREAS[nombre])

server.start(tcpport=8088)


valores = pd.read_csv('server config/valores.csv')
for i in range(0, len(valores)):
    variable = valores.iloc[i,0]
    funcion = valores.iloc[i,1]
    byte = int(valores.iloc[i,2])
    bit = int(valores.iloc[i,3])
    valor = int(valores.iloc[i,4])

    if 'bool' in funcion:
        # getattr(globals(), funcion)(AREAS[variable], byte, bit, valor)
        globals()[funcion](AREAS[variable], byte, bit, valor)
    else:
        # getattr(globals(), funcion)(AREAS[variable], byte, valor)
        globals()[funcion](AREAS[variable], byte, valor)
    

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