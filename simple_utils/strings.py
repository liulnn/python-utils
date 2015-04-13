# encoding:utf-8
import functools
import hashlib
import random
import string
import uuid


try:
    import simplejson as json
except ImportError:
    import json

json_dumps = functools.partial(json.dumps, ensure_ascii=False)
unique_uuid = lambda: uuid.uuid4().hex


def md5_hex_digest(x):
    return hashlib.md5(x.encode('raw_unicode_escape')).hexdigest()


def random_sample(length, letters=True, digits=True, filters=['O', 'o', '0']):
    if letters and not digits:
        raw_string = string.letters
    elif not letters and digits:
        raw_string = string.digits
    else:
        raw_string = string.letters + string.digits
    return ''.join(random.sample(
        filter((lambda x: False if x in filters else True), raw_string),
        length
        ))
