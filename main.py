import re
import sqlite3

conn = sqlite3.connect('/playersData.db')
cur = conn.cursor()

cur.execute("CREATE TABLE players(id INTEGER PRIMARY KEY AUTOINCREMENT, image STRING, name STRING, \
             position STRING, age INT, oa INT, pt INT, club STRING, price FLOAT, salary FLOAT)")


for i in range(20):
    path = "datafile/player{number}.txt".format(number=str(i+1))
    with open(path, encoding="utf-8", mode="r") as f:
        li = f.readlines()

        for row in range(60):

            imageRow = li[1122 + row * 11]  # 画像URLがある行を抽出
            statusRow = li[1124 + row * 11]  # 各ステータスがある行を抽出
            clubRow = li[1128 + row * 11]  # クラブ名がある行を抽出
            moneyRow = li[1131 + row * 11]  # 市場価値と給料がある行を抽出

            image = re.search(r'data-src="(.+)" data-srcset', imageRow).group(1)
            name = re.search(r'<div class="ellipsis">(.+)</div></a>', statusRow).group(1)

            position = re.search(r'pos pos[0-9]+">(.+)</span></a></td>', statusRow).group(1)
            while True:
                if len(position) > 20:  # ポジションが二つ以上の場合に抽出
                    first = re.search(r'^(.+)</span></a> <a rel="', position).group(1)
                    second = re.search(r'class="pos pos[0-9]+">(.+)$', position).group(1)

                    if len(first) > 20:  # ポジションが三つの時はさらに処理
                        reFirst = re.search(r'^(.+)</span></a> <a rel="', first).group(1)
                        reSecond = re.search(r'class="pos pos[0-9]+">(.+)$', first).group(1)
                        third = re.search(r'class="pos pos[0-9]+">(.+)$', second).group(1)
                        position = reFirst + ', ' + reSecond + ', ' + third
                        # print(reFirst, reSecond, third)
                        break
                    position = first + ', ' + second
                    # print(first, second)
                    break

                break

            age = re.search(r'data-col="ae">(.+)</td><td class="col col-oa col-sort"', statusRow).group(1)
            oa = re.search(r'"oa"><span class="bp3-tag p p-(.+)">[0-9]+</span></td><td class="col col-pt', statusRow).group(1)
            pt = re.search(r'"pt"><span class="bp3-tag p p-(.+)">[0-9]+</span>', statusRow).group(1)
            club = re.search(r'">(.+)</a><div', clubRow).group(1)
            price = re.search(r'"vl">€(.+)</td><td class="col col-wg', moneyRow).group(1)
            salary = re.search(r'"wg">€(.+)</td><td class="col col-tt', moneyRow).group(1)

            #print(image)
            #print(name)
            #print(position)
            #print(age)
            #print(oa)
            #print(pt)
            #print(club)
            #print(price)
            #print(salary)

            age = int(age)
            oa = int(oa)
            pt = int(pt)
            if 'K' in price:
                price = float(price.replace('K', '')) / 1000
            else:
                price = float(price.replace('M', ''))

            salary = float(salary.replace('K', ''))

            playerData = (image, name, position, age, oa, pt, club, price, salary)

            #print(playerData)

            cur.execute("INSERT INTO players(image, name, position, age, oa, pt, club, price, salary) \
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", playerData)

            conn.commit()

cur.execute("SELECT * FROM players")
for row in cur:
    print(row)

conn.close()