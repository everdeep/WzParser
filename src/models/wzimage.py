import logging
from models.base import WzNode, WzNodeType
from wzio.binaryreader import WzBinaryReader
from enums import WzPropertyType
import factory.property as PropertyFactory

logger = logging.getLogger(__name__)

class WzImage(WzNode):
    header_byte_without_offset = 0x73
    header_byte_with_offset = 0x1B

    def __init__(
        self, parent, name="", block_size=0, block_start=0, offset=0, checksum=0
    ):
        super().__init__(parent, name)
        self._data = None
        self.block_size = block_size
        self.block_start = block_start
        self.offset = offset
        self.checksum = checksum
        self.node_type = WzNodeType.Image

    def parse(self, reader: WzBinaryReader):
        self._data = reader.read(self.block_size)

        reader.seek(self.offset)
        byte = reader.read_uint_8()
        if byte == self.header_byte_without_offset:
            self._parse_properties(reader)

    def _parse_properties(self, reader):
        object_type = reader.read_wz_string()
        if object_type == WzPropertyType.Property.value:
            reader.seek(reader.position + 2)
            entry_count = reader.read_wz_int()
            for i in range(entry_count):
                self.add_child(PropertyFactory.create_property(self, reader, self.offset))
        else:
            raise Exception(f"Invalid object type: {object_type}")

    # def __str__(self):
    #     return f"WzImage(name={self.name}, parent={self.parent.name}, block_size={self.block_size}, offset={self.offset}, checksum={self.checksum})"

    # def __repr__(self):
    #     return str(self)
