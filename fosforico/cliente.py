from snap7.client import Client
from snap7.util import *
from snap7.snap7exceptions import Snap7Exception
from snap7.snap7types import *
from extras import *
import time
import csv
from datetime import datetime
import schedule
IP = '127.0.0.1' # ip del plc
PORT = 8088#102 #default is 102
RACK = 0
SLOT = 0
DB = 0#14 # numero de DB que se tiene que leer
DELAY = 60 * 60 * 1 # es en segundos, 60 * 60 * 1 = 1 hora
LONGITUD_STRUCT = 10#48 #longitud del struct en el offset es 46.0 + 2bytes del ultimo int
LONGITUD_ARRAY = 1000 #longitud del array
LONGITUD_MARCAS = 10#914 #longitud del DB0 -> marcas MW912 -> entonces leo hasta el 912 + 2 bytes
LAYOUT = 'layout config/db_test.txt'
LAYOUT_MARCA = 'layout config/marcas_test.txt'

LOG_FILE = 'log-{}.csv'.format(int(time.time())) # formato del csv log-150240240.csv

def write_csv(dictionary):
    lista = [valor for variable, valor in dictionary.items()]
    with open('logs/' + LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(lista) 
        
def reconect(client):
    while not client.get_connected():
        client.connect(IP, RACK, SLOT, PORT)
        if client.get_connected():
            break
        time.sleep(5)
        
        

''' Lee los layout del DB 14 y de la marca '''
with open(LAYOUT, 'r')  as f:
    layout = f.read()
with open(LAYOUT_MARCA, 'r')  as f:
    layout_marca = f.read()


def main(client, db, marca):
    marca[0].read(client)
    indice = marca[0]['index']
    _db = db[indice]
    _db.read(client)
    write_csv(_db.export())



if __name__ == "__main__":
        
    client = Client()
    reconect(client)

    db_data = client.db_get(DB)
    marca_data = client.read_area(S7AreaMK, 0, 0, LONGITUD_MARCAS)

    db = DB_mixin(DB, db_data, layout, LONGITUD_STRUCT, LONGITUD_ARRAY)
    marca = DB_mixin(0, marca_data, layout_marca, LONGITUD_MARCAS, 1)

    schedule.every(DELAY).seconds.do(main, client=client, db=db, marca=marca)

    while True:
        try:
            if not client.get_connected():
                reconect(client)
            
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break

