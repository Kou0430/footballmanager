from cs50 import SQL

db = SQL("sqlite:///playersData.db")

squad = db.execute("SELECT * FROM players LIMIT 5")
print(squad)
for i in range(len(squad)):
    if i == 0:
        if "CM" in squad[i]["position"]:
            print("CM")
        elif "CAM" in squad[i]["position"]:
            print("CAM")