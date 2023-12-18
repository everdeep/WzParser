from models.base import WzNode
from enums import WzNodeType, WzVariantType, WzPropertyType


class WzProperty(WzNode):
    def __init__(self, parent, name="", value=None):
        super().__init__(parent, name)
        self.node_type = WzNodeType.Property
        self.variant = WzVariantType.Object
        self.property_type = WzPropertyType.Property
        self.value = value

    # def __str__(self):
    #     return f"WzProperty(name={self.name}, value={self.value})"

    # def __repr__(self):
    #     return str(self)
