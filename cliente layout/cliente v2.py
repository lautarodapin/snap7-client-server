from snap7.client import Client
from snap7.util import *
from snap7.snap7exceptions import Snap7Exception
from snap7.snap7types import *
from extras import *
IP = '127.0.0.1'
PORT = 8088
RACK = 0
SLOT = 0
client = Client()
client.connect(IP, RACK, SLOT, PORT)
with open('lecturas/db_small_int.txt', 'r') as f:
    layout = f.read()

db_number = 0
all_data = client.db_get(db_number)

db1 = DB_mixin(
    db_number,              # the db we use
    all_data,               # bytearray from the plc
    layout,                 # layout specification DB variable data
    10,                   # size of the specification 17 is start
    3,                      # number of row's / specifications
)

[print(db) for db in db1]


'''
with open('lecturas/marcas.txt', 'r') as f:
    layout = f.read()
all_data = client.read_area(S7AreaMK, 0, 0, 10)
db2 = DB(
    0,              # the db we use
    all_data,               # bytearray from the plc
    layout,                 # layout specification DB variable data
    6+2,                   # size of the specification 17 is start
    1,                      # number of row's / specifications
)
[print(db) for db in db2]

'''