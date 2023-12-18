from models.wzproperty import WzProperty
from enums import WzVariantType, WzPropertyType


class WzLongProperty(WzProperty):
    def __init__(self, parent, name, value):
        super().__init__(parent, name, value)
        self.variant = WzVariantType.Long
        self.property_type = WzPropertyType.Long

    # def __str__(self):
    #     return f"{self.__name__}(name={self.name}, value={self.value})"

    # def __repr__(self):
    #     return str(self)
