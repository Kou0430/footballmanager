import sqlite3

conn = sqlite3.connect('playersData.db')
cur = conn.cursor()

cur.execute("SELECT * FROM players WHERE oa = 91")
result = cur.fetchall()
print(result[0][2])
print(len(result))

cur.execute("SELECT COUNT(*) FROM players")
count = cur.fetchall()
print(count[0][0], type(count[0][0]))

conn.close()
