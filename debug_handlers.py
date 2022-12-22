from pony.orm.core import db_session, PrimaryKey, Optional
from pony import orm
from pony.orm import Database,Required,Set,select,commit
from flask import Flask
from flask import request
import json

from pony.orm import select, db_session, commit

#import ui_global
from pony.utils import count

DB_PATH ='db.db'  #'db\\db.db'#new
#DB_PATH = 'sqlite_dev.db'
db = Database()#new

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)#new

class Record(db.Entity):#new
    barcode = Required(str)
    name = Required(str)
    qty = Required(int)


class Tag(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag_name = Optional(str)
    products = Set('Product')


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    #Name = Optional(str) #!!!!pony.orm.dbapiprovider.OperationalError: no such column: Product.Name
    Partnumber = Optional(str)
    Measure = Optional(str)
    tags = Set(Tag)
    list_products = Set('List_product')
    incomes = Set('Income')
    buys = Set('Buy')


class List_product(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Required(int, default=0)
    qty_income = Required(int, default=0)
    products = Set(Product)


class Income(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_income = Optional(int, default=0)
    products = Set(Product)
    list_incomes = Set('List_income')


class Buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Optional(int, default=0)
    products = Set(Product)
    list_buys = Set('List_buy')


class List_buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    buys = Set(Buy)


class List_income(db.Entity):
    id = PrimaryKey(int, auto=True)
    incomes = Set(Income)



app = Flask(__name__)


# -BEGIN CUSTOM HANDLERS

def _init_on_start():#new on_start
    db.generate_mapping(create_tables=True)

# def _init_on_start(hashMap, _files=None, _data=None):
#   ui_global.setup_db()
#   return hashMap

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
    rows = []
    with db_session:#new
        query = select(c for c in Record)#https://stackoverflow.com/questions/16115713/how-pony-orm-does-its-tricks
    #query = select(c for c in ui_global.Record)#https://stackoverflow.com/questions/16115713/how-pony-orm-does-its-tricks

        for record in query:
            rows.append({'barcode': record.barcode, 'name': record.name, 'qty': record.qty})

    table['rows'] = rows
    hashMap.put('tab_scan', json.dumps(table))

    return hashMap


def _barcode_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'barcode':
        #hashMap.get('barcode_input')
        hashMap.put('ShowScreen', 'Input-qty')

    return hashMap


def _input_qty(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_qty':
        with db_session:
            #p = ui_global.Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))
            p = Record(barcode=hashMap.get('barcode_input'), name=hashMap.get('nom'), qty=hashMap.get('qty'))#new
            commit()
            hashMap.put('ShowScreen', 'Scan-offline')
            hashMap.put('toast', 'Добавлено')

    return hashMap

def _list_income_on_start(hashMap, _files=None, _data=None):
    table = {
        'type': 'table',
        'textsize': '20',

        'columns': [
            {
                'name': 'name',
                'header': 'Name',
                'weight': '2'
            },
            {
                'name': 'id',
                'header': 'ID',
                'weight': '1'
            },
        ]
    }
    rows = []
    with db_session:#new
        query = select(c for c in List_income)
        for list_income in query:
            rows.append({'id': list_income.id, 'name': 'Поступление'})

    table['rows'] = rows
    hashMap.put('tab_list_income', json.dumps(table))

    return hashMap

def _list_income_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_new_income':

        hashMap.put('ShowScreen', 'New_income')

    if hashMap.get('listener') == 'TableClick':# 'tab_list_income_click'
        hashMap.put('ShowScreen', 'New_income')

    return hashMap


def _new_income_on_start(hashMap, _files=None, _data=None):
    table = {
        'type': 'table',
        'textsize': '20',

        'columns': [
            {
                'name': 'id',
                'header': 'ID',
                'weight': '1'
            },
            {
                'name': 'name',
                'header': 'Name',
                'weight': '2'
            },
            {
                'name': 'qty_income',
                'header': 'QTY',
                'weight': '1'
            },
        ]
    }

    try:
        selected_line = json.loads(hashMap.d.get('selected_line'))
    except:
        with db_session:
            i = Income()
            l = List_income(incomes=i)  # create NEW income
            number_income = select(s for s in List_income).count()# НЕПРАВИЛЬНО СЧИТАЕТ количество строк в БД!!!!
            commit()
            hashMap.put('toast', 'добавлен НОВЫЙ список поступления')
            hashMap.put('number_income', str(number_income))

    else:
        selected_line = json.loads(hashMap.d.get('selected_line'))
        number_income = selected_line['id']
        hashMap.put('number_income', str(number_income))

    # selected_line = json.loads(hashMap.d.get('selected_line'))
    # name_income = selected_line['id']
    # hashMap.put('name_income', 'Поступления '+ str(name_income))
    # if not hashMap.containsKey('qty_product'):
    #     hashMap.put('qty_product', '0')
   #hashMap.put('name_income', 'Поступления')
    rows = []
    with db_session:#new
        if hasattr(Income[number_income], '__iter__'):
            query = select(c for c in Income[number_income])
            for income in query:
                rows.append({'id': income.id, 'name': 'Название товара', 'qty_income': income.qty_income})

    table['rows'] = rows
    hashMap.put('tab_income', json.dumps(table))

    return hashMap

def _new_income_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_add_product':
        hashMap.put('ShowScreen', 'List_product')

    return hashMap

def _add_product_on_start(hashMap, _files=None, _data=None):
    table = {
        'type': 'table',
        'textsize': '20',

        'columns': [
            {
                'name': 'id',
                'header': 'ID',
                'weight': '1'
            },
            {
                'name': 'name',
                'header': 'Name',
                'weight': '2'
            },
        ]
    }
    rows = []
    with db_session:#new
        query = select(c for c in Product)
        for product in query:
            rows.append({'id': product.id, 'name': product.Partnumber})

    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap

def _add_product_on_input(hashMap, _files=None, _data=None):
    selected_line={}
    if hashMap.get('listener') == 'TableClick':
        hashMap.put('ShowScreen', 'Input_qty')

    # if hashMap.get('listener') == 'tab_product_click':
    #     var1 = 'selected_line_id'
    #     hashMap.put('ShowScreen', 'Input_qty')

    return hashMap

def _listinput_qty_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_product = selected_line['name']
    hashMap.put('name_product', str(name_product))
    if not hashMap.containsKey('qty_product'):
        hashMap.put('qty_product', '0')

    return hashMap

def _listinput_qty_on_input(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    if hashMap.get('listener') == 'btn_qty':
        with db_session:
            p = Product[selected_line['id']]  # Name=hashMap.get('name_product'),
            i = Income(qty_income= hashMap.get('qty_product') , products=p)
            l=List_income(incomes=i)# ЗАКЛАДКА!!!!
            commit()
            hashMap.put('ShowScreen', 'New_income')
            hashMap.put('toast', 'добавлен кол-ва товара в список поступления')

    return hashMap



def _listproduct_on_start(hashMap, _files=None, _data=None):
    table = {
        'type': 'table',
        'textsize': '20',

        'columns': [
            {
                'name': 'id',
                'header': 'ID',
                'weight': '1'
            },
            {
                'name': 'name',
                'header': 'Name',
                'weight': '2'
            },
        ]
    }
    rows = []
    with db_session:#new
        query = select(c for c in Product)
        for product in query:
            rows.append({'id': product.id, 'name': product.Partnumber})#Name})

    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap

def _listproduct_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_newproduct':
        hashMap.put('ShowScreen', 'New-product')

    return hashMap


def _newproduct_on_start(hashMap, _files=None, _data=None):

    str_measure = 'kg;pcs;m;m3' # не получается сделать всплывающий список
    hashMap.put('str_measure', 'kg')
    return hashMap


def _newproduct_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_save_newproduct':
        with db_session:
            #p = ui_global.Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))
            p = Product(Partnumber=hashMap.get('name_product'), Measure=hashMap.get('str_measure'))#Name=hashMap.get('name_product'),
            commit()
            hashMap.put('ShowScreen', 'List-product')
            hashMap.put('toast', 'Добавлен товар')

    return hashMap


# -END CUSTOM HANDLERS

@app.route('/set_input_direct/<method>', methods=['POST'])
def set_input(method):
    func = method
    jdata = json.loads(request.data.decode('utf-8'))
    f = globals()[func]
    hashMap.d = jdata['hashmap']
    #f()
    #f('hashmap')
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
    _init_on_start()#new
    app.run(host='0.0.0.0', port=2075, debug=True)
