# gps_reader.process_file('D:\\Temp\\2020-02-03-18-43-18-106.jpg') #

from .classes import *


def ord_(dta):
    if isinstance(dta, str):
        return ord(dta)
    return dta

def increment_base(data, base):
    return ord_(data[base + 2]) * 256 + ord_(data[base + 3]) + 2


def process_file(file, stop_tag=DEFAULT_STOP_TAG, details=True, strict=False, debug=False, truncate_tags=True, auto_seek=True):
    def _conver(value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)
        
    with open(file, 'rb') as f:
        
        if auto_seek:
            f.seek(0)
        fake_exif = 0
        data = f.read(12)
        if data[0:2] == b'\xFF\xD8':
            # it's a JPEG file
            base = 2
            while ord_(data[2]) == 0xFF and data[6:10] in (b'JFIF', b'JFXX', b'OLYM', b'Phot'):
                length = ord_(data[4]) * 256 + ord_(data[5])
                f.read(length - 8)
                data = b'\xFF\x00' + f.read(10)
                fake_exif = 1
                if base > 2:
                    base = base + length + 4 - 2
                else:
                    base = length + 4
            f.seek(0)
            data = f.read(base + 4000)
            while 1:
                if data[base:base + 2] == b'\xFF\xE1':
                    # APP1
                    if data[base + 4:base + 8] == b"Exif":
                        base -= 2
                        break
                    increment = increment_base(data, base)
                    base += increment
                else:
                    try:
                        increment = increment_base(data, base)
                    except IndexError:
                        return {}
                    else:
                        base += increment
            f.seek(base + 12)
            if ord_(data[2 + base]) == 0xFF and data[6 + base:10 + base] == b'Exif':
                offset = f.tell()
                endian = f.read(1)
            else:
                return {}
        else:
            return {}
        endian = chr(ord_(endian[0]))

        hdr = ExifHeader(f, endian, offset, fake_exif, strict, debug, details, truncate_tags)
        ifd_list = hdr.list_ifd()
        ctr = 0
        for ifd in ifd_list:
            if ctr != 0 or 1:
                ifd_name = 'IFD %d' % ctr
            hdr.dump_ifd(ifd, ifd_name, stop_tag=stop_tag)
            ctr += 1
        # EXIF IFD

        # deal with MakerNote contained in EXIF IFD
        # (Some apps use MakerNote tags but do not use a format for which we
        # have a description, do not process these).
        try:
            _ret = {"latitude": hdr.tags['GPS GPSLatitude'], "longitude":hdr.tags['GPS GPSLongitude']}
            # ret = re.findall("Ratio=\[(.*?)\]",str(_ret))
            ret = [_conver(hdr.tags['GPS GPSLatitude']), _conver(hdr.tags['GPS GPSLongitude'])]
        except:
            ret = []
        
        return ret
        
