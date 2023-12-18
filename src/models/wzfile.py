import os
import uuid
import numpy as np
import logging
from crypto.wzcrypto import WzKey
from wzio.binaryreader import WzBinaryReader, WzHeader
from .wzdirectory import WzDirectory
from models.base import WzNode, WzNodeType
from treelib import Tree
from treelib.exceptions import NodeIDAbsentError, DuplicatedNodeIdError

logger = logging.getLogger(__name__)


def check_version_hash(version_header, version):
    version_hash = 0
    for c in str(version):
        version_hash = (version_hash * 32) + ord(c) + 1

    if version_header == 770:
        return np.uint32(version_hash)  # Always 59192

    decrypted_version_number = (
        ~(
            (version_hash >> 24)
            ^ (version_hash >> 16)
            ^ (version_hash >> 8)
            ^ version_hash
        )
        & 0xFF
    )

    if version_header == decrypted_version_number:
        return np.uint32(version_hash)

    return 0


class WzFile:
    copyright: np.str_
    file_version: np.byte
    path: str = None

    # Declared as a class property rather than inheriting the Tree class
    # to avoid cluttered properties
    tree: Tree = None

    def __init__(self, wz_path: str, wz_key: WzKey):
        self.id = uuid.uuid4()
        self.wz_dir = None
        self.version_header = None
        self.wz_key = wz_key
        logger.debug(f"Using IV of: {self.wz_key.iv}")

        if not os.path.exists(wz_path) or wz_path.endswith(".wz") == False:
            logger.error("Wz file not found or is invalid:", wz_path)
            return

        self.name = os.path.basename(wz_path)
        self.wz_path = wz_path
        self.maplestory_patch_version = -1
        self.maplestory_version = wz_key.version
        self.type = WzNodeType.File
        self.offset = 0
        self.node_path = None
        self.tree = Tree()

    def parse(self, build_tree=False):
        with WzBinaryReader(self.wz_path, self.wz_key) as reader:
            self.size = reader.file_size

            header = WzHeader()
            header.ident = reader.read_string(4)
            header.fsize = reader.read_uint_64()
            header.fstart = reader.read_uint_32()
            header.copyright = reader.read_string(int(header.fstart - 17))
            reader.header = header

            self.block_size = header.fsize

            # Skip unknown bytes to beginning of first section
            reader.seek(header.fstart)

            self.version_header = reader.read_uint_16()
            self.check_64bit_client(reader, self.version_header)

            logger.debug(f"Filename: {self.wz_path.split('/')[-1]}")
            logger.debug(f"Version header: {self.version_header}")

            success = self.try_decode(reader)
            if not success:
                logger.error(f"Failed to decode wz file: {self.wz_path}")
                return None

            # Build a tree
            if build_tree:
                self._build_tree()

        return self

    def check_64bit_client(self, reader: WzBinaryReader, version_header):
        if version_header > 0xFF:
            self.version_header = 770
        elif version_header == 0x80:
            reader.seek(reader.header.fstart)
            prop_count = reader.read_uint_32()
            if 0xFFFF >= prop_count > 0 == (prop_count & 0xFF):
                self.version_header = 770

    def try_decode(self, reader: WzBinaryReader):
        max_maple_version = 1000
        for i in range(0, max_maple_version):
            version_hash = check_version_hash(self.version_header, i)
            if version_hash == 0:
                continue

            logger.debug(f"Version hash found: {version_hash}")
            reader.hash = version_hash

            # Directory parsing
            fallback_offset_position = reader.position
            try:
                self.wz_dir = WzDirectory(
                    self, self.name, offset=reader.position
                ).parse(reader)

                return True
            except Exception as e:
                logger.error(f"Error: {e}")
                reader.seek(fallback_offset_position)
                continue
        return False

    def _build_tree(self):
        # Add root node
        self.tree.create_node(self.wz_dir.name, self.wz_dir.id, data=self.wz_dir)

        # list of tuples (parent, child)
        nodes = []

        # Add all children using BFS
        queue = self.wz_dir.get_children().copy()
        while len(queue) > 0:
            node = queue.pop(0)
            nodes.append((node.parent, node))
            queue.extend(node.get_children().copy())

        print(f"Fetched {len(nodes)} nodes")

        # Set the max number of retries to the number of nodes
        retry_count = len(nodes)
        while len(nodes) > 0:
            if retry_count <= 0:
                logger.error(f"Failed to add {len(nodes)} nodes to tree")
                break

            parent, child = nodes.pop(0)
            success = self._update_tree(parent, child)
            if not success:
                nodes.append((parent, child))
                retry_count -= 1

    def _update_tree(self, parent, child):
        logger.debug(f"Adding tree node {child.name} to parent {parent.name}")
        try:
            self.tree.create_node(child.name, child.id, parent.id, data=child)
            return True
        except NodeIDAbsentError as e:
            logger.error(
                f"Parent node ID {parent.id} not found for {child.name}: {child.node_path}"
            )
            return False
        except DuplicatedNodeIdError as e:
            logger.error(
                f"Duplicate node ID {child.id} for {child.name}: {child.node_path}"
            )
            return False

    # def __str__(self):
    #     return f"WzFile(name={self.name}, path={self.wz_path})"
