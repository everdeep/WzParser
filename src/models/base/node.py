import uuid
from enums import WzNodeType, WzVariantType


class WzNode:
    def __init__(self, parent=None, name="", offset=0, block_size=0, checksum=0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.parent = parent
        self.children: [WzNode] = []
        self.variant = WzVariantType.Unknown
        self.node_type = WzNodeType.Unknown
        self.offset = offset
        self.block_size = block_size
        self.checksum = checksum
        self.node_path = self._node_path()

        # super().__init__(self.name, self.id, data=self)


    # def __str__(self):
    #     return f"WzNode(name={self.name}, type={self.node_type}, parent={self.parent.name})"

    # def __repr__(self):
    #     return self.__str__()
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, type={self.node_type}, parent={self.parent.name})"

    def __str__(self):
        return f"id={self.id}, name={self.name}, type={self.node_type}, parent={self.parent.name}"
    
    def _node_path(self):
        if self.parent is None:
            return self.name

        if self.parent.node_path is None:
            return self.name

        return f"{self.parent.node_path}/{self.name}"

    def update_tree(self, parent, child):
        """Continues up to the root node and updates the tree with the new child node."""
        if parent is None:
            return

        parent.update_tree(parent, self)

    def add_child(self, child):
        self.children.append(child)

        # update tree
        # self.update_tree(child.parent, child)

    def get_children(self, node_type=None):
        if node_type is None:
            return self.children

        return [child for child in self.children if child.node_type == node_type]

    def export(self):
        if self.node_type == WzNodeType.Directory:
            return self._export_directory()
        elif self.node_type == WzNodeType.Image:
            return self._export_image()
        elif self.node_type == WzNodeType.Property:
            return self._export_property()
