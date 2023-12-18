from models.wzproperty import WzProperty
from enums import WzVariantType, WzPropertyType


class WzNullProperty(WzProperty):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.variant = WzVariantType.Null
        self.property_type = WzPropertyType.Null

    # def __str__(self):
    #     return f"{self.__name__}(name={self.name})"

    # def __repr__(self):
    #     return str(self)
