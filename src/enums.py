import logging
from enum import Enum

logger = logging.getLogger(__name__)


class WzPropertyType(Enum):
    Null = "Null"
    Short = "Short"
    Int = "Integer"
    Long = "Long"
    Float = "Float"
    Double = "Double"
    String = "String"
    Item = "Item"
    Property = "Property"
    Canvas = "Canvas"
    Vector = "Shape2D#Vector2D"
    Convex = "Shape2D#Convex2D"
    Sound = "Sound_DX8"
    UOL = "UOL"
    Lua = "Lua"
    PNG = "PNG"


class WzVariantType(Enum):
    Unknown = []
    Null = [0x00]
    Short = [0x02, 0x0B]
    Int = [0x03, 0x13]
    Float = [0x04]
    Double = [0x05]
    Long = [0x14]
    UOL = [0x08]
    Object = [0x09]


def _WzVariant_parser(cls, value):
    if not isinstance(value, int):
        # forward call to Types' superclass (enum.Enum)
        return super(WzVariantType, cls).__new__(cls, value)
    else:
        # map strings to enum values, default to Unknown
        return {
            0: WzVariantType.Null,
            2: WzVariantType.Short,
            11: WzVariantType.Short,
            3: WzVariantType.Int,
            19: WzVariantType.Int,
            4: WzVariantType.Float,
            5: WzVariantType.Double,
            20: WzVariantType.Long,
            8: WzVariantType.UOL,
            9: WzVariantType.Object,
        }.get(value, WzVariantType.Unknown)


setattr(WzVariantType, "__new__", _WzVariant_parser)


class WzNodeType(Enum):
    File = 0
    Image = 1
    Directory = 2
    Property = 3
    Unknown = 99


class AudioType(Enum):
    Raw = (0,)
    MP3 = (1,)
    WAV = 2


class WzDirectoryType(Enum):
    UnknownType = 1
    RetrieveStringFromOffset = 2
    WzDirectory = 3
    WzImage = 4
