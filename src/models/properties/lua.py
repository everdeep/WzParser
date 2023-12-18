from models.wzproperty import WzProperty


class WzLuaProperty(WzProperty):
    def __init__(self, parent, name):
        super().__init__(parent, name)
