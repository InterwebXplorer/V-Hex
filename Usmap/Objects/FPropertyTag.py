from Usmap.Objects.FName import FName
from Usmap.BinaryReader import BinaryStream
from enum import IntEnum, auto
from dataclasses import dataclass


class FPropertyTag:
    StructName: FName
    ValueType: 'FPropertyTag'
    EnumName: FName
    InnerType: 'FPropertyTag'

    def __init__(self, reader: BinaryStream, usmap) -> None:
        NameMap = usmap.NameMap

        Type = reader.readByteToInt()
        try:
            self.Type = EUsmapPropertyType(Type).name
        except:
            print(f"USMAP Reader: Invalid PropertyType Value {Type}")
            self.Type = Type

        if Type == EUsmapPropertyType.StructProperty:
            self.StructName = reader.readFName(NameMap)

        elif Type == EUsmapPropertyType.EnumProperty:
            self.InnerType = FPropertyTag(reader, usmap)
            self.EnumName = reader.readFName(NameMap)

        elif Type == EUsmapPropertyType.ArrayProperty:
            self.InnerType = FPropertyTag(reader, usmap)

        elif Type == EUsmapPropertyType.SetProperty:  # same as Array
            self.InnerType = FPropertyTag(reader, usmap)

        elif Type == EUsmapPropertyType.MapProperty:
            self.InnerType = FPropertyTag(reader, usmap)
            self.ValueType = FPropertyTag(reader, usmap)

    def GetValue(self):
        result = {}
        for v in ["Type", "StructName", "ValueType", "EnumName", "InnerType"]:
            val = getattr(self, v, None)
            if val is not None:
                if isinstance(val, FPropertyTag):
                    val = val.GetValue()
                if isinstance(val, FName):
                    val = val.string
                result.update({v: val})
    
        # if Type == EUsmapPropertyType.StructProperty:
        #     result.update(StructName=self.StructName)
        # elif Type == EUsmapPropertyType.EnumProperty:
        #     result.update(InnerType = self.InnerType, EnumName=self.EnumName.string)
        # elif Type == EUsmapPropertyType.ArrayProperty:
        #     result.update(InnerType=self.InnerType)
        # elif Type == EUsmapPropertyType.SetProperty:  # same as Array
        #     result.update(InnerType=self.InnerType)
        # elif Type == EUsmapPropertyType.MapProperty:
        #     result.update(InnerType=self.InnerType, ValueType=self.ValueType)
        return result

    def __str__(self) -> str:
        return str(self.GetValue())

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class EUsmapPropertyType(IntEnum):
    ByteProperty = 0
    BoolProperty = auto()
    IntProperty = auto()
    FloatProperty = auto()
    ObjectProperty = auto()
    NameProperty = auto()
    DelegateProperty = auto()
    DoubleProperty = auto()
    ArrayProperty = auto()
    StructProperty = auto()
    StrProperty = auto()
    TextProperty = auto()
    InterfaceProperty = auto()
    MulticastDelegateProperty = auto()
    WeakObjectProperty = auto()
    LazyObjectProperty = auto()
    AssetObjectProperty = auto()
    SoftObjectProperty = auto()
    UInt64Property = auto()
    UInt32Property = auto()
    UInt16Property = auto()
    Int64Property = auto()
    Int16Property = auto()
    Int8Property = auto()
    MapProperty = auto()
    SetProperty = auto()
    EnumProperty = auto()
    FieldPathProperty = auto()
