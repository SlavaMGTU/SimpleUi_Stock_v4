from pony.orm.core import db_session, PrimaryKey, Optional
from pony import orm
from pony.orm import Database, Required, Set, select, commit
from flask import Flask
from flask import request
import json

from pony.orm import select, db_session, commit

# import ui_global
from pony.utils import count

DB_PATH = 'db.db'  # 'db\\db.db'#new
# DB_PATH = 'sqlite_dev.db'
db = Database()  # new

db.bind(provider='sqlite', filename=DB_PATH, create_db=True)  # new


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
    list_products = Set('List_product') #, column='products' - Parameter 'column' is not allowed for many-to-one attribute Product.list_products
    incomes = Set('Income', cascade_delete=False)
    buys = Set('Buy', cascade_delete=False)


class List_product(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Required(int, default=0)
    qty_income = Required(int, default=0)
    products = Required(Product)#, column='list_products' no such column: List_product.list_products


class Income(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_income = Optional(int, default=0)
    products = Optional(Product)  # , column='incomes'
    list_incomes = Optional('List_income', column='incomes')


class Buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    qty_buy = Optional(int, default=0)
    products = Optional(Product)  # , column='buys'
    list_buys = Optional('List_buy', column='buys')


class List_buy(db.Entity):
    id = PrimaryKey(int, auto=True)
    buys = Set(Buy, cascade_delete=True)  # NotImplementedError:', column='list_buys' Parameter 'column' is not allowed for many-to-one attribute List_buy.buys


class List_income(db.Entity):
    id = PrimaryKey(int, auto=True)
    incomes = Set(Income, cascade_delete=True)  # NotImplementedError:', column='list_incomes' Parameter 'column' is not allowed for many-to-one attribute List_income.incomes


class Const(db.Entity):
    id = PrimaryKey(int, auto=True)  # id=1/2 - Buy-List_Buy and id=3/4 - Income_List_income
    number = Optional(int, default=1)


app = Flask(__name__)


# -BEGIN CUSTOM HANDLERS


def _init_on_start():  # new on_start
    db.generate_mapping(create_tables=True)

# begin Buy


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
    with db_session:  # new

        query = select(c for c in List_buy)
        for list_buy in query:
            rows.append({'id': list_buy.id, 'name': '??????????????'})

    table['rows'] = rows
    hashMap.put('tab_list_buy', json.dumps(table))

    return hashMap


def _list_buy_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'TableClick':  # 'tab_list_buy_click'
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_list_buy', str(selected_line['id']))  # counted the number of rows in the List_income
        hashMap.put('ShowScreen', 'New_buy')

    if hashMap.get('listener') == 'btn_new_buy':

        with db_session:  # search for the maximum "id" in List_buy
            number_list_buy = 0 #!!! ERrOR - !!!???????? ???????????????? ?? ??????-?? ?????????????? ?????????????? ??????-???? ?????? ?????????????????? ?????????? ???????????? ??????????????????
            query = select(c for c in List_buy)
            for list_buy in query:
                if list_buy.id > number_list_buy:
                    number_list_buy = list_buy.id  # id ???????????? ?? ????
            number_list_buy += 1
        with db_session:
            l = List_buy(id=number_list_buy)  # create NEW List_buy
            commit()
        hashMap.put('number_list_buy', str(number_list_buy))  # counted the number of rows in the List_buy
        hashMap.put('toast', '???????????????? ?????????? ???????????? ??????????????')
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
                'name': 'qty_income',
                'header': 'QTY',
                'weight': '1'
            },
        ]
    }

    rows = []

    with db_session:  # new table !!! ERrOR - !!! ??????-???? ?????? ?????????????????? ?????????? ???????????? ??????????????????
        number_list_buy = json.loads(hashMap.d.get('number_list_buy'))  # counted the number of rows in the List_buy
        l = List_buy[number_list_buy]
        buys = l.buys
        query = select(c for c in buys)
        if hasattr(query, '__iter__'):# ERROR!!!! ?????? ???? ?????????????? - ???????????? ???????????? ????????????
            for buy in query:
                try:
                    name = buy.products.Name
                except AttributeError:
                    rows.append({'id': buy.id, 'name': '???????????????????????? ????????????', 'qty_buy': buy.qty_buy})
                else:
                    rows.append({'id': buy.id, 'name': name, 'qty_buy': buy.qty_buy})
    table['rows'] = rows
    hashMap.put('number_list_buy', str(number_list_buy))
    hashMap.put('tab_buy1', json.dumps(table))# ?????????????? ?? ?????????? ???? ???????????????????? ERROR!!!!!!!

    return hashMap


def _new_buy_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_del_buy':
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            number_list_buy = selected_line['id']
            List_buy[number_list_buy].delete()  # del List_buy
            commit()
        hashMap.put('toast', '???????????? ???????????? ??????????????')
        hashMap.put('ShowScreen', 'List_buy')

    if hashMap.get('listener') == 'btn_add_product_buy':
        number_list = json.loads(hashMap.d.get('number_list_buy'))  # get number from List_buy
        number_buy = 0  # search for the maximum "id" in number_buy
        with db_session:
            query = select(c for c in Buy)
            for buy in query:
                if buy.id > number_buy:
                    number_buy = buy.id  # id ???????????? ?? ????
            number_buy += 1
        hashMap.put('number_buy', str(number_buy))  # counted the number of rows in the Buy
        hashMap.put('toast', '?????????????????? ?????????? ?????????????? ????????????')
        hashMap.put('ShowScreen', 'List_product_buy')

    if hashMap.get('listener') == 'TableClick':  # tab_buy1_click
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_buy', str(selected_line['id']))  # the number of rows in the Buy
        hashMap.put('toast', '???????????????????????????? ???????????????????? ????????????')
        hashMap.put('ShowScreen', 'Input_qty_buy')

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
    number_buy = json.loads(hashMap.d.get('number_list_buy'))
    with db_session:  # new #  !!! ERrOR - !!! ??????-???? ?????? ?????????????????? ?????????? ???????????? ??????????????????
        query = select(c for c in Product)
        # for product in query:
        #     rows.append({'id': product.id, 'name': product.Name})
        l = List_buy[number_buy]
        buys = l.buys
        query1 = select(s for s in buys)
        for product in query:
            print_yes = True
            if hasattr(query1, '__iter__'):
                for buy in query1:
                    try:
                        name = buy.products.Name
                    except AttributeError:
                        buy.delete()  # del error Buy
                    else:
                        if buy.products.Name == product.Name:  # ???????? ?????????? ???????? ?? ?????????????? (Buy) - ???? ???????????????? ?? ????????
                            print_yes = False
            if print_yes == True:
                rows.append({'id': product.id, 'name': product.Name})
    table['rows'] = rows
    hashMap.put('tab_product_buy', json.dumps(table))

    return hashMap


def _add_product_buy_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'TableClick':  # tab_product_buy_click
        hashMap.put('ShowScreen', 'Input_new_qty_buy')

    if hashMap.get('listener') == 'btn_new_product_buy':  # NOT working yet!!!
        hashMap.put('ShowScreen', 'Input_new_qty_buy')

    return hashMap


def _listinput_qty_buy_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_product = selected_line['name']
    hashMap.put('name_product_buy', str(name_product))

    return hashMap


def _listinput_qty_buy_on_input(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    qty_product = json.loads(hashMap.d.get('qty_product_buy'))
    if hashMap.get('listener') == 'btn_qty_buy':
        with db_session:
            Buy[selected_line['id']].qty_buy = qty_product  # ?????????????????? ???????????????????? ????????????
            commit()

    hashMap.remove('selected_line')  # ???????????????? ???????????? ?????? ???????? ???????? ???? ?????????????????? ???????????????? ?? Product ???? List_buy
    hashMap.put('ShowScreen', 'New_buy')
    hashMap.put('toast', '?????????????????? ??????-???? ???????????? ?? ???????????? ??????????????')

    return hashMap


def _listinput_new_qty_buy_on_start(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    name_product = selected_line['name']
    hashMap.put('new_name_product_buy', str(name_product))

    return hashMap


def _listinput_new_qty_buy_on_input(hashMap, _files=None, _data=None):
    selected_line = json.loads(hashMap.d.get('selected_line'))
    number_list_buy = json.loads(hashMap.d.get('number_list_buy'))
    number_buy = json.loads(hashMap.d.get('number_buy'))
    qty_product = json.loads(hashMap.d.get('new_qty_product_buy'))

    if hashMap.get('listener') == 'btn_new_qty_buy':
        with db_session:
            p = Product[selected_line['id']]
            i = Buy(id=number_buy)
            i.qty_buy = qty_product
            i.list_buys = number_list_buy
            i.products = p
            commit()

    hashMap.remove('selected_line')  # ???????????????? ???????????? ?????? ???????? ???????? ???? ?????????????????? ???????????????? ?? Product ???? List_income
    hashMap.put('ShowScreen', 'New_buy')
    hashMap.put('toast', '?????????????????? ?????????????? ???????????? ?? ???????????? ??????????????')

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
    with db_session:  # new

        number_list = select(s for s in List_income).count()  # ?????????????? ???????????????????? ?????????? ?? ????
        query = select(c for c in List_income)
        for list_income in query:
            rows.append({'id': list_income.id, 'name': '??????????????????????'})

    table['rows'] = rows
    hashMap.put('tab_list_income', json.dumps(table))

    return hashMap


def _list_income_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'TableClick':  # 'tab_list_income_click'
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_list_income', str(selected_line['id']))  # counted the number of rows in the List_income
        hashMap.put('ShowScreen', 'New_income')

    if hashMap.get('listener') == 'btn_new_income':

        with db_session:  # search for the maximum "id" in List_income
            number_income = 0
            query = select(c for c in List_income)
            for list_income in query:
                if list_income.id > number_income:
                    number_income = list_income.id  # id ???????????? ?? ????
            number_income += 1
        with db_session:
            l = List_income(id=number_income)  # create NEW List_income #incomes=i
            commit()
        hashMap.put('number_list_income', str(number_income))  # counted the number of rows in the List_income
        hashMap.put('toast', '???????????????? ?????????? ???????????? ??????????????????????')
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

    with db_session:  # new table
        number_income = json.loads(hashMap.d.get('number_list_income'))  # counted the number of rows in the List_income
        l = List_income[number_income]
        incomes = l.incomes
        query = select(c for c in incomes)
        if hasattr(query, '__iter__'):
            for income in query:
                try:
                    name = income.products.Name
                except AttributeError:
                    rows.append({'id': income.id, 'name': '???????????????????????? ????????????', 'qty_income': income.qty_income})
                else:
                    rows.append({'id': income.id, 'name': name, 'qty_income': income.qty_income})
    table['rows'] = rows
    hashMap.put('number_list_income', str(number_income))
    hashMap.put('tab_income', json.dumps(table))

    return hashMap


def _new_income_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_del_income':
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            number_income = selected_line['id']
            List_income[number_income].delete()  # del List_income
            commit()
        hashMap.put('toast', '???????????? ???????????? ??????????????????????')
        hashMap.put('ShowScreen', 'List_income')

    if hashMap.get('listener') == 'btn_add_product':
        number_list = json.loads(hashMap.d.get('number_list_income'))  # get number from List_income
        number_income = 0  # search for the maximum "id" in number_income
        with db_session:
            query = select(c for c in Income)
            for income in query:
                if income.id > number_income:
                    number_income = income.id  # id ???????????? ?? ????
            number_income += 1
        hashMap.put('number_income', str(number_income))  # counted the number of rows in the Income
        hashMap.put('toast', '?????????????????? ?????????? ?????????????? ????????????')
        hashMap.put('ShowScreen', 'List_product')

    if hashMap.get('listener') == 'TableClick':  # tab_income_click
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_income', str(selected_line['id']))  # the number of rows in the Income
        hashMap.put('toast', '???????????????????????????? ???????????????????? ????????????')
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
    with db_session:  # new
        query = select(c for c in Product)
        l = List_income[number_income]
        incomes = l.incomes
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
                        if income.products.Name == product.Name:  # ???????? ?????????? ???????? ?? ??????????????????????(Income) - ???? ???????????????? ?? ????????
                            print_yes = False
            if print_yes == True:
                rows.append({'id': product.id, 'name': product.Name})
    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap


def _add_product_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'TableClick':  # tab_product_click
        hashMap.put('ShowScreen', 'Input_new_qty')

    if hashMap.get('listener') == 'btn_new_product':  # NOT working yet!!!
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
            Income[selected_line['id']].qty_income = qty_product  # ?????????????????? ???????????????????? ????????????
            commit()

    hashMap.remove('selected_line')  # ???????????????? ???????????? ?????? ???????? ???????? ???? ?????????????????? ???????????????? ?? Product ???? List_income
    hashMap.put('ShowScreen', 'New_income')
    hashMap.put('toast', '?????????????????? ??????-???? ???????????? ?? ???????????? ??????????????????????')

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
            i = Income(id=number_income)
            i.qty_income = qty_product
            i.list_incomes = number_list_income
            i.products = p
            commit()

    hashMap.remove('selected_line')  # ???????????????? ???????????? ?????? ???????? ???????? ???? ?????????????????? ???????????????? ?? Product ???? List_income
    hashMap.put('ShowScreen', 'New_income')
    hashMap.put('toast', '?????????????????? ??????-???? ???????????? ?? ???????????? ??????????????????????')

    return hashMap


def _listproduct_all_on_start(hashMap, _files=None, _data=None):
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
                'header': 'Buy',
                'weight': '1'
            },
            {
                'name': 'qty_income',
                'header': 'Inc',
                'weight': '1'
            },
        ]
    }

    rows = []

    with db_session:  # new table

        query = select(c for c in Product)
        for product in query:
            id = product.id
            sum_qty_income=0
            sum_qty_buy=0
            #query1 = select(s for s in product.incomes.qty_income)
            for qty_buy in product.buys.qty_buy:
                sum_qty_buy = sum_qty_buy + qty_buy
            for qty_income in product.incomes.qty_income:
                sum_qty_income = sum_qty_income + qty_income
            rows.append({'id': product.id, 'name': product.Name, 'qty_income': sum_qty_income, 'qty_buy':sum_qty_buy})  # Name}) ,

        # if hasattr(query, '__iter__'):
        #     for product in query:
        #         rows.append({'id': product.id, 'name': product.name, 'qty_income': product.qty_income})
    table['rows'] = rows

    hashMap.put('tab_all_product', json.dumps(table))

    return hashMap


def _new_income_on_input(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_del_income':
        with db_session:
            selected_line = json.loads(hashMap.d.get('selected_line'))
            number_income = selected_line['id']
            List_income[number_income].delete()  # del List_income
            commit()
        hashMap.put('toast', '???????????? ???????????? ??????????????????????')
        hashMap.put('ShowScreen', 'List_income')

    if hashMap.get('listener') == 'btn_add_product':
        number_list = json.loads(hashMap.d.get('number_list_income'))  # get number from List_income
        number_income = 0  # search for the maximum "id" in number_income
        with db_session:
            query = select(c for c in Income)
            for income in query:
                if income.id > number_income:
                    number_income = income.id  # id ???????????? ?? ????
            number_income += 1
        hashMap.put('number_income', str(number_income))  # counted the number of rows in the Income
        hashMap.put('toast', '?????????????????? ?????????? ?????????????? ????????????')
        hashMap.put('ShowScreen', 'List_product')

    if hashMap.get('listener') == 'TableClick':  # tab_income_click
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_income', str(selected_line['id']))  # the number of rows in the Income
        hashMap.put('toast', '???????????????????????????? ???????????????????? ????????????')
        hashMap.put('ShowScreen', 'Input_qty')

    return hashMap

#begin product

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
    with db_session:  # new
        query = select(c for c in Product)
        for product in query:
            rows.append({'id': product.id, 'name': product.Name})  # Name})

    table['rows'] = rows
    hashMap.put('tab_product', json.dumps(table))

    return hashMap


def _listproduct_on_input(hashMap, _files=None, _data=None):

    if hashMap.get('listener') == 'TableClick':
        selected_line = json.loads(hashMap.d.get('selected_line'))
        hashMap.put('number_product', str(selected_line['id']))  # the number of rows in the Income
        hashMap.put('toast', '???????????????????????????? ??????????')
        hashMap.put('ShowScreen', 'Edit-product')

    if hashMap.get('listener') == 'btn_newproduct':
        hashMap.put('toast', '???????????????? ??????????')
        hashMap.put('ShowScreen', 'New-product')

    return hashMap


def _newproduct_on_start(hashMap, _files=None, _data=None):
    measure = hashMap.get('measure_product')
    if measure == None: # ?????????????? ?????????????????????? ???????????????? ???????????????????????? ????????????
        measure = 'kg;pcs;m;m3'
        hashMap.put('measure_products', measure)# 'kg')
        hashMap.put('measure_product', 'kg')
    else:
        measure = measure + ';kg;pcs;m;m3'# ???????????????? ???? ?????? ?? ???????????? ??????????????
        hashMap.put('measure_products', measure)


    return hashMap


def _newproduct_on_input(hashMap, _files=None, _data=None):
    measure = hashMap.get('measure_product')
    if hashMap.get('listener') == 'measure_products': #????????????!!! ?????? ???????????????????? ???????????? ?????????????? ?????????????????? ???????????????????? ???????????????? ?? ???????????? ???????????????? ?? ???????????????? ???????? ????????????
        measure = hashMap.get('measure_products')
        measures = measure + ';kg;pcs;m;m3'
        hashMap.put('measure_product', str(measure))# ????. ?????? ????????????????
        hashMap.put('measure_products', measures)#???????????? ????. ?????? ????????

    if hashMap.get('listener') == 'btn_save_newproduct':
        tags = hashMap.get('tags_product')
        tags_list = tags.split(',')
        tags_set = set(tags_list)
        with db_session:
            # p = ui_global.Record(barcode=hashMap.get('barcode'), name=hashMap.get('nom'), qty=int(hashMap.get('qty')))
            # create new Product
           # measure = hashMap.get('measure_product')
            p = Product(Name=hashMap.get('name_product'),
                        Partnumber=hashMap.get('partnumber_product'),
                        Measure = hashMap.get('measure_product'))#hashMap.get(str(measure)))#measure)  # Name=hashMap.get('name_product'),

        # create new Product Tags
            #number_product = select(p.id for p in Product).max()# search for the maximum "id" in number_Product
            # add all tags in to the table
            for tag_name in tags_set: #  iterate over the values tags_set # search tags
                query_tag = Tag.get(tag_name = tag_name)
                if query_tag == None:
                    t=Tag()
                    t.tag_name = tag_name
                    p.tags.add(t)
                else:
                    t=Tag[query_tag.id]#.products()
                    p.tags.add(t)
            commit()
            hashMap.put('ShowScreen', 'List-product')
            hashMap.put('toast', '???????????????? ??????????')

    return hashMap

# Start EDIT

def _editproduct_on_start(hashMap, _files=None, _data=None):

    selected_line = json.loads(hashMap.d.get('selected_line'))
    id_product = selected_line['id']
    with db_session:
        p = Product[id_product]
        hashMap.put('name_product', str(p.Name))
        hashMap.put('partnumber_product', str(p.Partnumber))
        hashMap.put('measure_product', str(p.Measure))
        #query = select(c for c in p.tags)
        tags =''
        for tag_name in p.tags.tag_name: #query:
            tags = str(tag_name) +','+ tags
        tags = tags[:-1]
        hashMap.put('tags_product', str(tags))

    measure = hashMap.get('measure_products')
    if measure == None: # ?????????????? ?????????????????????? ???????????????? ???????????????????????? ????????????
        measure = 'kg;pcs;m;m3'
        hashMap.put('measure_products', measure)# 'kg')
    else:
        measure = measure + ';kg;pcs;m;m3'# ???????????????? ???? ?????? ?? ???????????? ??????????????
        hashMap.put('measure_products', measure)

    return hashMap

def _editproduct_on_input(hashMap, _files=None, _data=None):
    measure = hashMap.get('measure_product')
    selected_line = json.loads(hashMap.d.get('selected_line'))
    id_product = selected_line['id']
    if hashMap.get('listener') == 'measure_products': #????????????!!! ?????? ???????????????????? ???????????? ?????????????? ?????????????????? ???????????????????? ???????????????? ?? ???????????? ???????????????? ?? ???????????????? ???????? ????????????
        measure = hashMap.get('measure_products')
        with db_session:
            p = Product[id_product]
            p.Measure = measure
            commit()
        measures = measure + ';kg;pcs;m;m3'
        hashMap.put('measure_product', str(measure))# ????. ?????? ????????????????
        hashMap.put('measure_products', measures)#???????????? ????. ?????? ????????

    if hashMap.get('listener') == 'btn_save_editproduct':
        tags = hashMap.get('tags_product')
        tags_list = tags.split(',')
        tags_set = set(tags_list)# create NEW tags_set {'tag1', 'tag2'}
        with db_session:

            # overwriting new data in Product
            p = Product[id_product]
            p.Name = hashMap.get('name_product')
            p.Partnumber = hashMap.get('partnumber_product')
            p.Measure = hashMap.get('measure_product')

            # overwriting tags in Product
            tag_old_names = select(t.tag_name for t in p.tags)[:]# create tag_old_set from Product
            tags_old_set=set()
            for tag_name in tag_old_names:
                tags_old_set.add(tag_name)

            diff_set = tags_old_set.difference(tags_set)# del not use old tag # Error -not check Entity ???Tag??? on tags without relationships with Entity ???Product???
            for tag_name in diff_set:
                del_id=Tag.get(tag_name = tag_name).id
                p.tags.remove(Tag[del_id])

            new_set = tags_set.difference(tags_old_set)#create set with new tags or new Relationships with old tags
            for tag_name in new_set: #  iterate over the values new_set # search tags
                query_tag = Tag.get(tag_name = tag_name)
                if query_tag == None:
                    t=Tag()
                    t.tag_name = tag_name
                    p.tags.add(t)
                else:
                    t=Tag[query_tag.id]#.products()
                    p.tags.add(t)
            commit()
            hashMap.put('ShowScreen', 'List-product')
            hashMap.put('toast', '???????????????????????????? ??????????')

    return hashMap


# Finish EDIT






# -END CUSTOM HANDLERS

@app.route('/set_input_direct/<method>', methods=['POST'])
def set_input(method):
    func = method
    jdata = json.loads(request.data.decode('utf-8'))
    f = globals()[func]
    hashMap.d = jdata['hashmap']
    # f()
    # f('hashmap')
    f(hashMap)  # new
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
    _init_on_start()  # new
    app.run(host='0.0.0.0', port=2075, debug=True)
