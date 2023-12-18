import struct
import numpy as np
from constants import OFFSET
from utils import rotate_left
from crypto.wzcrypto import WzKey


class WzHeader:
    DEFAULT_WZ_HEADER_COPYRIGHT = "Package file v1.0 Copyright 2022 Wizet, ZMS"

    ident = ""
    copyright = ""
    fsize = 0
    fstart = 0

    def __init__(self, ident="PKG1", fsize=0, fstart=60):
        self.ident = ident
        self.fsize = fsize
        self.fstart = fstart
        self.copyright = self.DEFAULT_WZ_HEADER_COPYRIGHT

    def __str__(self):
        return "WzHeader(ident={}, fsize={}, fstart={}, copyright={})".format(
            self.ident, self.fsize, self.fstart, self.copyright
        )

    def __repr__(self):
        return str(self)


class WzBinaryReader:
    hash = None
    header: WzHeader = None

    def __init__(self, wz_path, key):
        self.wz_path = wz_path
        self.key: WzKey = key

    def __str__(self):
        return f"WzBinaryReader(key={self.key}, path={self.wz_path}, pos={self.position}, available={self.bytes_remaining}, file_size={self.file_size})"

    def __repr__(self):
        return str(self)

    def __enter__(self):
        self.reader = open(self.wz_path, "rb")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reader.close()

    def seek(self, offset, whence=0):
        self.reader.seek(offset, whence)

    def read(self, n=1):
        return self.reader.read(n)

    def read_string(self, n):
        return self.reader.read(n).decode("ascii")

    def read_uint_8(self):
        return int.from_bytes(self.reader.read(1), byteorder="little", signed=False)

    def read_uint_16(self):
        return int.from_bytes(self.reader.read(2), byteorder="little", signed=False)

    def read_uint_32(self):
        return int.from_bytes(self.reader.read(4), byteorder="little", signed=False)

    def read_uint_64(self):
        return int.from_bytes(self.reader.read(8), byteorder="little", signed=False)

    def read_int_8(self):
        return int.from_bytes(self.reader.read(1), byteorder="little", signed=True)

    def read_int_16(self):
        return int.from_bytes(self.reader.read(2), byteorder="little", signed=True)

    def read_int_32(self):
        return int.from_bytes(self.reader.read(4), byteorder="little", signed=True)

    def read_int_64(self):
        return int.from_bytes(self.reader.read(8), byteorder="little", signed=True)

    def read_float_32(self):
        return struct.unpack("f", self.reader.read(4))[0]

    def read_float_64(self):
        return struct.unpack("d", self.reader.read(8))[0]

    def read_wz_int(self):
        sb = self.read_int_8()
        return self.read_int_32() if sb == -128 else sb

    def read_wz_float(self):
        flag = self.read_uint_8()
        if flag == 0x00:
            return 0
        if flag == 0x80:
            return self.read_float_32()

    def read_wz_long(self):
        sb = self.read_int_8()
        return self.read_int_64() if sb == -128 else sb

    def read_wz_string(self):
        length = self.read_int_8()
        if length == 0:
            return

        if length > 0:
            # Unicode
            if length == 127:
                length = self.read_int_32()

            if length <= 0:
                return None

            mask = 0xAAAA
            ret_str = ""

            for i in range(length):
                val = self.read_uint_16()
                val = val ^ (mask + i)
                val = (self.key.at(i * 2 + 1) << 8) + self.key.at(i * 2)
                ret_str += chr(val)

            return ret_str
        elif length < 0:
            # ASCII
            if length == -128:
                length = self.read_int_32()
                if length <= 0:
                    return None
            else:
                length = -length

            mask = 0xAA
            ret_str = ""

            for i in range(0, length):
                b = self.read_uint_8()
                b = b ^ (mask + i)
                b = b ^ self.key.at(i)
                ret_str += chr(b)

            return ret_str

    def read_wz_uol(self, offset=0):
        flag = self.read_uint_8()

        if flag == 0x00 or flag == 0x73:
            return self.read_wz_string()
        elif flag == 0x01 or flag == 0x1B:
            pos = self.read_uint_32()
            return self.read_string_at_offset(offset + pos)
        else:
            return ""

    def read_offset(self):
        offset = np.uint32((self.position - self.header.fstart) ^ (2**32 - 1))
        offset *= self.hash
        offset -= OFFSET
        offset = rotate_left(offset, (offset & 0x1F))
        encrypted_offset = self.read_uint_32()
        offset ^= encrypted_offset
        offset += self.header.fstart * 2
        return offset

    def read_string_at_offset(self, offset, read_byte=False):
        current_pos = self.position
        self.seek(offset)
        if read_byte:
            self.read()

        data = self.read_wz_string()
        self.seek(current_pos)
        return data

    @property
    def position(self):
        if self.reader is None:
            return 0
        return self.reader.tell()

    @property
    def file_size(self):
        """Get the length of the file for a regular file (not a device file)"""
        current_pos = self.position
        self.seek(0, 2)  # move to end of file
        length = self.position  # get current position
        self.seek(current_pos)  # go back to where we started
        return length

    @property
    def bytes_remaining(self):
        """Get number of bytes left to read"""
        current_pos = self.position
        return self.file_size - current_pos
