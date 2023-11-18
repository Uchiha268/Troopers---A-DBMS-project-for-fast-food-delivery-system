import mysql.connector
import pandas as pd
import random

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")

command = "select user_id from user where user_id not in (select user_id from orders) and permissions <> 'deliver_agent';"
c.execute(command)
data = c.fetchall()
order_id = 208
total_amount = 0


for i in range(3000):
    user_id = random.choice(data)
    data.remove(user_id)
    user_id = '\'' + user_id[0] + '\''
    franchise_id = random.randint(1, 10)
    offer_id = random.randint(0,3)
    discount = 0
    date = '\'' + str(random.randint(1,30)) + '/' + str(random.randint(1, 12)) + '/' + '2011' + '\''
    final_price = 0

    command = "insert into orders values(" + str(order_id) + ',' + str(total_amount) + ',' + user_id + ',' + str(franchise_id) + ',' + str(offer_id) + ',' + str(discount) + ',' + str(final_price) + ',' + str(date) + ');'
    c.execute(command)
    order_id += 1
    # print(command)
    
mydb.commit()
