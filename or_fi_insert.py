import mysql.connector
import pandas as pd
import random

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")

command = "select order_id, franchise_id, food_id from order_and_food_item where order_id > 207 order by order_id"
c.execute(command)
data = c.fetchall()
franchise_limit = [5, 5, 5, 3, 4, 4, 5, 2, 3, 3]

# for i in range(len(data)):
#     order_id = data[i][0]
#     franchise_id = data[i][1]
#     food_id = random.randint(1, franchise_limit[franchise_id - 1])
#     quantity = random.randint(1,5)
#     total_price = 0
#     command = "insert into order_and_food_item values(" + str(order_id) + ',' + str(food_id) + ',' + str(franchise_id) + ',' + str(quantity) + ',' + str(total_price) + ');'
#     c.execute(command)

for i in range(1000):
    choice = random.choice(data)
    order_id = choice[0]
    franchise_id = choice[1]
    cur_food_id = choice[2]
    food_id = random.randint(1, franchise_limit[franchise_id - 1])
    while(food_id == cur_food_id):
        food_id = random.randint(1, franchise_limit[franchise_id - 1])
    quantity = random.randint(1, 5)
    total_price = 0
    command = "insert into order_and_food_item values(" + str(order_id) + ',' + str(food_id) + ',' + str(franchise_id) + ',' + str(quantity) + ',' + str(total_price) + ');'
    try:
        c.execute(command)
    except:
        continue
mydb.commit()

