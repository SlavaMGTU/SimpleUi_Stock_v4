import json
from time import time
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
from threading import Thread
import library




def create_tables(hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cur = conn.cursor()

    '''cur.execute("DROP TABLE DocPr")
    #  cur.execute("CREATE TABLE IF NOT EXISTS DocInv (_id REAL, Date TEXT NOT NULL,Number TEXT NOT NULL,Partner TEXT NOT NULL,WhereHouse TEXT NOT NULL);")
    conn.commit()'''

    '''cur.execute("DROP TABLE Setting")
        #  cur.execute("CREATE TABLE IF NOT EXISTS DocInv (_id REAL, Date TEXT NOT NULL,Number TEXT NOT NULL,Partner TEXT NOT NULL,WhereHouse TEXT NOT NULL);")
    conn.commit()'''

    '''cur.execute("DROP TABLE DocPrTable")
    #  cur.execute("CREATE TABLE IF NOT EXISTS DocInv (_id REAL, Date TEXT NOT NULL,Number TEXT NOT NULL,Partner TEXT NOT NULL,WhereHouse TEXT NOT NULL);")
    conn.commit()'''

    cur.execute(
        "CREATE TABLE IF NOT EXISTS DocPr (id INTEGER,uid,Date TEXT,Number TEXT,Partner TEXT NOT NULL,WhereHouse TEXT,PRIMARY KEY(uid));")
    #  cur.execute("CREATE TABLE IF NOT EXISTS DocInv (_id REAL, Date TEXT NOT NULL,Number TEXT NOT NULL,WhereHouse TEXT NOT NULL);")
    conn.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS DocPrTable (id INTEGER,id_doc Text, BarCode Text , PartNo Text, Name,characteristic Text, Price Text, AQTY Text,QTY Integer,TimeStamp Text,PRIMARY KEY(id_doc,BarCode));")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Setting (id INTEGER Primary KEY, show_field TEXT,"
                "enter_QTY Text,search_db Text,enter_QPage INTEGER,DB_URL Text,DB_USER Text,DB_PASSWORD Text);")
    conn.commit()


def init_on_start(hashMap, _files=None, _data=None):
    create_tables(hashMap)
    return hashMap


def exchange_on_start(hashMap, _files=None, _data=None):
    on_start_set(hashMap)
    hashMap.put('SetTitle', 'Приемка')
    if hashMap.containsKey('tab_doc') == False:

            j = {"customcards": {
                "options": {
                    #"search_enabled": True,
                    "save_position": True
                },

                "layout": {
                    "type": "LinearLayout",
                    "orientation": "vertical",
                    "height": "match_parent",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@descr",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "-1",
                            "TextColor": "#6F9393",
                            "TextBold": False,
                            "TextItalic": True,
                            "BackgroundColor": "",
                            "width": "wrap_content",
                            "height": "wrap_content",
                            "weight": 0
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "horizontal",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "0",
                            "Elements": [


                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@Number",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "TextSize": "16",
                                    "TextColor": "#DB7093",
                                    "TextBold": True,
                                    "TextItalic": False,
                                    "BackgroundColor": "",
                                    "width": "match_parent",
                                    "height": "wrap_content",
                                    "weight": 2
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@Date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "TextSize": "16",
                                    "TextColor": "#DB7093",
                                    "TextBold": True,
                                    "TextItalic": False,
                                    "BackgroundColor": "",
                                    "width": "match_parent",
                                    "height": "wrap_content",
                                    "weight": 2
                                },
                            ]
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@Wherehouse",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "-1",
                            "TextColor": "#6F9393",
                            "TextBold": False,
                            "TextItalic": True,
                            "BackgroundColor": "",
                            "width": "wrap_content",
                            "height": "wrap_content",
                            "weight": 0
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@partner",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "-1",
                            "TextColor": "#6F9393",
                            "TextBold": False,
                            "TextItalic": True,
                            "BackgroundColor": "",
                            "width": "wrap_content",
                            "height": "wrap_content",
                            "weight": 0
                        },
                    ]
                }

            }
            }

            conn = None
            db_url = hashMap.get('DB_PATH')
            try:
                       conn = sqlite3.connect(db_url)
            except sqlite3.Error as e:
                       raise ValueError('Нет соединения с базой!')

                   # -----------------------------------
            cursor = conn.cursor()
            cursor.execute(
                       "SELECT * from DocPr")

            results = cursor.fetchall()


            j["customcards"]["cardsdata"] = []
            i=0;
            for record in results:

                c = {
                    "key": str(i),
                    "descr": "Поступление товаров",
                    "Date":  record[2],
                    "Number": record[3],
                    "partner": record[4],
                    "Wherehouse": record[5]

                }
                j["customcards"]["cardsdata"].append(c)
                i+=1;

            cursor.close()
            conn.close()

            hashMap.put("tab_doc", json.dumps(j, ensure_ascii=False).encode('utf8').decode())

    return hashMap


'''def exchange_on_start(hashMap, _files=None, _data=None):
    on_start_set(hashMap, _files, _data)
    hashMap.put('SetTitle', 'Приемка')
    if hashMap.containsKey('tab_doc') == False:

        table = {
            "type": "table",
            "textsize": "17",
            "borders": 'true',

            "columns": [

                {
                    "name": "Date",
                    "header": "Дата",
                    "weight": "0.5"
                },
                {
                    "name": "Number",
                    "header": "Номер",
                    "weight": "0.5"
                },
                {
                    "name": "WhereHouse",
                    "header": "Склад",
                    "weight": "1"
                }

            ]
        }'''





def get_changes_from_server_1(hashMap):

    db_url = hashMap.get('DB_PATH')
    url, username, password = library.url_login_pas(hashMap)

    start_time = time()
    r = requests.get(url + '/get_prihod_data', auth=HTTPBasicAuth(username, password))


    if r.status_code == 200:
        start_time = time()
        conn = sqlite3.connect(db_url)

        r.encoding = 'utf-8'
        jdata = json.loads(r.text.encode("utf-8"))
        NNmessage = jdata.get('NNmessage')
        nom = 0
        try:
            cursor1 = conn.cursor()
            # for table_name in jdata.get('SqlQuery'):
            val = jdata.get('SqlQuery')['DocReceipt']
            cursor1.executemany("INSERT OR REPLACE INTO DocPr VALUES(NULL, ?,?,?,?,?)", jdata.get('SqlQuery')['DocReceipt'])
            cursor1.executemany("INSERT OR REPLACE INTO DocPrTable VALUES(NULL,?,?,?,?,?,?,?,?,?)",
                                jdata.get('SqlQuery')['DocPrTable'])
            nom += 1
            conn.commit()
            hashMap.put('basic_notification', "[{'number':1,'title':'Simple','message':'Документы загружены'}]")
        except sqlite3.Error as err:
            hashMap.put('toast', 'nomSql ' + str(nom))
            raise ValueError(err)
        conn.close()
    else:
        hashMap.put('toast', 'Ошибка соединения с 1С '+r.text)
    r.close()
    hashMap.put('_load_active', '0')
    hashMap.remove('tab_doc')
    hashMap.put('listener', 'th_finish')
    return hashMap


# Обработчик событий загрузки/выгрузки
def exchange_on_press(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'btn_load':
       get_changes_from_server_1(hashMap)
       #th = Thread(target=get_changes_from_server_1, args=(hashMap,))
       #hashMap.put('basic_notification', "[{'number':1,'title':'Simple','message':'Начало загрузки'}]")
       #th.start()
       #th.join()


    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("break", "")

    elif hashMap.get("listener") == 'CardsClick':
        #   global doc_id

        # global doc_Nom
        key_card=hashMap.get("selected_card_key")

        jrecord = json.loads(hashMap.get("tab_doc"))
        rec=jrecord['customcards']['cardsdata'][int(key_card)]
        number = str(rec['Number'])
        date = str(rec['Date'])
        try:
            conn = sqlite3.connect(hashMap.get('DB_PATH'))
        except sqlite3.Error as e:
            raise ValueError('Нет соединения с базой!')
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cur = conn.cursor()
        cur.execute('select * from DocPr  WHERE Number=? AND Date=?', (number, date))
        result = cur.fetchall()
        uid = ''
        for res in result:
            uid = res['uid']
            break

        cur.close()
        conn.close()

        if hashMap.containsKey('tab_scan'):
            hashMap.remove('tab_scan')
        hashMap.put("Number", number)
        hashMap.put("Date", date)
        hashMap.put("doc_id", str(uid))
        hashMap.put("ShowScreen", "Сканирование Документа")
    return hashMap


def insert_data(el, hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO DocPrTable(id_doc,BarCode, PartNo, Name,characteristic, Price , AQTY,QTY,TimeStamp) VALUES(?,?,?,?,?,?,?,?,?)", el)
    conn.commit()
    cur.close()
    conn.close()
    return hashMap


def save_data(el, hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cur = conn.cursor()
    cur.execute('UPDATE DocInvTable SET QTY=?, TimeStamp=? WHERE BarCode=? AND id_doc=?',
                (str(el['QTY']),time(), str(el['BarCode']), str(hashMap.get("doc_id"))))
    conn.commit()
    cur.close()
    conn.close()
    return hashMap

def out_page(hashMap, _files=None, _data=None):
    if not hashMap.containsKey('number_page'):
        number_page = 100000000
    else:
        number_page=int(hashMap.get('number_page'))


    tab_scan=json.loads(hashMap.get('tab_scan'))
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cursor = conn.cursor()
    #  cursor.execute("SELECT * from DocInvTable")
    cursor.execute("SELECT * from DocPrTable WHERE id_doc=" + ("'" + str(hashMap.get("doc_id")) + "'"))

    rows = []
    results = cursor.fetchall()
    if len(results) > 0:
        row_onPage = int(hashMap.get('list_QPage'))
        page = int(len(results) / row_onPage)
        if number_page>page:
            number_page=page

        hashMap.put('number_page', str(page))

        for record in results[(max(number_page - 1, 0)) * row_onPage: number_page * row_onPage]:
            str_j = {"id": record[0], "BarCode": record[2], "PartNo": record[3], "Name": record[4],
                     "Price": record[6],
                     "AQTY": record[7],
                     "QTY": record[8]}

            key = []
            val = []
            for col in tab_scan['columns']:
                key.append(col['name'])
                if str_j.get(col['name']) == 'null':
                    val.append('')
                else:
                    val.append(str_j.get(col['name']))

            d = {}
            d.update(zip(key, val))
            rows.append(d)  # "doc_id": record[1],
            # rows.append(str_j)

        tab_scan['rows'] = rows

    hashMap.put('tab_scan', json.dumps(tab_scan))
    return hashMap

def get_count(hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cursor = conn.cursor()
    #  cursor.execute("SELECT * from DocInvTable")
    cursor.execute("SELECT SUM(QTY) from DocPrTable WHERE QTY>0 AND id_doc=" +"'" + str(hashMap.get("doc_id"))+"'")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(results)==0:
        return 0

    res=results[0][0]
    if res==None:
        res=0
    return res


def goods_on_start(hashMap, _files=None, _data=None):
    #hashMap.put('list_QPage', '1')

    if not hashMap.containsKey('number_page'):
        number_page = 100000000

    else:
        number_page = int(hashMap.get('number_page'))

    hashMap.put('SetTitle', hashMap.get('Number') + ' от ' + hashMap.get('Date'))
    if not hashMap.containsKey("tab_scan"):

        columns = []
        columns.append({
            "name": "BarCode",
            "header": "Штрихкод",
            "weight": "1"
        })
        # column_name=["PartNo", "name", "characteistic", "price", "ac", "fact"]
        name = ["Арт..", "Наименование", "Хар..", "Цена", "План", "Факт"]
        dx = 0

        # dict_columns={"id":"id","PartNo":"PartNo", "name":"Name", "characteristic":"characteristic","sh_code":"BarCode", "price":"Price", "ac":"0", "fact":"QTY"}
        for column in ["PartNo", "Name", "characteristic", "Price", "AQTY", "QTY"]:
            if hashMap.get('show_' + column) == "true":
                weight=1
                if column=='Name':
                    weight = 3

                columns.append({
                    "name": column,
                    "header": name[dx],
                    "weight": weight,
                    "gravity ": "right"
                })
            dx += 1

        tab_scan = {
            "type": "table",
            "textsize": "14",
            "borders": 'true',

            "columns": columns}
        conn = None
        db_url = hashMap.get('DB_PATH')
        try:
            conn = sqlite3.connect(db_url)
        except sqlite3.Error as e:
            raise ValueError('Нет соединения с базой!')
        cursor = conn.cursor()
        #  cursor.execute("SELECT * from DocInvTable")
        show_document=hashMap.get("show_document")
        if show_document=='true':
            cursor.execute("SELECT * from DocPrTable WHERE id_doc=" + ("'" + str(hashMap.get("doc_id")) + "' Order by TimeStamp DESC"))
        else:
            cursor.execute("SELECT * from DocPrTable WHERE QTY>0 AND id_doc=" + (
                        "'" + str(hashMap.get("doc_id")) + "' Order by TimeStamp DESC"))

        rows = []
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        hashMap.put('count_scan',str(get_count(hashMap)))

        if len(results) > 0:
            row_onPage=hashMap.get('enter_QPage')
            if  row_onPage=='None' or row_onPage==None:
                row_onPage=50
            else:
                row_onPage = int(row_onPage)


            page = max(int(len(results) / row_onPage),1)

            hashMap.put('all_page','...'+str(page))
            if number_page > page:
                number_page = page
            if number_page<=0:
                number_page=1

            hashMap.put('number_page', str(number_page))

            for record in results[(max(number_page - 1, 0)) * row_onPage: number_page * row_onPage]:
                str_j = {"id": record[0], "BarCode": record[2], "PartNo": record[3], "Name": record[4],
                         "characteristic": record[5],
                         "Price": record[6],
                         "AQTY": record[7],
                         "QTY": record[8]}

                key = []
                val = []
                for col in tab_scan['columns']:
                    key.append(col['name'])
                    if str_j.get(col['name']) == 'null':
                        val.append('')
                    else:
                        val.append(str_j.get(col['name']))

                d = {}
                d.update(zip(key, val))
                rows.append(d)  # "doc_id": record[1],
                # rows.append(str_j)

            tab_scan['rows'] = rows
        else:
            hashMap.put('all_page', '...' + str(1))
            hashMap.put('number_page', str(1))
        hashMap.put('tab_scan', json.dumps(tab_scan))

    return hashMap

def show_dialog_not_find(hashMap):
    hashMap.put("this_no_prod", "1")
    hashMap.put('beep', '')
    hashMap.put("ShowDialog", "Товар не найден")
    hashMap.put("ShowDialogStyle",
                json.dumps({"title": "Товар не найден "
                                     , "yes": "ОК", "no": ""}))

    #hashMap.put('beep_volume', '100')


    return hashMap



def check_product(hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cursor = conn.cursor()
    cursor.execute("SELECT * from DocPrTable WHERE BarCode="+"'"+str(hashMap.get("barcode_input"))+"'"+" AND id_doc="+
                    "'" + str(hashMap.get("doc_id")) + "'")

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(results) == 0:
            if hashMap.get('search_db') == 'true':
                res = search_db(hashMap, str(hashMap.get("barcode_input")))
                if len(res) == 0:
                    show_dialog_not_find(hashMap)
                    return hashMap, results, False

                res = res[0]

                results = [(res[0], hashMap.get("doc_id"), res[2],
                            res[3], res[4], res[5], res[6],'0', 0, '')]
                res_w = (hashMap.get("doc_id"), res[2],
                         res[3], res[4], res[5], res[6], res[7], 0, '')

                insert_data(res_w, hashMap)
            else:
                show_dialog_not_find(hashMap)

                return hashMap, results, False




    return hashMap, results, True


def add_element_in_table(hashMap, hand=False):
    tab_scan = json.loads(hashMap.get("tab_scan"))

    _, results, prod_find = check_product(hashMap)
    if not prod_find:
        return hashMap

    if 'rows' in tab_scan:
        rows = tab_scan['rows']
        row_onPage = hashMap.get('enter_QPage')
        if row_onPage == 'None':
            row_onPage = 50
        else:
            row_onPage = int(row_onPage)

        if len(rows) > row_onPage:
            hashMap.put('number_page', str(int(hashMap.get('number_page'))+1))
            rows = []
    else:
        rows = []

    enter_qty = int(hashMap.get('e_qty'))
    for el in rows:
        if el['BarCode'] == hashMap.get("barcode_input"):
            qty = int(el['QTY']) + enter_qty
            #hashMap.put('toast', "rows"+'  '+str(results))
            el['QTY'] = str(qty)
            tab_scan['rows'] = rows
            hashMap.put('tab_scan', json.dumps(tab_scan))
            save_data(el, hashMap)
            return hashMap

    # dict_columns={"id":"id","PartNo":"PartNo", "name":"Name", "characteristic":"characteristic","BarCode":"BarCode", "price":"Price", "ac":"0", "QTY":"QTY"}
    tab_scan['rows'] = rows

    for record in results:
        str_j = {"id": record[0], "BarCode": record[2], "PartNo": record[3], "Name": record[4], "Price": record[6],
                 "characteristic": record[5],
                 'AQTY': record[7],
                 "QTY": str(int(record[8]) + enter_qty), 'TimeStamp': ''}

        key = []
        val = []
        for col in tab_scan['columns']:
            key.append(col['name'])
            val.append(str_j.get(col['name']))

        d = {}
        d.update(zip(key, val))
        rows.append(d)  # "doc_id": record[1],
        # rows.append(str_j)
        save_data(str_j, hashMap)
    # tab_scan['rows'] = rows
    #hashMap.put('toast', "results" + '  ' + str(results))
    hashMap.put('tab_scan', json.dumps(tab_scan))
    return hashMap


def goods_input(hashMap, _files=None, _data=None):
    if hashMap.containsKey("enter_QTY") == False:
        on_start_set(hashMap)
        #goods_on_start(hashMap)

    '''if hashMap.get("event") == "onResultPositive":
        add_element_in_table(hashMap, True)
        hashMap.remove("event")'''

    if hashMap.get("listener") == "btn_back":
       hashMap.put('number_page',str(int(hashMap.get('number_page'))-1))
       hashMap.remove('tab_scan')

    elif hashMap.get("listener") == "btn_forward":
        hashMap.put('number_page', str(int(hashMap.get('number_page')) + 1))
        hashMap.remove('tab_scan')

    elif hashMap.get("listener") == "btn_send":
        hashMap.put("ShowDialog", "Пересчет окончен")
        hashMap.put("ShowDialogStyle",
                    json.dumps({"title": "Пересчет окончен?", "yes": "Да", "no": "Нет"}))

    elif hashMap.get("event") == "onResultPositive" :
        if hashMap.get("this_no_prod")=='1':
            hashMap.remove("event")
            hashMap.remove("this_no_prod")
        else:
            hashMap.remove("event")
            th = Thread(target=send_movement_on_server, args=(hashMap,))
            th.start()
            th.join()
            hashMap.put('ShowScreen', 'Новый экран')
        #send_movement_on_server(hashMap, _files, _data)

    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("ShowScreen", "Новый экран")

    elif hashMap.get("listener") == "barcode":
        # hashMap.put('en_barcode',str(hashMap.get("barcode_input")))

        if hashMap.get(
                "enter_QTY") == 'Ручной ввод "Окно"':
            _, results, prod_find = check_product(hashMap)
            if prod_find:
                hashMap.put("ShowScreen", "Ввод количества")


        else:
            hashMap.put('e_qty', "1")
            th = Thread(target=add_element_in_table, args=(hashMap,))
            th.start()
            th.join()
            hashMap.put('count_scan', str(get_count(hashMap)))
            #add_element_in_table(hashMap)

    elif hashMap.get("listener") == "TableClick":
        jrecord = json.loads(hashMap.get("selected_line"))
        hashMap.put('barcode_input', str(jrecord['BarCode']))
        hashMap.remove('listener')

        # hashMap.put('e_qty', "")
        if hashMap.get(
                "enter_QTY") == 'Ручной ввод в списке':
            hashMap.put("ShowScreen", "Ввод количества")
            #goods_on_start(hashMap)

    #  hashMap.put('enterQty','10')
    return hashMap


def search_db(hashMap, barcode):
    status_r = False

    url, username, password = url_login_pas(hashMap)
    r = requests.get(url + '/get_el_barcode',
                     auth=requests.auth.HTTPBasicAuth(username, password), data=json.dumps({'barcode': barcode,'id_doc':hashMap.get('doc_id')}))
    # r = requests.get(url + '/get_el_barcode', auth=HTTPBasicAuth(username, password),data=json.dumps({'barcode':barcode}))
    val = []
    r.close()
    if r.status_code == 200:
        r.encoding = 'utf-8'
        jdata = json.loads(r.text.encode("utf-8"))
        NNmessage = jdata.get('NNmessage')
        val = jdata.get('SqlQueryBarcode')
        #hashMap.put("toast", str(val))
    else:
        hashMap.put("toast", r.text)
    return val

def check_plan_fact(hashMap):
    hashMap.put("this_plan", "1")
    hashMap.put("ShowDialog", "")
    hashMap.put("ShowDialogStyle",
                    json.dumps({"title": "Превышено плановое значение "
                                   , "yes": "ОК", "no": ""}))
    return hashMap


def Q_on_start(hashMap, _files=None, _data=None):
    hashMap.put('SetTitle', hashMap.get('Number') + ' от ' + hashMap.get('Date'))
    if hashMap.containsKey("QQTY") == False:

        hashMap.put('hand_enter','0')

        db_url = hashMap.get('DB_PATH')
        try:
            conn = sqlite3.connect(db_url)
        except sqlite3.Error as e:
            raise ValueError('Нет соединения с базой!')
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * from DocInvTable WHERE BarCode=" + "'"+str(hashMap.get("barcode_input"))+"'" + ' And id_doc=' + "'" + str(
                hashMap.get("doc_id")) + "'")


        results = cursor.fetchall()
        cursor.close()
        conn.close()

        limit=False
        aqty=0
        qqty=0

        for key in ["PartNo", "Name", "characteristic", "Price", "AQTY"]:
            hashMap.put('Q' + key, '')

            if len(results) > 0:
                for key, val in results[0].items():
                        if hashMap.get('show_' + key) == 'true':
                            if key == 'QTY':
                                hashMap.put('SetQTY', str(val))
                                hashMap.put('Q_QTY', 'Станет ' + str(int(val) + 1) + ' шт')
                                hashMap.put('eqty', '1')
                                qqty = val
                                val = 'Было ' + str(val) + 'шт'


                            elif key == 'AQTY':
                                aqty = val
                                val = str(val) + ' (шт)'

                            elif key == 'Price':
                                val = "Цена: "+str(val) + ' р'

                            hashMap.put('Q' + key, val)
                        else:
                            hashMap.put('Q' + key, '')
            else:
                hashMap.put('eqty', '0')
                show_dialog_not_find(hashMap)
                return hashMap

        if(int(aqty)<(int(qqty)+1)):
            check_plan_fact(hashMap)
    return hashMap


def Q_on_input(hashMap, _files=None, _data=None):
    qty = hashMap.get('SetQTY')
    e_qty = hashMap.get('eqty')
    if e_qty == 'null' or e_qty == '':
        e_qty = 0

    if qty == 'null':
        qty = 0
    e_qty = int(e_qty)
    qty = int(qty)

    if hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.remove("QQTY")
        hashMap.remove("tab_scan")
        hashMap.put('ShowScreen', 'Сканирование Документа')

    elif hashMap.get('listener') == 'btn_minus':
        e_qty = max(int(e_qty) - 1, 0)
        hashMap.put('eqty', str(e_qty))
        hashMap.put('hand_enter', '1')
    elif hashMap.get('listener') == 'btn_plus':
        e_qty = e_qty + 1
        hashMap.put('eqty', str(e_qty))
        hashMap.put('hand_enter', '1')
    elif hashMap.get('listener') == 'barcode':
       # if hashMap.get('QBarcode') == hashMap.get('barcode_input'):
        if hashMap.get('hand_enter')=='1':
           hashMap.put('listener_hand_dialog', 'hand_enter_dialog')
           hashMap.put("alert","Количество изменено вручную, для дальнейшей работы необходимо сохранить результат")
           hashMap.put('ShowDialog','Предупреждение')
           hashMap.put("ShowDialogStyle",
                       json.dumps({"title": "Внимание!!!", "yes": "Сохранить", "no": "Отмена"}))
        else:

            save_data({'QTY': (qty + 1),
                      'BarCode': hashMap.get('QBarCode')}, hashMap)
            hashMap.remove("QQTY")
            hashMap.remove("eqty")
            hashMap.put('ShowScreen', 'Ввод количества')
           # hashMap.remove("QQTY")
            #hashMap.remove("tab_scan")
            #hashMap.put('listener','barcode')
            #hashMap.put('ShowScreen', 'Сканирование Документа')
            #      e_qty += 1;
            #     hashMap.put('eqty', str(e_qty))
            #  else:
            return hashMap

    elif hashMap.get('listener') == 'Btn_save':
        save_data({'QTY': (e_qty + qty),
                   'BarCode': hashMap.get('barcode_input')}, hashMap)
        hashMap.remove("QQTY")
        hashMap.remove("eqty")
        hashMap.remove("tab_scan")
        hashMap.put('ShowScreen', 'Сканирование Документа')


    elif hashMap.get('listener') == 'Btn_cancel':
        # hashMap.put('break', '')
        hashMap.remove("QQTY")
        hashMap.remove("tab_scan")
        hashMap.put('ShowScreen', 'Сканирование Документа')

    elif hashMap.get("event") == "onResultPositive":
        if hashMap.get("listener_hand_dialog")=='hand_enter_dialog':

           save_data({'QTY': (e_qty + qty),
                       'BarCode': hashMap.get('barcode_input')}, hashMap)
           hashMap.remove("listener_hand_dialog")
        # hashMap.put('break', '')
        if hashMap.get("this_plan")=="1":
            hashMap.remove("event")
            hashMap.remove("this_plan")
            return hashMap

        hashMap.remove("event")
        hashMap.remove("QQTY")
        hashMap.remove("eqty")
        #hashMap.remove("listener")
        hashMap.remove("tab_scan")
        hashMap.put('ShowScreen', 'Сканирование Документа')


    hashMap.put('Q_QTY', 'Станет ' + str(e_qty + qty) + ' шт')

    return hashMap


def send_movement_on_server(hashMap, _files=None, _data=None):
    if hashMap.containsKey('_Upload_active'):
        if hashMap.get('_Upload_active') == '1':
            return hashMap

    result, status_code = library.test_connection(hashMap)
    if not result:
        hashMap.put('toast', 'нет соединения ' + str(status_code))
        return hashMap

    hashMap.put('basic_notification', "[{'number':1,'title':'Simple','message':'выгрузка документа'}]")
    hashMap.put('_Upload_active', '1')
    conn = sqlite3.connect(
        hashMap.get('DB_PATH'))  # sqlite3.connect('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS')#

    # android_id = hashMap.get('CLIENT_CODE')  # hashMap.get('OID_ID')  # '43'  # ''OID_ID")

    url, username, password = library.url_login_pas(hashMap)

    try:
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cursor1 = conn.cursor()

        cursor1.execute(
            "SELECT id_doc,BarCode,Price,QTY from DocPrTable WHERE id_doc =" + "'" + str(hashMap.get("doc_id")) + "'")


    except sqlite3.Error as err:
        raise ValueError(err)
    a = cursor1.fetchall()
    #  hashMap.put('toast', str(a[0]))
    Tex1 = json.dumps(a, ensure_ascii=False)
    #  hashMap.put('toast', str(Tex1))
    r = requests.post(url + '/load_pr', auth=HTTPBasicAuth(username, password), data=Tex1.encode('utf-8'))  #

    if r.status_code == 200:

        cursor1.executescript(
            "Delete  from DocPrTable WHERE id_doc =" + "'" + str(hashMap.get("doc_id")) + "';" +
            "Delete  from DocPr WHERE uid =" + "'" + str(hashMap.get("doc_id")) + "';")
        conn.commit()

        hashMap.put('basic_notification', "[{'number':1,'title':'Simple','message':'документ выгружен'}]")
        cursor1.close()
        conn.close()
        hashMap.put('_Upload_active', '0')
        hashMap.remove('tab_doc')

        return hashMap


    else:
        hashMap.put('toast', str(r.text))
        cursor1.close()
        conn.close()

    hashMap.put('_Upload_active', '0')
    return hashMap


# ----------------------------------------------------------------
def on_start_set(hashMap, _files=None, _data=None):
    if hashMap.containsKey('show_PartNo') == False:
        enter_QTY = 'Только сканирование;' \
                    'Ручной ввод "Окно";' \
                    'Ручной ввод в списке'
        hashMap.put("list_QTY", enter_QTY)
    set = Setting()
    set.on_start_set(hashMap)
    return hashMap


def save_satting(hashMap, _files=None, _data=None):
    set=Setting()
    set.save_setting(hashMap)
    return hashMap


def on_input_set(hashMap, _files=None, _data=None):
    set = Setting()
    set.on_input_set(hashMap)

    return hashMap

def url_login_pas(hashMap):
    username = hashMap.get('DB_USER')
    password = hashMap.get('DB_PASSWORD')
    url =hashMap.get('DB_URL') #'http://192.168.90.48:8080/roznWeb/hs/simplewms'  #
    return url, username, password

def test_connection(hashMap):
    url, username, password = url_login_pas(hashMap)
    try:
        r = requests.get(url + '/test_connect', auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True , r.status_code
        else:
            return False , r.status_code

    except Exception as e:
        hashMap.put("toast",str(e))

    return False, "408"

class Setting:
    column_list = ["show_PartNo", "show_Name", "show_characteristic", "show_Price", "show_AQTY", "show_QTY",
                        "show_BarCode", "show_document",
                        "enter_QTY", "search_db", "enter_QPage", "DB_URL",
                        "DB_USER", "DB_PASSWORD"]
    show_field = "show_field"
    column_list_db = ["enter_QTY", "search_db", "enter_QPage", "DB_URL",
                      "DB_USER", "DB_PASSWORD"]
    check_list = ["show_PartNo", "show_Name", "show_characteristic", "show_Price", "show_AQTY", "show_QTY",
                  "show_BarCode","show_document"]


    def save_setting(self,hashMap):

        ##--------------------------------------------------------
        val_list = []
        for col in self.check_list:
            val_list.append(hashMap.get(col))
        if val_list.count('true') < 2:
            hashMap.put("toast", "Минимальные настройки отображения Артикул, количество факт")
            hashMap.put('show_PartNo', 'true')

        ##--------------------------------------------------------

        hashMap.put('show_BarCode', 'true')
        hashMap.put('show_QTY', 'true')

        val_ = []
        for column in self.check_list:
            val_.append({column: hashMap.get(column)})

        val=[]
        val.append(str(json.dumps(val_)))

        for column in self.column_list_db:
              val.append(hashMap.get(column))


        conn = None
        db_url = hashMap.get('DB_PATH')
        try:
            conn = sqlite3.connect(db_url)
        except sqlite3.Error as e:
            raise ValueError('Нет соединения с базой!')
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO Setting VALUES(1, ?,?,?,?,?,?,?)", val)
        conn.commit()
        cursor.close()
        conn.close()
        hashMap.put("toast", "Настройки сохранены")
        return hashMap

    def on_start_set(self,hashMap, _files=None, _data=None):
        if hashMap.containsKey('show_PartNo') == False:
            #enter_QTY ='Только сканирование;' \
            #            'Ручной ввод "Окно";' \
            #            'Ручной ввод в списке'


            hashMap.put("list_QPage", '50;100;200')
            hashMap.put('show_BarCode', 'true')
            hashMap.put('show_QTY', 'true')

            conn = None
            db_url = hashMap.get('DB_PATH')
            try:
                conn = sqlite3.connect(db_url)
                conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
            except sqlite3.Error as e:
                raise ValueError('Нет соединения с базой!')

            # -----------------------------------
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from Setting Where id=1")

            results = cursor.fetchall()
            if len(results) != 0:
                for el in results[0]:
                    if el == 'id':
                        continue
                    elif el==self.show_field:
                        for item in json.loads(results[0][el]):
                           for key, val in item.items():
                               hashMap.put(key, str(val))
                    else:
                        hashMap.put(el, str(results[0][el]))

            cursor.close()
            conn.close()
            val_list = []
            for col in ["show_BarCode", "show_PartNo", "show_Name", "show_characteristic", "show_Price", "show_AQTY",
                        "show_QTY"]:
                val_list.append(hashMap.get(col))
            if val_list.count('true') < 2:
                # hashMap.put("toast", "Минимальные настройки отображения Артикул, количество факт")
                hashMap.put('show_PartNo', 'true')
                hashMap.put('show_QTY', 'true')

            if hashMap.containsKey('DB_URL') == False:
                hashMap.put('DB_URL', '')
            if hashMap.containsKey('DB_USER') == False:
                hashMap.put('DB_USER', '')
            if hashMap.containsKey('DB_PASSWORD') == False:
                hashMap.put('DB_PASSWORD', '')

        return hashMap

    def on_input_set(self,hashMap, _files=None, _data=None):
        if hashMap.get('listener') == 'btn_resset':
            #delete_tab_bd(hashMap)
            return hashMap
        elif hashMap.get('listener') == 'btn_check':
            result, r = test_connection(hashMap)
            if result:

                hashMap.put('toast','подключено успешно')
            else:
                hashMap.put('toast', 'нет соединения '+ str(r))


        elif hashMap.get('listener') == 'btn_save':
            hashMap.put('ShowDialog', "")
            hashMap.put("ShowDialog", "Сохранение настроек")
            hashMap.put("ShowDialogStyle",
                        json.dumps({"title": "Сохранить настройки?", "yes": "Подтвердить", "no": "Отмена"}))

        if hashMap.get("event") == "onResultPositive":
            self.save_setting(hashMap)
            hashMap.remove("event")
            hashMap.put("break", "")
        return hashMap

    '''def save_setting(hashMap):
        column_list = ["show_PartNo", "show_Name", "show_characteristic", "show_Price", "show_AQTY", "show_QTY",
                       "show_BarCode",
                       "enter_QTY", "search_db", "enter_QPage", "DB_URL",
                       "DB_USER", "DB_PASSWORD"]
        ##--------------------------------------------------------
        val_list = []
        for col in ["show_PartNo", "show_Name", "show_characteristic", "show_Price", "show_AQTY", "show_QTY",
                    "show_BarCode"]:
            val_list.append(hashMap.get(col))
        if val_list.count('true') < 2:
            hashMap.put("toast", "Минимальные настройки отображения Артикул, количество факт")
            hashMap.put('show_PartNo', 'true')

        ##--------------------------------------------------------

        hashMap.put('show_BarCode', 'true')
        hashMap.put('show_QTY', 'true')

        val = []
        for column in column_list:
            a = hashMap.get(column)
            if a == None:
                a = "false"
            elif column == 'enterQTY':
                print(hashMap.get(column))
            val.append(hashMap.get(column))

        conn = None
        db_url = hashMap.get('DB_PATH')
        try:
            conn = sqlite3.connect(db_url)
        except sqlite3.Error as e:
            raise ValueError('Нет соединения с базой!')
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO Setting VALUES(1, ?,?,?,?,?,?,?)", val)
        conn.commit()
        cursor.close()
        conn.close()
        hashMap.put("toast", "Настройки сохранены")
        return hashMap'''





'''def delete_tab_bd(hashMap):
    conn = None
    db_url = hashMap.get('DB_PATH')
    try:
        conn = sqlite3.connect(db_url)
    except sqlite3.Error as e:
        raise ValueError('Нет соединения с базой!')
    cur = conn.cursor()
    cur.execute("DROP TABLE DocInv")
    conn.commit()
    cur.execute("DROP TABLE DocInvTable")
    conn.commit()

    cur.execute("DROP TABLE Setting")
    conn.commit()
    cur.close()
    conn.close()
    hashMap.put('break', '')
    return hashMap'''

