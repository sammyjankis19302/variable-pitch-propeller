"""Extract the preview picture that SolidWorks (2015 and later) stores inside a .SLDPRT/.SLDASM file.
Usage: python3 -I tools/sw_preview.py <file> <out.png>
SolidWorks files are a chain of zlib-compressed streams; one of them, PreviewPNG, is the thumbnail
the file browser shows. No SolidWorks needed."""
import struct, sys, zlib

MARKER = b'\x14\x00\x06\x00\x08\x00'

def streams(path):
    data = open(path, 'rb').read()
    i = data.find(MARKER)
    while i >= 0:
        try:
            csize, usize, nlen = struct.unpack('<III', data[i + 14:i + 26])
        except struct.error:
            break
        name = bytes(((b >> 4) | (b << 4)) & 0xFF for b in data[i + 26:i + 26 + nlen])  # names are nibble-swapped
        payload = data[i + 26 + nlen:i + 26 + nlen + csize]
        try:
            out = zlib.decompressobj(-15).decompress(payload)
        except zlib.error:
            out = None
        yield name.decode('ascii', 'replace'), out
        i = data.find(MARKER, i + 26 + nlen + csize if out is not None else i + 1)

def preview(path):
    best = None
    for name, out in streams(path):
        if out and out[:8] == b'\x89PNG\r\n\x1a\n' and (best is None or len(out) > len(best)):
            best = out
    return best

if __name__ == '__main__':
    png = preview(sys.argv[1])
    if png is None:
        sys.exit('no preview found in ' + sys.argv[1])
    open(sys.argv[2], 'wb').write(png)
