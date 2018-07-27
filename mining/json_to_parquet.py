# -*- coding: utf-8 -*-

import time
import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd


def json_to_parquet(data, output, schema):
    column_data = {}
    array_data = []

    for row in data:
        for column in schema.names:
            _col = column_data.get(column, [])
            _col.append(row.get(column))
            column_data[column] = _col

    for column in schema:
        _col = column_data.get(column.name)
        if isinstance(column.type, pa.lib.TimestampType):
            _converted_col = []
            for t in _col:
                try:
                    _converted_col.append(pd.to_datetime(t))
                except pd._libs.tslib.OutOfBoundsDatetime:
                    _converted_col.append(pd.Timestamp.max)
            array_data.append(pa.Array.from_pandas(pd.to_datetime(_converted_col), type=pa.timestamp('ms')))
        # Float types are ambiguous for conversions, need to specify the exact type
        elif column.type.id == pa.float64().id:
            array_data.append(pa.array(_col, type=pa.float64()))
        elif column.type.id == pa.float32().id:
            # Python doesn't have a native float32 type
            # and PyArrow cannot cast float64 -> float32
            _col = pd.to_numeric(_col, downcast='float')
            array_data.append(pa.Array.from_pandas(_col, type=pa.float32()))
        elif column.type.id == pa.int64().id:
            array_data.append(pa.array([int(ele) for ele in _col], type=pa.int64()))
        else:
            array_data.append(pa.array(_col, type=column.type))

    data = pa.RecordBatch.from_arrays(array_data, schema.names)

    try:
        table = pa.Table.from_batches(data)
    except TypeError:
        table = pa.Table.from_batches([data])

    pq.write_table(table, output, compression='SNAPPY', coerce_timestamps='ms')


if __name__ == '__main__':
    schema = pa.schema([
        pa.field('name', pa.string()),
        pa.field('labels', pa.list_(pa.string())),
        pa.field('created', pa.timestamp('ms')),
        pa.field('valid', pa.bool_()),
        pa.field('status', pa.int64()),
    ])
    data = [
        {
            'name': 'a',
            'labels': ['A', 'B'],
            'created': int(28800000 + 1000 * time.mktime(datetime.datetime(2018, 8, 1).date().timetuple())),
            'valid': True,
            'status': 1,
        },
        {
            'name': 'b',
            'labels': ['B', 'C'],
            'created': int(28800000 + 1000 * time.mktime(datetime.datetime(2018, 8, 2).date().timetuple())),
            'valid': False,
            'status': 2,
        },
    ]
    json_to_parquet(data, 'a', schema)
    table2 = pq.read_table('a')
    print table2.to_pandas()
