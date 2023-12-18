from models.wzproperty import WzProperty
from enums import WzVariantType, WzPropertyType


class WzShortProperty(WzProperty):
    def __init__(self, parent, name, value):
        super().__init__(parent, name, value)
        self.variant = WzVariantType.Short
        self.property_type = WzPropertyType.Short

    def __str__(self):
        return f"{self.__name__}(name={self.name}, value={self.value})"

    def __repr__(self):
        return str(self)
