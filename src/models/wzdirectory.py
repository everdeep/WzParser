import logging
from enums import WzDirectoryType
from wzio import WzBinaryReader
from .wzimage import WzImage
from models.base import WzNode, WzNodeType

logger = logging.getLogger(__name__)


class WzDirectory(WzNode):
    def __init__(self, parent, name="", block_size=0, offset=0, checksum=0):
        super().__init__(parent, name, offset, block_size, checksum)
        self.type = WzNodeType.Directory

    def parse(self, reader: WzBinaryReader):
        if reader.bytes_remaining < 1:
            return None

        entry_count = reader.read_wz_int()
        if entry_count < 0 or entry_count > 1000000:
            raise Exception("Invalid WZ version used for decryption")

        for i in range(entry_count):
            directory_type = reader.read_uint_8()

            if directory_type == WzDirectoryType.UnknownType.value:
                reader.read_uint_32()
                reader.read_uint_16()
                reader.read_offset()
                continue
            elif directory_type == WzDirectoryType.RetrieveStringFromOffset.value:
                offset = reader.read_uint_32()
                remember_pos = reader.position
                reader.seek(reader.header.fstart + offset)

                directory_type = reader.read()
                node_name = reader.read_wz_string()

                logger.debug(f"Type: {directory_type} - Name: {node_name}")

            elif directory_type in [
                WzDirectoryType.WzDirectory.value,
                WzDirectoryType.WzImage.value,
            ]:
                node_name = reader.read_wz_string()
                remember_pos = reader.position
            else:
                unknown_bytes = reader.read(20)
                logger.debug(f"Bytes: {unknown_bytes}")
                raise Exception(f"[WzDirectory] Unknown directory: {directory_type}")

            reader.seek(remember_pos)
            block_size = reader.read_wz_int()
            checksum = reader.read_wz_int()
            offset = reader.read_offset()

            if directory_type == WzDirectoryType.WzDirectory.value:
                directory = WzDirectory(self, node_name, block_size, offset, checksum)
                self.add_child(directory)
            elif directory_type == WzDirectoryType.WzImage.value:
                img = WzImage(
                    self, node_name, block_size, reader.position, offset, checksum
                )
                self.add_child(img)

        # Parse all directories
        for child in self.get_children(WzNodeType.Directory):
            child.parse(reader)

        # Parse images
        for child in self.get_children(WzNodeType.Image):
            child.parse(reader)

        return self

    # def __str__(self):
    #     return f"WzDirectory(name={self.name}, block_size={self.block_size}, offset={self.offset}, checksum={self.checksum})"

    # def __repr__(self):
    #     return str(self)
