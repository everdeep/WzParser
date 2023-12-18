from models.wzproperty import WzProperty
from enums import WzPropertyType, WzVariantType


class WzVectorProperty(WzProperty):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.variant = WzVariantType.Object
        self.property_type = WzPropertyType.Vector
        self.X = 0.0
        self.Y = 0.0

    # def __str__(self):
    #     return f"{self.__name__}(name={self.name}, ({self.X}, {self.Y}))"

    # def __repr__(self):
    #     return str(self)
