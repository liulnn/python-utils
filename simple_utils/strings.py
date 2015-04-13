# encoding:utf-8
import functools
import hashlib
import string
import uuid


try:
    import simplejson as json
except ImportError:
    import json

json_dumps = functools.partial(json.dumps, ensure_ascii=False)
md5 = lambda x: hashlib.md5(x.encode('raw_unicode_escape')).hexdigest()

unique_uuid = lambda: uuid.uuid4().hex


def random(length, letters=True, digits=True, filters=['O', 'o', '0']):
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
