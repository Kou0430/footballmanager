import sqlite3

conn = sqlite3.connect('C:/Users/hcr_t/PycharmProjects/pythonProject/finalproject/footballmanager/users.db')
cur = conn.cursor()

cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username STRING, \
             hash STRING)")

conn.commit()
conn.close()