from io import BufferedReader, BytesIO
from struct import *
import sys
import logging
import os
from typing import Tuple, TypeVar, Union

from Usmap.Objects.FName import FName

T = TypeVar("T")

class BinaryStream:
    def __init__(self, fp: Union[BufferedReader, BytesIO, str, bytes], size: int = -1):
        if isinstance(fp, str):
            self.base_stream = open(fp, "rb")
            self.size = os.path.getsize(fp)
        elif isinstance(fp, bytes):
            self.base_stream = BytesIO(fp)
            self.size = len(fp)
        else:
            self.base_stream = fp
            self.size = size

    def seek(self, offset, SEEK_SET=1):
        self.base_stream.seek(offset, SEEK_SET)

    def readByte(self):
        return self.base_stream.read(1)

    def readByteToInt(self):
        return int.from_bytes(self.base_stream.read(1), "little")

    def readBytes(self, length):
        return self.base_stream.read(length)

    def readChar(self):
        return self.unpack('b')

    def readUChar(self):
        return self.unpack('B')

    def readBool(self):
        return self.unpack('?')

    def readSByte(self):
        return self.unpack("b", 1)

    def readInt16(self):
        return self.unpack('h', 2)

    def readUInt16(self):
        return self.unpack('H', 2)

    def readInt32(self) -> int:
        return self.unpack('i', 4)

    def readUInt32(self):
        return self.unpack('I', 4)

    def readInt64(self):
        return self.unpack('q', 8)

    def readUInt64(self):
        return self.unpack('Q', 8)

    def readFloat(self):
        return self.unpack('f', 4)

    def readDouble(self):
        return self.unpack('d', 8)

    def readString(self):
        length = self.readByteToInt()
        return str(self.unpack(str(length) + 's', length))

    def readFString(self):
        length = self.readByteToInt()
        LoadUCS2Char: bool = length < 0

        if LoadUCS2Char:
            if length == -sys.maxsize - 1:  # maybe?
                raise Exception("Archive is corrupted.")

            length = -length

        if length == 0:
            return ""

        if LoadUCS2Char:
            data = []
            for i in range(length):
                if i == length - 1:
                    self.readInt16()
                else:
                    data.append(self.readInt16())
            string = ''.join(map(str, [chr(v) for v in data]))
            return string

        else:
            return self.readBytes(length).decode("utf-8")

    def readTArray(self, func: T) -> Tuple[T]:
        length = self.readInt32()
        A = tuple(func() for _ in range(length))
        return A

    def readFName(self, NameMap):
        NameIndex = self.readInt32()
        # Number = self.readByteToInt()

        if 0 <= NameIndex < len(NameMap):
            return NameMap[NameIndex] # FName(NameMap[NameIndex], NameIndex, 0)

        logging.debug(f"Bad Name Index: {NameIndex}/{len(NameMap)} - Loader Position: {self.base_stream.tell()}")
        return FName("None", 0, 0)

    def writeBytes(self, value):
        self.base_stream.write(value)

    def writeChar(self, value):
        self.pack('c', value)

    def writeUChar(self, value):
        self.pack('C', value)

    def writeBool(self, value):
        self.pack('?', value)

    def writeInt16(self, value):
        self.pack('h', value)

    def writeUInt16(self, value):
        self.pack('H', value)

    def writeInt32(self, value):
        self.pack('i', value)

    def writeUInt32(self, value):
        self.pack('I', value)

    def writeInt64(self, value):
        self.pack('q', value)

    def writeUInt64(self, value):
        self.pack('Q', value)

    def writeFloat(self, value):
        self.pack('f', value)

    def writeDouble(self, value):
        self.pack('d', value)

    def writeString(self, value):
        length = len(value)
        self.writeUInt16(length)
        self.pack(str(length) + 's', value)

    def pack(self, fmt, data):
        return self.writeBytes(pack(fmt, data))

    def unpack(self, fmt, length=1):
        return unpack(fmt, self.readBytes(length))[0]
