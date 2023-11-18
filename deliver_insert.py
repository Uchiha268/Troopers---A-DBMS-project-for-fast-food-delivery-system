import mysql.connector
import pandas as pd
import random

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")

command = "select user_id from user where permissions = 'delivery_agent' and user_id not in (select user_id from delivery_agent);"
c.execute(command)
data = c.fetchall()
agent_id = 1042

for i in range(len(data)):
    user_id = "\'" + data[i][0] + "\'"
    available = 1
    command = "insert into delivery_agent values(" + str(agent_id) + "," + str(user_id) + "," + str(available) + ");"
    agent_id += 1
    c.execute(command)

mydb.commit()


