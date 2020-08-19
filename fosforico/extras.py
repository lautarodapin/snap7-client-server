import struct
from snap7.util import *

'''
Extras para soportar small ints

DB_mixin::hereada de DB
DB_Row_mixin::hereda de DB_Row: añade en set_value y get_value el SINT
'''




def set_usint(bytearray_, byte_index, _int):
    """set unsigned small int

    Args:
        bytearray_ (bytearray): bytearray
        byte_index (int): index of the bytearray
        _int (int): positive value to set (0 - 255)

    Returns:
        bytearray: bytearray of the db
    """
    _int = int(_int)
    _bytes = struct.unpack('B', struct.pack('>B', _int))
    bytearray_[byte_index] = _bytes[0]
    return bytearray_


def get_usint(bytearray_, byte_index):
    """get the unsigned small int from the bytearray

    Args:
        bytearray_ (bytearray)
        byte_index (int): index of the bytearray

    Returns:
        int: unsigned small int (0 - 255)
    """
    data = bytearray_[byte_index] & 0xff
    packed = struct.pack('B', data)
    value = struct.unpack('>B', packed)[0]
    return value


def set_sint(bytearray_, byte_index, _int):
    """set small int

    Args:
        bytearray_ (bytearray)
        byte_index (int): index of the bytearray
        _int (int): small int (-128 - 127)

    Returns:
        bytearray
    """
    _int = int(_int)
    _bytes = struct.unpack('B', struct.pack('>b', _int))
    bytearray_[byte_index] = _bytes[0]
    return bytearray_


def get_sint(bytearray_, byte_index):
    """get the small int

    Args:
        bytearray_ (bytearray)
        byte_index (int): index of the bytearray

    Returns:
        int: small int (-127 - 128)
    """
    data = bytearray_[byte_index]
    packed = struct.pack('B', data)
    value = struct.unpack('>b', packed)[0]
    return value


class DB_mixin(DB):
    
    def make_rows(self):
        id_field = self.id_field
        row_size = self.row_size
        specification = self.specification
        layout_offset = self.layout_offset

        for i in range(self.size):
            # calculate where row in bytearray starts
            db_offset = i * row_size + self.db_offset
            # create a row object
            row = DB_Row_mixin(self,
                         specification,
                         row_size=row_size,
                         db_offset=db_offset,
                         layout_offset=layout_offset,
                         row_offset=self.row_offset)

            # store row object
            key = row[id_field] if id_field else i
            if key and key in self.index:
                msg = '%s not unique!' % key
                logger.error(msg)
            self.index[key] = row



class DB_Row_mixin(DB_Row):
    ''' Provee funcionalidad para soportar small ints '''
    
    def get_value(self, byte_index, _type):
        _bytearray = self.get_bytearray()

        if _type == 'BOOL':
            byte_index, bool_index = byte_index.split('.')
            return get_bool(_bytearray, self.get_offset(byte_index),
                            int(bool_index))

        # remove 4 from byte index since
        # first 4 bytes are used by db
        byte_index = self.get_offset(byte_index)

        if _type.startswith('STRING'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return get_string(_bytearray, byte_index, max_size)

        if _type == 'REAL':
            return get_real(_bytearray, byte_index)

        if _type == 'DWORD':
            return get_dword(_bytearray, byte_index)

        if _type == 'INT':
            return get_int(_bytearray, byte_index)

        if _type == 'USINT':
            return get_usint(_bytearray, byte_index)

        if _type == 'SINT':
            return get_sint(_bytearray, byte_index)
        raise ValueError

    def set_value(self, byte_index, _type, value):
        _bytearray = self.get_bytearray()

        if _type == 'BOOL':
            byte_index, bool_index = byte_index.split('.')
            return set_bool(_bytearray, self.get_offset(byte_index),
                            int(bool_index), value)

        byte_index = self.get_offset(byte_index)

        if _type.startswith('STRING'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return set_string(_bytearray, byte_index, value, max_size)

        if _type == 'REAL':
            return set_real(_bytearray, byte_index, value)

        if _type == 'DWORD':
            return set_dword(_bytearray, byte_index, value)

        if _type == 'INT':
            return set_int(_bytearray, byte_index, value)
        
        if _type == 'USINT':
            return set_usint(_bytearray, byte_index, value)

        if _type == 'SINT':
            return set_sint(_bytearray, byte_index, value)

        raise ValueError

