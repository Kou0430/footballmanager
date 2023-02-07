from cs50 import SQL

li = [""] * 11
print(li)

for i in range(11):
    li[i] = "{i}".format(i=i)

print(li)
