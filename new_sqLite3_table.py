import sqlite3

#con = sqlite3.connect(r'./db/db.db')
con = sqlite3.connect(r'D:\work\python\22-08-15_SimpleUI_test\07-Simple_start\db\db.db')


print ("Opened database successfully")
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS db(barcode TEXT,'
                                          'name TEXT,'
                                          'qty INT)')
con.commit()
print ("Table created successfully")
cur.close()
con.close()
