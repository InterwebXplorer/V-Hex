import io
from re import S
from typing import Dict, List, Tuple
from enum import IntEnum, auto
from dataclasses import dataclass
import inspect

import brotli

from Usmap.Oodle import Decompress
from Usmap.BinaryReader import BinaryStream
from Usmap.Objects.FPropertyTag import FPropertyTag


class Version(IntEnum):
    Initial = 0

    Latest_Plus_One = auto()
    Latest = Latest_Plus_One - 1


class Usmap:
    MAGIC = 0x30C4
    NameMap: Tuple[str]
    Enums: dict
    Mappings: Dict[str, 'Struct']

    def __init__(self, fp) -> None:
        self.reader = BinaryStream(fp)
        self.Mappings = {}
        self.Enums = {}

    def read(self):
        reader = self.reader

        magic = reader.readInt16()
        if magic != self.MAGIC:
            raise Exception("invalid magic")

        version = Version(reader.readByteToInt())

        if version != Version.Latest:  # Initial
            raise Exception(f".usmap file has invalid version {version}")

        method = reader.readByteToInt()
        compressSize = reader.readInt32()
        decompressSize = reader.readInt32()

        # 0 -> "None"
        # 1 -> "Oodle"
        # 2 -> "Brotli"
        decompressedData: bytes
        if method == 0:
            decompressedData = reader.readBytes(compressSize)
        elif method == 1:
            decompressedData = Decompress(reader.readBytes(compressSize),decompressSize)
        elif method == 2:
            decompressedData = brotli.decompress(reader.readBytes(compressSize))
        else:
            raise Exception("Unknown compression method")

        if len(decompressedData) != decompressSize:
            raise ValueError(f"Failed to decompress data, Expected length {decompressSize} got {len(decompressedData)}")

        self.reader = BinaryStream(io.BytesIO(decompressedData))
        self.ParseData()
        return self

    def ParseData(self):
        reader = self.reader

        self.NameMap = reader.readTArray(reader.readFString)

        # Enums
        size = reader.readUInt32()
        for _ in range(size):
            enumName = reader.readFName(self.NameMap)
            Number = reader.readByteToInt()
            Values = []
            for _ in range(Number):
                Name = reader.readFName(self.NameMap)
                Values.append(Name)

            self.Enums[enumName] = ()
            self.Enums[enumName] = tuple(Values)

        # Schemas
        size = reader.readUInt32()
        for _ in range(size):
            structName = reader.readFName(self.NameMap)
            SuperIndex = reader.readUInt32()
            PropertyCount = reader.readUInt16()

            serializablePropertyCount = reader.readUInt16()
            props = {}
            for _ in range(serializablePropertyCount):
                SchemaIndex = reader.readUInt16()
                ArraySize = reader.readByteToInt()
                Name = reader.readFName(self.NameMap)
                data = FPropertyTag(reader, self)

                prop: StructProps = StructProps(SchemaIndex,ArraySize, Name, data)
                props[SchemaIndex] = prop

            struct: Struct = Struct(structName, SuperIndex, PropertyCount, props=props)
            self.Mappings[struct.Name] = struct

    def GetValue(self):
        Dict = {}
        Dict["Enums"] = self.Enums
        Dict["Mappings"] = {}
        for k,v in self.Mappings.items():
            Dict["Mappings"][k] = v.GetValue()
        return Dict

@dataclass
class StructProps:
    SchemaIndex: int
    ArraySize: int
    Name: str
    data: FPropertyTag

    def GetValue(self):
        return {
            "SchemaIndex": self.SchemaIndex,
            "ArraySize": self.ArraySize,
            "Name": self.Name,
            **self.data.GetValue()
        }

@dataclass
class Struct:
    Name: str
    SuperIndex: int
    PropertyCount: int
    props: Dict[int, StructProps]

    def GetValue(self):
        props = {}
        for k,v in self.props.items():
            props[k] = v.GetValue()

        return {
            "Name": self.Name,
            "SuperIndex": self.SuperIndex,
            "PropertyCount": self.PropertyCount,
            "props": props
        }

    def getprop(self, index: int):
        return self.props.get(index)