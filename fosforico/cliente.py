#!/usr/bin/python3
import logging
import os
BASE_DIR = "/home/pi/Documents/snap7-client-server/fosforico"
import time
logging.basicConfig(level=logging.DEBUG, filename=os.path.join(BASE_DIR, 'info', 'log-{}.log'.format(int(time.time()))))
from snap7.client import Client
from snap7.util import *
from snap7.snap7types import *#types import *
from snap7.snap7exceptions import *#exceptions import *
from extras import *
import csv
from datetime import datetime
#import schedule
IP = '127.0.0.1' # ip del plc
PORT = 102 #default is 102
RACK = 0
SLOT = 0
DB = 14 # numero de DB que se tiene que leer
DELAY = 60 * 15 # es en segundos, 60 * 60 * 1 = 1 hora | corro la funcion cada 15 minutos por si falla en obtneer datos, no deberia haber datos dobles.
LONGITUD_STRUCT = 48 #longitud del struct en el offset es 46.0 + 2bytes del ultimo int
LONGITUD_ARRAY = 1000 #longitud del array
LONGITUD_MARCAS = 914 #longitud del DB0 -> marcas MW912 -> entonces leo hasta el 912 + 2 bytes
LAYOUT = 'layout config/db14.txt'
LAYOUT_MARCA = 'layout config/marcas fosforico.txt'

LOG_FILE = 'log-{}.csv'.format(int(time.time())) # formato del csv log-150240240.csv
INDEX = (None,None)
def write_csv(dictionary):
    lista = [valor for variable, valor in dictionary.items()]
    with open(os.path.join(BASE_DIR ,'logs', LOG_FILE), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(lista) 
        
def reconect(client):
    while not client.get_connected():
        try:
            client.connect(IP, RACK, SLOT, PORT)
            time.sleep(1)
        except Snap7Exception as e:
            continue
        except Exception as e:
            continue
        if client.get_connected():
            break
        time.sleep(5)
        
        

''' Lee los layout del DB 14 y de la marca '''
with open(os.path.join(BASE_DIR, LAYOUT), 'r')  as f:
    layout = f.read()
with open(os.path.join(BASE_DIR, LAYOUT_MARCA), 'r')  as f:
    layout_marca = f.read()


def main(client, db, marca):
    try:
        marca_data = client.read_area(S7AreaMK, 0, 0, LONGITUD_MARCAS)
        marca = DB_mixin(0, marca_data, layout_marca, LONGITUD_MARCAS, 1)
        indice = marca[0]['index']
        INDEX[0] = indice
        _db = db[indice]
        _db.read(client)
        if INDEX[0] != INDEX[1] or INDEX[0] is None: # verifico si paso de indic para no repetir
            write_csv(_db.export())
            INDEX[1] = INDEX[0]
    except:
        print('Funcion fallo')



if __name__ == "__main__":
        
    client = Client()
    reconect(client)

    db_data = client.db_get(DB)
    marca_data = client.read_area(S7AreaMK, 0, 0, LONGITUD_MARCAS)

    db = DB_mixin(DB, db_data, layout, LONGITUD_STRUCT, LONGITUD_ARRAY)
    marca = DB_mixin(0, marca_data, layout_marca, LONGITUD_MARCAS, 1)

    #schedule.every(DELAY).seconds.do(main, client=client, db=db, marca=marca)

    while True:
        try:
            if not client.get_connected():
                reconect(client)
            time.sleep(DELAY)
            main(client=client, db=db, marca=marca)
            #schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break

