from pony.orm.core import db_session
from pony import orm
from pony.orm import Database,Required,Set,select,commit
from flask import Flask
from flask import request
import json


from pony.orm import select, db_session, commit



DB_PATH ='db.db'  #'db\\db.db'#new
#DB_PATH = 'sqlite_dev.db'
db = Database()#new

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)#new
#


class Record(db.Entity):#new
    barcode = Required(str)
    name = Required(str)
    qty = Required(int)

app = Flask(__name__)


# -BEGIN CUSTOM HANDLERS

def _init():#new
    db.generate_mapping(create_tables=True)

def _sample1_on_create(hashMap, _files=None, _data=None):
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





def _barcode_on_start(hashMap, _files=None, _data=None):
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
    with db_session:#new
        query = select(c for c in Record)#https://stackoverflow.com/questions/16115713/how-pony-orm-does-its-tricks
        rows = []
        for record in query:
            rows.append({'barcode': record.barcode, 'name': record.name, 'qty': record.qty})

    table['rows'] = rows
    hashMap.put('table', json.dumps(table))

    return hashMap


def _barcode_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'barcode_input':
        hashMap.get('barcode_input')
        hashMap.put('ShowScreen', 'Input-qty')

    return hashMap


def _input_qty(hashMap, _files=None, _data=None):
    with db_session:
        p = Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))#new
        commit()

    hashMap.put('ShowScreen', 'Input-qty')
    hashMap.put('toast', 'Добавлено')
    return hashMap


# -END CUSTOM HANDLERS

@app.route('/set_input_direct/<method>', methods=['POST'])
def set_input(method):
    func = method
    jdata = json.loads(request.data.decode('utf-8'))
    f = globals()[func]
    hashMap.d = jdata['hashmap']
    #f()
    f(hashMap)#new
    jdata['hashmap'] = hashMap.export()
    jdata['stop'] = False
    jdata['ErrorMessage'] = ''
    jdata['Rows'] = []

    return json.dumps(jdata)


@app.route('/post_screenshot', methods=['POST'])
def post_screenshot():
    d = request.data
    return '1'


class hashMap:
    d = {}

    def put(key, val):
        hashMap.d[key] = val

    def get(key):
        return hashMap.d.get(key)

    def remove(key):
        if key in hashMap.d:
            hashMap.d.pop(key)

    def containsKey(key):
        return key in hashMap.d

    def export():  # It's NOT error!!!
        ex_hashMap = []
        for key in hashMap.d.keys():
            ex_hashMap.append({'key': key, 'value': hashMap.d[key]})
        return ex_hashMap


if __name__ == '__main__':
    _init()#new
    app.run(host='0.0.0.0', port=2075, debug=True)