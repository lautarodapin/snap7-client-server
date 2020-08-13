import snap7
import ctypes
from snap7 import snap7types
from snap7.snap7exceptions import Snap7Exception
from snap7.common import check_error
from snap7 import util

import pandas as pd

IP = '127.0.0.1'
RACK = 0
SLOT = 0
PORT = 8088 #default is 102

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT, PORT)

valores = pd.read_csv('cliente v2 config/valores.csv')
data_items = (snap7types.S7DataItem*len(valores))()
for i in range(0, len(valores)):
    area = valores.iloc[i,0]
    tipo = valores.iloc[i,1]
    numero = valores.iloc[i,2]
    byte = valores.iloc[i,3]
    bit = valores.iloc[i,4]

    data_items[i].Area = ctypes.c_int32(getattr(snap7types, area))
    data_items[i].WordLen = ctypes.c_int32(getattr(snap7types, tipo))
    data_items[i].Result = ctypes.c_int32(0)
    data_items[i].DBNumber = ctypes.c_int32(int(numero))
    data_items[i].Start = ctypes.c_int32(8 * int(byte) + int(bit)) # al estar en modo bit es 8 bits * 5 bytes ya que en el DB0.DBX5.0
    data_items[i].Amount = ctypes.c_int32(getattr(snap7types, tipo))  

for di in data_items:
    # create the buffer
    buffer = ctypes.create_string_buffer(di.Amount)

    # cast the pointer to the buffer to the required type
    pBuffer = ctypes.cast(ctypes.pointer(buffer),
                          ctypes.POINTER(ctypes.c_uint8))
    di.pData = pBuffer

result, data_items = plc.read_multi_vars(data_items)
for di in data_items:
    check_error(di.Result)


result_values = []
for di in data_items:
    if di.WordLen == getattr(snap7types, 'S7WLBit'):
        value = util.get_bool(di.pData, 0, 0)
    elif di.WordLen == getattr(snap7types, 'S7WLByte'):
        value = util.get_int(di.pData, 0)
    elif di.WordLen == getattr(snap7types, 'S7WLDWord'):
        value = util.get_dword(di.pData, 0)
    elif di.WordLen == getattr(snap7types, 'S7WLReal'):
        value = util.get_real(di.pData, 0)
    result_values.append(value)
print(result_values)