from enums import WzPropertyType, WzVariantType
from models.wzproperty import WzProperty


class WzConvexProperty(WzProperty):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.variant = WzVariantType.Object
        self.property_type = WzPropertyType.Convex

    # def __str__(self):
    #     return f"WzConvexProperty(name={self.name})"

    # def __repr__(self):
    #     return str(self)
