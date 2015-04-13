# encoding:utf-8
import datetime
import time

import pytz


def datetime_to_timestamp(_datetime, TIME_ZONE):
    if type(_datetime) is datetime.date:
        _datetime = datetime.datetime(
            _datetime.year, _datetime.month, _datetime.day
        ).replace(tzinfo=pytz.utc
                  ).astimezone(pytz.timezone(TIME_ZONE))
    if not _datetime.tzinfo:
        raise ValueError('datetime.tzinfo not available')
    _datetime = _datetime.replace(tzinfo=_datetime.tzinfo).astimezone(
        pytz.timezone(TIME_ZONE))
    try:
        return time.mktime(_datetime.timetuple()) + \
            _datetime.microsecond / 1000000.0
    except:
        return time.mktime(_datetime.timetuple())


def timestamp_to_datetime(timestamp, TIME_ZONE):
    datetimee = datetime.datetime.utcfromtimestamp(timestamp)
    datetimee = datetimee.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone(TIME_ZONE))
    return datetimee


def clock(now_time=None):
    if not now_time:
        now_time = time.gmtime()
    return '%s%02d%02d' % (
        chr(now_time.tm_hour + 97).upper(),
        now_time.tm_min,
        now_time.tm_sec)
