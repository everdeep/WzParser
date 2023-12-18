import logging
from enums import WzPropertyType, WzVariantType
from models.wzproperty import WzProperty
from wzio.binaryreader import WzBinaryReader

logger = logging.getLogger(__name__)


class WzPngProperty(WzProperty):
    def __init__(self, parent, name, reader: WzBinaryReader, parse=False):
        super().__init__(parent, name)
        self.variant = WzVariantType.Object
        self.property_type = WzPropertyType.PNG

        logger.debug(f"({name}) @ ({reader.position})")

        self.width = reader.read_wz_int()
        self.height = reader.read_wz_int()
        self.format = reader.read_wz_int()
        self.format2 = reader.read_wz_int()
        reader.seek(reader.position + 4)
        self.offset = reader.position
        self.block_size = reader.read_uint_32() - 1
        reader.seek(reader.position + 1)

        if parse:
            self._load()
        else:
            reader.seek(reader.position + self.block_size)

    def _load(self, reader) -> None:
        self.data = reader.read(self.block_size)

    # def __str__(self):
    #     return f"{self.__name__}(name={self.name}, WxH=({self.width}, {self.height}), offset={self.offset}, block_size={self.block_size})"

    # def __repr__(self):
    #     return str(self)
