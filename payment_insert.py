import mysql.connector
import pandas as pd
import random

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")
banks = ["ICICI", "HDFC", "HSBC", "SBI", "UBI", "PNB"]

command = "select order_id, user_id from orders where order_id > 3101 order by order_id;" #iterate each time by the number of delivery agents you can assign (add more delivery agents to speed up the process and jump by more number)
c.execute(command)
data = c.fetchall()

for j in range(len(data)):
    payment_id = random.randint(10000000, 99999999)
    card_no = []
    for i in range(16):
        card_no.append(str(random.randint(1, 9)))

    card_no = '\'' + "".join(card_no) + '\''
    bank = '\'' + random.choice(banks) + '\''
    order_id = data[j][0]
    user_id = '\'' + data[j][1] + '\''

    command = "insert into payment_info values(" + str(payment_id) + ',' + str(order_id)  + ',' + str(bank)  + ',' + str(user_id)  + ',' + str(card_no) + ');'
    c.execute(command)
    # print(command)

mydb.commit()


