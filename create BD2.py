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

#new



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



# -BEGIN CUSTOM HANDLERS

db.generate_mapping(create_tables=True)

with db_session:
      # for number in range(10):
      #     i = Income(qty_income=10-number)#qty_income=0, products=p
      #     l= List_income(incomes=i)
      #     p = Product(incomes=i, Partnumber='Partnumber' + str(number), Measure='Measure1', Name='Name1')  # Name=hashMap.get('name_product'),
      #
      # #List_income[number].incomes.add(i)

    # for number in range(1, 3):
    #     cons1 = Const()
    #     cons1.number =1 # get number from List_income
    # commit()
    # a = select(s for s in List_income).count()#
    # for number in range(1, 3):
    #     List_income[number].delete()


