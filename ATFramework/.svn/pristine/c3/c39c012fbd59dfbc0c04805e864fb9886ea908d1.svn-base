import struct
import re


from .tag import *
from fractions import Fraction
class Ratio(Fraction):
    """
    Ratio object that eventually will be able to reduce itself to lowest
    common denominator for printing.
    """

    # We're immutable, so use __new__ not __init__
    def __new__(cls, numerator=0, denominator=None):
        try:
            self = super(Ratio, cls).__new__(cls, numerator, denominator)
        except ZeroDivisionError:
            self = super(Ratio, cls).__new__(cls)
            self._numerator = numerator
            self._denominator = denominator
        return self
    __new__.doc = Fraction.__new__.__doc__

    def __repr__(self):
        return str(self)

    @property
    def num(self):
        return self.numerator

    @property
    def den(self):
        return self.denominator

    def decimal(self):
        return float(self)


try:
    basestring
except NameError:
    basestring = str

class IfdTag:
    """
    Eases dealing with tags.
    """

    def __init__(self, printable, tag, field_type, values, field_offset,field_length):
        self.printable = printable
        self.tag = tag
        self.field_type = field_type
        self.field_offset = field_offset
        self.field_length = field_length
        self.values = values

    def __str__(self):
        return self.printable

    def __repr__(self):
        try:
            s = '(0x%04X) %s=%s @ %d' % (self.tag,
                                         FIELD_TYPES[self.field_type][2],
                                         self.printable,
                                         self.field_offset)
        except:
            s = '(%s) %s=%s @ %s' % (str(self.tag),
                                     FIELD_TYPES[self.field_type][2],
                                     self.printable,
                                     str(self.field_offset))
        return s


class ExifHeader:
    """
    Handle an EXIF header.
    """
    def __init__(self, file, endian, offset, fake_exif, strict,
                 debug=False, detailed=True, truncate_tags=True):
        self.file = file
        self.endian = endian
        self.offset = offset
        self.fake_exif = fake_exif
        self.strict = strict
        self.debug = debug
        self.detailed = detailed
        self.truncate_tags = truncate_tags
        self.tags = {}

    def s2n(self, offset, length, signed=False):
        """
        Convert slice to integer, based on sign and endian flags.

        Usually this offset is assumed to be relative to the beginning of the
        start of the EXIF information.
        For some cameras that use relative tags, this offset may be relative
        to some other starting point.
        """
        # Little-endian if Intel, big-endian if Motorola
        fmt = '<' if self.endian == 'I' else '>'
        # Construct a format string from the requested length and signedness;
        # raise a ValueError if length is something silly like 3
        try:
            fmt += {
                (1, False): 'B',
                (1, True):  'b',
                (2, False): 'H',
                (2, True):  'h',
                (4, False): 'I',
                (4, True):  'i',
                (8, False): 'L',
                (8, True):  'l',
                }[(length, signed)]
        except KeyError:
            raise ValueError('unexpected unpacking length: %d' % length)
        self.file.seek(self.offset + offset)
        buf = self.file.read(length)
        if buf:
            return struct.unpack(fmt, buf)[0]
        return 0

    def n2s(self, offset, length):
        """Convert offset to string."""
        s = ''
        for dummy in range(length):
            if self.endian == 'I':
                s += chr(offset & 0xFF)
            else:
                s = chr(offset & 0xFF) + s
            offset = offset >> 8
        return s

    def _first_ifd(self):
        """Return first IFD."""
        return self.s2n(4, 4)

    def _next_ifd(self, ifd):
        """Return the pointer to next IFD."""
        entries = self.s2n(ifd, 2)
        next_ifd = self.s2n(ifd + 2 + 12 * entries, 4)
        if next_ifd == ifd:
            return 0
        else:
            return next_ifd

    def list_ifd(self):
        """Return the list of IFDs in the header."""
        i = self._first_ifd()
        ifds = []
        while i:
            ifds.append(i)
            i = self._next_ifd(i)
        return ifds

    def dump_ifd(self, ifd, ifd_name, tag_dict=EXIF_TAGS, relative=0, stop_tag=DEFAULT_STOP_TAG):
        """
        Return a list of entries in the given IFD.
        """
        # make sure we can process the entries
        try:
            entries = self.s2n(ifd, 2)
        except TypeError:
            logger.warning("Possibly corrupted IFD: %s" % ifd)
            return

        for i in range(entries):
            # entry is index of start of this IFD in the file
            entry = ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)

            # get tag name early to avoid errors, help debug
            tag_entry = tag_dict.get(tag)
            if tag_entry:
                tag_name = tag_entry[0]
            else:
                tag_name = 'Tag 0x%04X' % tag

            # ignore certain tags for faster processing
            if not (not self.detailed and tag in IGNORE_TAGS):
                field_type = self.s2n(entry + 2, 2)

                # unknown field type
                if not 0 < field_type < len(FIELD_TYPES):
                    if not self.strict:
                        continue
                    else:
                        raise ValueError('Unknown type %d in tag 0x%04X' % (field_type, tag))

                type_length = FIELD_TYPES[field_type][0]
                count = self.s2n(entry + 4, 4)
                offset = entry + 8
                if count * type_length > 4:
                    if relative:
                        tmp_offset = self.s2n(offset, 4)
                        offset = tmp_offset + ifd - 8
                        if self.fake_exif:
                            offset += 18
                    else:
                        offset = self.s2n(offset, 4)

                field_offset = offset
                values = None
                if field_type == 2:
                    if count != 0:  
                        file_position = self.offset + offset
                        try:
                            self.file.seek(file_position)
                            values = self.file.read(count)

                            # Drop any garbage after a null.
                            values = values.split(b'\x00', 1)[0]
                            if isinstance(values, bytes):
                                try:
                                    values = values.decode("utf-8")
                                except UnicodeDecodeError:
                                    logger.warning("Possibly corrupted field %s in %s IFD", tag_name, ifd_name)
                        except OverflowError:
                            logger.warn('OverflowError at position: %s, length: %s', file_position, count)
                            values = ''
                        except MemoryError:
                            logger.warn('MemoryError at position: %s, length: %s', file_position, count)
                            values = ''
                    else:
                        values = ''
                else:
                    values = []
                    signed = (field_type in [6, 8, 9, 10])
                    if count < 1000:
                        for dummy in range(count):
                            if field_type in (5, 10):
                                # a ratio
                                value = Ratio(self.s2n(offset, 4, signed),
                                              self.s2n(offset + 4, 4, signed))
                            elif field_type in (11,12):
                                # a float or double
                                unpack_format = ""
                                if self.endian == 'I':
                                    unpack_format += "<"
                                else:
                                    unpack_format += ">"
                                if field_type == 11:
                                    unpack_format += "f"
                                else:
                                    unpack_format += "d"
                                self.file.seek(self.offset + offset)
                                byte_str = self.file.read(type_length)
                                value = struct.unpack(unpack_format,byte_str)
                            else:
                                value = self.s2n(offset, type_length, signed)
                            values.append(value)
                            offset = offset + type_length
                    elif tag_name in ('MakerNote', makernote.canon.CAMERA_INFO_TAG_NAME):
                        for dummy in range(count):
                            value = self.s2n(offset, type_length, signed)
                            values.append(value)
                            offset = offset + type_length
                if count == 1 and field_type != 2:
                    printable = str(values[0])
                elif count > 50 and len(values) > 20 and not isinstance(values, basestring) :
                    if self.truncate_tags :
                        printable = str(values[0:20])[0:-1] + ", ... ]"
                    else:
                        printable = str(values[0:-1])
                else:
                    try:
                        printable = str(values)
                    except UnicodeEncodeError:
                        printable = unicode(values)
                if tag_entry:

                    if len(tag_entry) != 1:
                        if callable(tag_entry[1]):
                            printable = tag_entry[1](values)
                        elif type(tag_entry[1]) is tuple:
                            ifd_info = tag_entry[1]
                            try:
                                self.dump_ifd(values[0], ifd_info[0], tag_dict=ifd_info[1], stop_tag=stop_tag)
                            except IndexError:
                                logger.warn('No values found for %s SubIFD', ifd_info[0])
                        else:
                            printable = ''
                            for i in values:
                                printable += tag_entry[1].get(i, repr(i))

                self.tags[ifd_name + ' ' + tag_name] = IfdTag(printable, tag,
                                                              field_type,
                                                              values, field_offset,
                                                              count * type_length)
                try:
                    tag_value = repr(self.tags[ifd_name + ' ' + tag_name])
                except UnicodeEncodeError:
                    tag_value = unicode(self.tags[ifd_name + ' ' + tag_name])

            if tag_name == stop_tag:
                break



