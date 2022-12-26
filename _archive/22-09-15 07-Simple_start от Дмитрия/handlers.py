from pony.orm.core import db_session
from pony import orm
from pony.orm import Database,Required,Set,select,commit

import json



import ui_global



def sample1_on_create(hashMap, _files=None, _data=None):
    if not hashMap.containsKey('a'):
        hashMap.put('a', '')
    if not hashMap.containsKey('b'):
        hashMap.put('b', '')
    return hashMap


def _sample1_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_res':
        sum = int(hashMap.get('a')) + int(hashMap.get('b'))
        hashMap.put('toast', str(int(hashMap.get('a')) + int(hashMap.get('b'))))
    return hashMap


def init_on_start(hashMap, _files=None, _data=None):
    ui_global.init()
    return hashMap


def barcode_on_start(hashMap, _files=None, _data=None):
    table = {
        'type': 'table',
        'textsize': '20',

        'columns': [
            {
                'name': 'barcode',
                'header': 'Barcode',
                'weight': '2'
            },
            {
                'name': 'name',
                'header': 'Name',
                'weight': '2'
            },
            {
                'name': 'qty',
                'header': 'Qty.',
                'weight': '1'
            }
        ]
    }
    # work with SQL via Pony ORM
    query = select(c for c in ui_global.Record)#https://stackoverflow.com/questions/16115713/how-pony-orm-does-its-tricks
    rows = []
    for record in query:
        rows.append({'barcode': record.barcode, 'name': record.name, 'qty': record.qty})

    table['rows'] = rows
    hashMap.put('table', json.dumps(table))

    return hashMap


def barcode_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'barcode_input':
        hashMap.get('barcode_input')
        hashMap.put('ShowScreen', 'Input-qty')

    return hashMap


def _input_qty(hashMap, _files=None, _data=None):
    with db_session:
        p = ui_global.Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))
        commit()

    hashMap.put('ShowScreen', 'Input-qty')
    hashMap.put('toast', 'Добавлено')
    return hashMap


