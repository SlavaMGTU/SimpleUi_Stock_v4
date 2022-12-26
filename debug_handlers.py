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
    products = Set('Product', column='tags')


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    Name = Optional(str) #!!!!pony.orm.dbapiprovider.OperationalError: no such column: Product.Name
    Partnumber = Optional(str)
    Measure = Optional(str)
    tags = Set(Tag, column='products')
    list_products = Set('List_product', column='products')
    incomes = Set('Income', cascade_delete=False)
    buys = Set('Buy', cascade_delete=False)


class List_product(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Required(int, default=0)
    qty_income = Required(int, default=0)
    products = Set(Product, column='list_products')


class Income(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_income = Optional(int, default=0)
    products = Optional(Product)#, column='incomes'
    list_incomes = Optional('List_income', column='incomes')


class Buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Optional(int, default=0)
    products = Optional(Product)#, column='buys'
    list_buys = Optional('List_buy', column='buys')


class List_buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    buys = Set(Buy, cascade_delete=True)  # NotImplementedError:', column='list_buys' Parameter 'column' is not allowed for many-to-one attribute List_buy.buys


class List_income(db.Entity):
    id = PrimaryKey(int, auto=True)
    incomes = Set(Income, cascade_delete=True)  # NotImplementedError:', column='list_incomes' Parameter 'column' is not allowed for many-to-one attribute List_income.incomes


class Const(db.Entity):
    id = PrimaryKey(int, auto=True)# id=1/2 - Buy-List_Buy and id=3/4 - Income_List_income
    number = Optional(int, default=1)


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

        number_list = select(s for s in List_income).count()  # СЧИТАЕТ количество строк в БД

        # if number_list ==0:
        #     l = List_income()  # create NEW List_income

        query = select(c for c in List_income)
        for list_income in query:
            rows.append({'id': list_income.id, 'name': 'Поступление'})

    table['rows'] = rows
    hashMap.put('tab_list_income', json.dumps(table))

    return hashMap

def _list_income_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_new_income':

        with db_session:
            #i = Income()
            l = List_income()  # create NEW List_income #incomes=i
            number_income = l.id  # СЧИТАЕТ количество строк в БД!!!!
            cons = Const[4]
            cons.number = number_income #counted the number of rows in the List_income
            commit()

        hashMap.put('toast', 'добавлен НОВЫЙ список поступления')
        hashMap.put('ShowScreen', 'New_income')

    if hashMap.get('listener') == 'TableClick':# 'tab_list_income_click'

        selected_line = json.loads(hashMap.d.get('selected_line'))
        number_income = selected_line['id']
        with db_session:
            #i = Income()
            cons = Const[4]
            cons.number = number_income #counted the number of rows in the List_income
            commit()

        #hashMap.put('number_income', str(number_income))

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

    rows = []

    with db_session:#new table
        cons = Const[4]
        number_income = cons.number #counted the number of rows in the List_income
        lis=List_income[number_income]
        incomes=lis.incomes
        query = select(c for c in incomes)
        if hasattr(query, '__iter__'):
            for income in query:
                try:
                    name = income.products.Partnumber
                except AttributeError:
                    rows.append({'id': income.id, 'name': 'Наименование товара', 'qty_income': income.qty_income})
                else:
                    rows.append({'id': income.id, 'name': name, 'qty_income': income.qty_income})
        commit()

    table['rows'] = rows
    hashMap.put('tab_income', json.dumps(table))

    return hashMap

def _new_income_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_del_income':
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            number_income = selected_line['id']
            List_income[number_income].delete()  # del List_income
            commit()
        hashMap.put('toast', 'удален список поступления')
        hashMap.put('ShowScreen', 'List_income')

    if hashMap.get('listener') == 'btn_add_product':
        with db_session:
            cons1 = Const[4]
            number_list = cons1.number# get number from List_income
            list_income = List_income[number_list]# get List_income
            i = Income()  # create new Income
            list_income.incomes.add(i)
            cons = Const[3]
            cons.number = i.id #counted the number of ID in the Income
            commit()
        hashMap.put('toast', 'добавлена НОВая строчка товара')
        hashMap.put('ShowScreen', 'List_product')

    if hashMap.get('listener') == 'TableClick':#tab_income_click
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            cons = Const[3]
            cons.number = selected_line['id'] #counted the number of ID in the Income
            commit()
        hashMap.put('toast', 'Отредактируйте количество товара')
        hashMap.put('ShowScreen', 'Input_qty')

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
            rows.append({'id': product.id, 'name': product.Partnumber})#ERROR!!!! product.Partnumber -> product.Name

    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap

def _add_product_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'TableClick':#tab_product_click
        hashMap.put('ShowScreen', 'Input_qty')

    if hashMap.get('listener') == 'btn_new_product':
        hashMap.put('ShowScreen', 'New_income')

    return hashMap

def _listinput_qty_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_product = selected_line['name']
    hashMap.put('name_product', str(name_product))

    return hashMap

def _listinput_qty_on_input(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    qty_product = json.loads(hashMap.d.get('qty_product'))
    if hashMap.get('listener') == 'btn_qty':
        with db_session:
            if 'qty_income' in selected_line:
                p = Product.get(Partnumber=selected_line['name'])
            else:
                p = Product[selected_line['id']]  # Name=hashMap.get('name_product'),?????ОШИБКА!!! не те скобки????

            cons = Const[3]
            number_income = cons.number  # get the number of ID in the Income
            i = Income[number_income]
            i.qty_income = qty_product
            i.products = p

            commit()

    hashMap.remove('selected_line')# удаление строки для того чтоб не смещалось значения с Product на List_income
    hashMap.put('ShowScreen', 'New_income')
    hashMap.put('toast', 'добавлено кол-во товара в список поступления')

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
