# Interoperability tags
INTEROP_TAGS = {
    0x0001: ('InteroperabilityIndex', ),
    0x0002: ('InteroperabilityVersion', ),
    0x1000: ('RelatedImageFileFormat', ),
    0x1001: ('RelatedImageWidth', ),
    0x1002: ('RelatedImageLength', ),
}
INTEROP_INFO = (
    'Interoperability',
    INTEROP_TAGS
)

# GPS tags
GPS_TAGS = {
    0x0002: ('GPSLatitude', ),
    0x0004: ('GPSLongitude', ),
}
GPS_INFO = (
    'GPS',
    GPS_TAGS
)

# Main Exif tag names
EXIF_TAGS = {
    0x8825: ('GPSInfo', GPS_INFO),  # GPS tags
}
DEFAULT_STOP_TAG = 'UNDEF'

# field type descriptions as (length, abbreviation, full name) tuples
FIELD_TYPES = (
    (0, 'X', 'Proprietary'),  # no such type
    (1, 'B', 'Byte'),
    (1, 'A', 'ASCII'),
    (2, 'S', 'Short'),
    (4, 'L', 'Long'),
    (8, 'R', 'Ratio'),
    (1, 'SB', 'Signed Byte'),
    (1, 'U', 'Undefined'),
    (2, 'SS', 'Signed Short'),
    (4, 'SL', 'Signed Long'),
    (8, 'SR', 'Signed Ratio'),
    (4, 'F32', 'Single-Precision Floating Point (32-bit)'),
    (8, 'F64', 'Double-Precision Floating Point (64-bit)'),
)

# To ignore when quick processing
IGNORE_TAGS = (
    0x9286,  # user comment
    0x927C,  # MakerNote Tags
    0x02BC,  # XPM
)
