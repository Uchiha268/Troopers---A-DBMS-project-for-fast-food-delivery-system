import mysql.connector
import pandas as pd
import random

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")

command = "select user_id from orders where user_id not in (select user_id from user_and_offer);"
c.execute(command)
data = c.fetchall()

for i in range(len(data)):
    user_id = '\'' + data[i][0] + '\''
    offer_id = 0
    command = "insert into user_and_offer values(" + str(user_id) + ',' + str(offer_id) + ');'
    c.execute(command)

command = "select user_id, offer_id from orders where offer_id <> 0;"
c.execute(command)
data = c.fetchall()

for i in range(len(data)):
    user_id = '\'' + data[i][0] + '\''
    offer_id = data[i][1]
    command = "insert into user_and_offer values(" + str(user_id) + ',' + str(offer_id) + ');'
    c.execute(command)

mydb.commit()