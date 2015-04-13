# encoding:utf-8
from StringIO import StringIO
from struct import pack, unpack
import json


def writeBool(_bool):
    if _bool:
        return writeByte(1)
    else:
        return writeByte(0)


def writeByte(_byte):
    buf = StringIO()
    buf.write(pack("!b", _byte))
    buf.seek(0)
    return buf.buf


def writeI16(_i16):
    buf = StringIO()
    buf.write(pack("!h", _i16))
    buf.seek(0)
    return buf.buf


def writeI32(_i32):
    buf = StringIO()
    buf.write(pack("!i", _i32))
    buf.seek(0)
    return buf.buf


def writeI64(_i64):
    buf = StringIO()
    buf.write(pack("!q", _i64))
    buf.seek(0)
    return buf.buf


def writeDouble(_dub):
    buf = StringIO()
    buf.write(pack("!d", _dub))
    buf.seek(0)
    return buf.buf


def writeString(_str):
    return _str.encode('utf8')


def writeJson(_json):
    return writeString(json.dumps(_json, ensure_ascii=False))


def readBool(_bool):
    val = readByte(_bool)
    if val == 0:
        return False
    return True


def readByte(_byte):
    val, = unpack('!b', _byte)
    return val


def readI16(_i16):
    val, = unpack('!h', _i16)
    return val


def readI32(_i32):
    val, = unpack('!i', _i32)
    return val


def readI64(_i64):
    val, = unpack('!q', _i64)
    return val


def readDouble(_dub):
    val, = unpack('!d', _dub)
    return val


def readString(_str):
    return _str.decode('utf8')


def readJson(_json):
    return json.loads(readString(_json))
