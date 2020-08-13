import logging
logging.basicConfig(level=logging.INFO)

from snap7.client import Client
from snap7 import snap7types
from snap7.snap7exceptions import Snap7Exception
from snap7 import util
import time
import datetime
import pandas as pd
import csv
DELAY = 1 #delay si se desconecta del plc, el tiempo en segundos que espera en volver a tratar de conectar
IP = '127.0.0.1'
RACK = 0
SLOT = 0
PORT = 8088 #default is 102



DBS = {}
DATE = datetime.datetime.now().strftime('%H,%M,%S %d-%m-%y')
FILE = f'records/log-{DATE}.log'
with open(FILE, 'w') as f:
    f.write('')

def guardar_datos(datos):
    ''' Guarda los datos en un archivo csv con la fecha en formato timestamp'''
    with open(FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(datos)
    

def leer_datos():
    ''' Lee el archivo bloques, que debe estar compuesto por el Area a leer, el numero del DB, el nombre de la variable donde se almacena en python
    Y la longitud del DB
    
    Areas: apuntan a las areas de memoria del plc, el nombre debe ser identico en el csv.
        * S7AreaPE = 0x81
        * S7AreaPA = 0x82
        * S7AreaMK = 0x83
        * S7AreaDB = 0x84
        * S7AreaCT = 0x1C
        * S7AreaTM = 0x1D

    >>> DB1.DBX10.1 -> area=S7AreaDB, numero=1, nombre='db1', longitud=11
     '''
    dbs = pd.read_csv('client config/bloques.csv')
    for i in range(0, len(dbs)):
        area = dbs.iloc[i,0]
        numero = dbs.iloc[i,1]
        nombre = dbs.iloc[i,2]
        longitud = dbs.iloc[i,3]
        DBS[nombre] = plc.read_area(getattr(snap7types, area), int(numero), 0, int(longitud))

def leer_variables():
    ''' Lee el archivo los valores que se deben leer de los DBs previamente leidos y almacenados en la variable. 
    Segun el tipo de variable es la funcion que debe indicarse.
    
    Funciones:
        * get_bool
        * get_int
        * get_real
        * get_string
        * get_dword

    >>> DB1.DBX10.1 -> funcion = get_bool, byte = 10, bit = 1
    ''' 
    datos = pd.read_csv('client config/valores.csv')
    DATOS = []
    for i in range(0, len(datos)):
        nombre = datos.iloc[i, 0]
        funcion = datos.iloc[i, 1]
        byte = datos.iloc[i, 2]
        bit = datos.iloc[i, 3]

        if 'bool' in funcion:
            resultado = getattr(util, funcion)(**dict(
                    _bytearray=DBS[nombre],
                    byte_index=byte,
                    bool_index=bit
                ))
        else:
            resultado = getattr(util, funcion)(**dict(
                    _bytearray=DBS[nombre],
                    byte_index=byte,
                ))
        logging.info(f"{nombre} function={funcion} byte={byte}, bit={bit} resultado={resultado}")
        DATOS.append(resultado)
    return DATOS
if __name__ == "__main__":
    plc = Client()
    plc.connect(IP, RACK, SLOT, PORT)
    

    while True:
        try:
            while not plc.get_connected():
                try:
                    plc.connect(IP, RACK, SLOT, PORT)
                except Exception as e:
                    print(e)
                
            leer_datos()
            datos = leer_variables()
            guardar_datos(datos)
            time.sleep(DELAY)
        except KeyboardInterrupt:
            break
        except Snap7Exception:            
            while not plc.get_connected():
                try:
                    plc.connect(IP, RACK, SLOT, PORT)
                except Exception as e:
                    print(e)