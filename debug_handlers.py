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


class Tag(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag_name = Optional(str)
    products = Set('Product', column='tags')


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    Name = Optional(str)
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


def _list_buy_on_start(hashMap, _files=None, _data=None):
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

        number_list = select(s for s in List_buy).count()  # СЧИТАЕТ количество строк в БД

        # if number_list ==0:
        #     l = List_income()  # create NEW List_income

        query = select(c for c in List_buy)
        for list_buy in query:
            rows.append({'id': list_buy.id, 'name': 'Поступление'})

    table['rows'] = rows
    hashMap.put('tab_list_buy', json.dumps(table))

    return hashMap

def _list_buy_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_new_buy':

        with db_session:
            l = List_buy()  # create NEW List_buy
            number_buy = l.id  # номер id в БД!!!!
            cons = Const[2]
            cons.number = number_buy #counted the number of rows in the List_buy
            commit()

        hashMap.put('toast', 'добавлен НОВЫЙ список закупок')
        hashMap.put('ShowScreen', 'New_buy')

    if hashMap.get('listener') == 'TableClick':# 'tab_list_buy_click'

        selected_line = json.loads(hashMap.d.get('selected_line'))
        number_buy = selected_line['id']
        with db_session:
            #i = Buy()
            cons = Const[2]
            cons.number = number_buy #counted the number of rows in the List_buy
            commit()

        hashMap.put('ShowScreen', 'New_buy')

    return hashMap


def _new_buy_on_start(hashMap, _files=None, _data=None):
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
                'name': 'qty_buy',
                'header': 'QTY',
                'weight': '1'
            },
        ]
    }

    rows = []

    with db_session:#new table
        cons = Const[2]
        number_buy = cons.number #counted the number of rows in the List_buy
        lis=List_buy[number_buy]
        buys=lis.buys
        query = select(c for c in buys)
        if hasattr(query, '__iter__'):
            for buy in query:
                try:
                    name = buy.products.Name
                except AttributeError:
                    rows.append({'id': buy.id, 'name': 'Наименование товара', 'qty_income': buy.qty_buy})
                else:
                    rows.append({'id': buy.id, 'name': name, 'qty_buy': buy.qty_buy})
        commit()

    table['rows'] = rows
    hashMap.put('tab_buy', json.dumps(table))

    return hashMap

def _new_buy_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'btn_del_buy':
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            number_buy = selected_line['id']
            List_buy[number_buy].delete()  # del List_buy
            commit()
        hashMap.put('toast', 'удален список закупки')
        hashMap.put('ShowScreen', 'List_buy')

    if hashMap.get('listener') == 'btn_add_product':
        with db_session:
            cons1 = Const[2]
            number_list = cons1.number# get number from List_buy
            list_buy = List_buy[number_list]# get List_buy
            i = Buy()  # create new Buy
            list_buy.buys.add(i)
            cons = Const[1]
            cons.number = i.id #counted the number of ID in the Buy
            commit()
        hashMap.put('toast', 'добавлена НОВая строчка товара')
        hashMap.put('ShowScreen', 'List_buy_product')

    if hashMap.get('listener') == 'TableClick':#tab_buy_click
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            cons = Const[1]
            cons.number = selected_line['id'] #counted the number of ID in the Buy
            commit()
        hashMap.put('toast', 'Отредактируйте количество товара')
        hashMap.put('ShowScreen', 'Input_buy_qty')

    return hashMap

def _add_product_buy_on_start(hashMap, _files=None, _data=None):
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
            rows.append({'id': product.id, 'name': product.Name})#ERROR!!!! product.Partnumber -> product.Name

    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap

def _add_product_buy_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'TableClick':#tab_buy_product_click
        hashMap.put('ShowScreen', 'Input_buy_qty')

    if hashMap.get('listener') == 'btn_new_buy_product':
        hashMap.put('ShowScreen', 'New_buy')

    return hashMap

def _listinput_qty_buy_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_buy_product = selected_line['name']
    hashMap.put('name_buy_product', str(name_buy_product))

    return hashMap

def _listinput_qty_buy_on_input(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    qty_buy_product = json.loads(hashMap.d.get('qty_buy_product'))
    if hashMap.get('listener') == 'btn_buy_qty':
        with db_session:
            if 'qty_buy_income' in selected_line:
                p = Product.get(Name=selected_line['name'])
            else:
                p = Product[selected_line['id']]  # Name=hashMap.get('name_buy_product'),?????ОШИБКА!!! не те скобки????

            cons = Const[1]
            number_buy = cons.number  # get the number of ID in the Buy
            i = Buy[number_buy]
            i.qty_buy = qty_buy_product
            i.products = p
            commit()

    hashMap.remove('selected_line')# удаление строки для того чтоб не смещалось значения с Product на List_income
    hashMap.put('ShowScreen', 'New_buy')
    hashMap.put('toast', 'добавлено кол-во товара в список закупок')

    return hashMap



# begin Income

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

    if hashMap.get('listener') == 'TableClick':# 'tab_list_income_click'

        selected_line = json.loads(hashMap.d.get('selected_line'))
        #number_income = selected_line['id']
        hashMap.put('number_list_income', str(selected_line['id']))#counted the number of rows in the List_income
        # with db_session:
        #     #i = Income()
        #     cons = Const[4]
        #     cons.number = number_income #counted the number of rows in the List_income
        #     commit()

        #hashMap.put('number_income', str(number_income))

        hashMap.put('ShowScreen', 'New_income')

    if hashMap.get('listener') == 'btn_new_income':

        with db_session: # search for the maximum "id" in List_income
            number_income = 0
            query = select(c for c in List_income)
            for list_income in query:
                if list_income.id>number_income:
                    number_income = list_income.id # id строки в БД
            number_income += 1

            # cons = Const[4]
            # cons.number = number_income #counted the number of rows in the List_income
        with db_session:
            l = List_income(id = number_income)  # create NEW List_income #incomes=i
            commit()
        hashMap.put('number_list_income', str(number_income))#counted the number of rows in the List_income
        hashMap.put('toast', 'добавлен НОВЫЙ список поступления')
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
        # cons = Const[4]
        # number_income = cons.number #counted the number of rows in the List_income
        number_income = int(json.loads(hashMap.d.get('number_list_income'))) #counted the number of rows in the List_income
        l=List_income[number_income]
        incomes=l.incomes
        query = select(c for c in incomes)
        if hasattr(query, '__iter__'):
            for income in query:
                try:
                    name = income.products.Name
                except AttributeError:
                    rows.append({'id': income.id, 'name': 'Наименование товара', 'qty_income': income.qty_income})
                else:
                    rows.append({'id': income.id, 'name': name, 'qty_income': income.qty_income})
        #commit()
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
        number_list = json.loads(hashMap.d.get('number_list_income'))  # get number from List_income
        number_income = 0  # search for the maximum "id" in number_income
        with db_session:

            query = select(c for c in Income)
            for income in query:
                if income.id > number_income:
                    number_income = income.id  # id строки в БД
            number_income += 1
            #l = Income(id=number_income, list_incomes =number_list)  # create NEW Income #incomes=i

            #commit()
        hashMap.put('number_income', str(number_income))#counted the number of rows in the Income
        hashMap.put('toast', 'добавлена НОВая строчка товара')
        hashMap.put('ShowScreen', 'List_product')

    if hashMap.get('listener') == 'TableClick':#tab_income_click
        selected_line = json.loads(hashMap.d.get('selected_line'))
        # with db_session:
        #
        #     cons = Const[3]
        #     cons.number = selected_line['id'] #counted the number of ID in the Income
        #     commit()
        hashMap.put('number_income', str(selected_line['id']))# the number of rows in the Income
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
    number_income = json.loads(hashMap.d.get('number_list_income'))
    with db_session:#new
        query = select(c for c in Product)
        # cons = Const[4]
        # number_income = cons.number #counted the number of rows in the List_income
        l=List_income[number_income]
        incomes=l.incomes
        query1 = select(s for s in incomes)
        for product in query:
            print_yes = True
            if hasattr(query1, '__iter__'):
                for income in query1:
                    try:
                        name = income.products.Name
                    except AttributeError:
                        income.delete()  # del error Income
                    else:
                        if income.products.Name == product.Name: # Если товар есть в поступлении(Income) - НЕ печатать в Табл
                            print_yes = False
            if print_yes == True:
                rows.append({'id': product.id, 'name': product.Name})
        #commit()
    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap

def _add_product_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'TableClick':#tab_product_click
        hashMap.put('ShowScreen', 'Input_new_qty')

    if hashMap.get('listener') == 'btn_new_product':# NOT working yet!!!
        hashMap.put('ShowScreen', 'Input_new_qty')

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
            Income[selected_line['id']].qty_income=qty_product# Изменение количества товара
            commit()

    hashMap.remove('selected_line')# удаление строки для того чтоб не смещалось значения с Product на List_income
    hashMap.put('ShowScreen', 'New_income')
    hashMap.put('toast', 'изменение кол-ва товара в списке поступления')

    return hashMap


def _listinput_new_qty_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_product = selected_line['name']
    hashMap.put('new_name_product', str(name_product))

    return hashMap

def _listinput_new_qty_on_input(hashMap, _files=None, _data=None):

    selected_line = json.loads(hashMap.d.get('selected_line'))
    number_list_income = json.loads(hashMap.d.get('number_list_income'))
    number_income = json.loads(hashMap.d.get('number_income'))
    qty_product = json.loads(hashMap.d.get('new_qty_product'))

    if hashMap.get('listener') == 'btn_new_qty':
        with db_session:
            p = Product[selected_line['id']]

            # cons = Const[3]
            # number_income = cons.number  # get the number of ID in the Income

            i = Income(id=number_income)
            i.qty_income = qty_product
            i.list_incomes = number_list_income
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
            rows.append({'id': product.id, 'name': product.Name})#Name})

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
            p = Product(Name=hashMap.get('name_product'), Measure=hashMap.get('str_measure'))#Name=hashMap.get('name_product'),
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
