from models.wzproperty import WzProperty
from .png import WzPngProperty
from enums import WzVariantType, WzPropertyType


class WzCanvasProperty(WzProperty):
    PROPERTY_NAME_INLINK = "_inlink"
    PROPERTY_NAME_OUTLINK = "_outlink"
    PROPERTY_NAME_ORIGIN = "_origin"
    PROPERTY_NAME_HEAD = "head"
    PROPERTY_NAME_LT = "lt"
    PROPERTY_NAME_ANIMATION_DELAY = "delay"

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.png: WzPngProperty = None
        self.variant = WzVariantType.Object
        self.property_type = WzPropertyType.Canvas

    # def __str__(self):
    #     return f"WzCanvasProperty(name={self.name})"

    # def __repr__(self):
    #     return str(self)
