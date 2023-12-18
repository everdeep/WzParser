import logging
from models.wzproperty import WzProperty
from models.properties import *
from enums import WzVariantType, WzPropertyType

logger = logging.getLogger(__name__)


def create_property(parent, reader, offset=None) -> WzProperty:
    global OFFSET
    if offset is not None:
        OFFSET = offset

    logger.debug(f"Creating property for parent ({parent.name}) @ ({reader.position})")

    name = reader.read_wz_uol(OFFSET)
    variant_type = reader.read_wz_int()

    try:
        variant_type = WzVariantType(variant_type)
    except ValueError:
        logger.error(f"Invalid variant type: ({variant_type}) @ ({reader.position - 5})")
        raise

    logger.debug(f"Name: ({name}), Variant Type: ({variant_type.name})")

    # For debugging a specific property
    if reader.position >= 1695:
        pass

    if variant_type == WzVariantType.Null:
        # Null
        return WzNullProperty(parent, name)
    elif variant_type == WzVariantType.Short:
        # Int 16
        return WzShortProperty(parent, name, reader.read_int_16())
    elif variant_type == WzVariantType.Int:
        # Wz int
        return WzIntProperty(parent, name, reader.read_wz_int())
    elif variant_type == WzVariantType.Float:
        # Wz float 32
        return WzFloatProperty(parent, name, reader.read_wz_float())
    elif variant_type == WzVariantType.Double:
        # Float 64
        return WzDoubleProperty(parent, name, reader.read_float_64())
    elif variant_type == WzVariantType.Long:
        # Wz Long
        return WzLongProperty(parent, name, reader.read_wz_long())
    elif variant_type == WzVariantType.UOL:
        # Wz UOL
        return WzUOLProperty(parent, name, reader.read_wz_uol())
    elif variant_type == WzVariantType.Object:
        # Object
        property = WzProperty(parent, name)
        end_pos = reader.read_uint_32() + reader.position
        new_property = _extract_more(property, reader, name=name)
        reader.seek(end_pos)
        if new_property is not None:
            new_property.parent = parent
            new_property.node_path = f"{parent.node_path}/{new_property.name}"
            return new_property
        return property
    else:
        raise Exception(f"Invalid variant type: ({variant_type}) @ ({reader.position})")


def _extract_more(parent, reader, **kwargs):
    child_object_type = reader.read_uint_8()
    if child_object_type in [0x00, 0x73]:
        return _parse_object(parent, reader, **kwargs)
    elif child_object_type in [0x01, 0x1B]:
        object_type = reader.read_string_at_offset(OFFSET + reader.read_uint_32())
        return _parse_object(parent, reader, object_type=object_type, **kwargs)


def _parse_object(parent, reader, **kwargs):
    """
    The property we are parsing is an object, so we need to extract more information from it.
    """
    name = kwargs.get("name", "")
    object_type = kwargs.get("object_type", None)

    # Determine the object type
    if object_type is None:
        object_type = reader.read_wz_string()

    try:
        object_type = WzPropertyType(object_type)
    except ValueError:
        return WzProperty(None, name, "Unknown property...")

    logger.debug(f"Object type: ({object_type.name})")

    if object_type == WzPropertyType.Property:
        # Empty bytes
        reader.seek(reader.position + 2)

        # Read child count
        entry_count = reader.read_wz_int()

        # Create properties
        for i in range(entry_count):
            parent.add_child(create_property(parent, reader))

        return None

    elif object_type == WzPropertyType.Canvas:
        # Create a Canvas property
        reader.seek(reader.position + 1)
        canvas_property = WzCanvasProperty(None, name)
        # Check if canvas property has sub-properties

        if reader.read_uint_8() == 1:
            # Skip 2 bytes
            reader.seek(reader.position + 2)

            # Read child count
            entry_count = reader.read_wz_int()
            for i in range(entry_count):
                canvas_property.add_child(create_property(canvas_property, reader))

        # Create PNG property
        canvas_property.png = WzPngProperty(canvas_property, "PNG", reader)
        return canvas_property
    elif object_type == WzPropertyType.Vector:
        # Create a Vector Property
        vector_property = WzVectorProperty(None, name)
        vector_property.X = WzIntProperty(vector_property, "X", reader.read_wz_int())
        vector_property.Y = WzIntProperty(vector_property, "Y", reader.read_wz_int())
        return vector_property
    elif object_type == WzPropertyType.Convex:
        # Create a Convex Property
        convex_property = WzConvexProperty(None, name)

        # Read child count
        entry_count = reader.read_wz_int()
        for i in range(entry_count):
            _extract_more(convex_property, reader)

        return convex_property
    elif object_type == WzPropertyType.Sound:
        # Create a Sound Property
        wz_audio = WzAudioProperty(None, name, reader)
        return wz_audio
    elif object_type == WzPropertyType.UOL:
        wz_uol = WzUOLProperty(None, name, reader.read_wz_uol())
        return wz_uol
