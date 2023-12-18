from models.wzproperty import WzProperty
from wzio.binaryreader import WzBinaryReader
from enums import WzPropertyType, WzVariantType

SOUND_HEADER = [
    0x02, 0x83, 0xEB, 0x36, 0xE4, 0x4F, 0x52, 0xCE, 0x11, 0x9F, 0x53, 0x00,
    0x20, 0xAF, 0x0B, 0xA7, 0x70, 0x8B, 0xEB, 0x36, 0xE4, 0x4F, 0x52, 0xCE,
    0x11, 0x9F, 0x53, 0x00, 0x20, 0xAF, 0x0B, 0xA7, 0x70, 0x00, 0x01, 0x81,
    0x9F, 0x58, 0x05, 0x56, 0xC3, 0xCE, 0x11, 0xBF, 0x01, 0x00, 0xAA, 0x00,
    0x55, 0x59, 0x5A
]


class WzAudioProperty(WzProperty):
    def __init__(self, parent, name, reader: WzBinaryReader, parse=False):
        super().__init__(parent, name)
        self.variant_type = WzVariantType.Object
        self.property_type = WzPropertyType.Sound
        self.data = None

        self._load(reader, parse)

    def _load(self, reader, parse):
        self.block_size = reader.read_wz_int()
        len_ms = reader.read_wz_int()

        header_offset = reader.position
        reader.seek(reader.position + len(SOUND_HEADER))
        wav_format_length = reader.read_uint_8()
        reader.seek(header_offset)

        self.header = reader.read(len(SOUND_HEADER) + 1 + wav_format_length)
        # self._parse_wz_audio_header()

        self.offset = reader.position

        if parse:
            self.data = reader.read(self.block_size)
        else:
            reader.seek(reader.position + self.block_size)

    def _parse_wz_audio_header(self):
        wav_header_size = len(self.header) - len(SOUND_HEADER) - 1
        start = len(SOUND_HEADER) + 1
        wav_header = self.header[start: start + wav_header_size]

        # TODO
        if len(wav_header) < 00:
            pass

    # def __str__(self):
    #     return f"WzAudioProperty(name={self.name}, offset={self.offset})"

    # def __repr__(self):
    #     return str(self)
