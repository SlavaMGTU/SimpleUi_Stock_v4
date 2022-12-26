from pony import orm
from pony.orm import Database,Required,Set,Json,PrimaryKey,Optional
from pony.orm.core import db_session
import datetime
import sqlite3
from typing import Optional


# Constants and variables
DB_PATH ='//data/data/ru.travelfood.simple_ui/databases/SimpleWMS' # 'db.db'#'db\\db.db'
#DB_PATH = 'sqlite_dev.db'
db = Database()
db.bind(provider='sqlite', filename=DB_PATH, create_db=True)


class Record(db.Entity):
    barcode = Required(str)
    name = Required(str)
    qty = Required(int)

def init():
    db.generate_mapping(create_tables=True)

def setup_db(hash_map: Optional['hashMap'] = None,
             db_path: str = DB_PATH,
             database: Database = db
             ) -> None:
    '''
    Creates the database with required tables
    '''

    if hash_map:
        db_path = hash_map.get('DB_PATH')

    db.bind(provider='sqlite', filename=db_path, create_db=True)
    db.generate_mapping(create_tables=True)
#
#
# def add_table_entries(data: dict) -> None:
#     '''
#     Fills the database tables with some data
#     '''
#
#     for table, records in data.items():
#
#         for record_data in records:
#             obj = table.get(name=record_data.get('name'))
#
#             if obj:
#                 obj.set(**record_data)
#             else:
#                 table(**record_data)

