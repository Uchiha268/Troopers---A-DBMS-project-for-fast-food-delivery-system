import pandas as pd 
import random

names = pd.read_csv("../../Graph Theory/names.csv")

users = names["name"].tolist()[0:30]
email = []
number = []
mobile = []
password = []
permission = []
address = ["House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082","House #2 PushpamVihar, 560078", "House #17 PushpamVihar, 560078", "B building #793, Altamond Heights, 560082"]
for names in users:
	email.append(names.replace(" ", "").lower() + "@gmail.com")

for i in range(30):
	ph_no = []
	for j in range(0, 10):
		ph_no.append(str(random.randint(0, 9)))

	mobile.append("".join(ph_no))

for i in range(30):
	cur_password = []
	pass_length = random.randint(8, 32)
	for j in range(pass_length):
		cur_password.append(chr(random.randint(0, 25) + ord('a')))

	password.append("".join(cur_password))

for i in range(28):
	permission.append("end_user")

for i in range(2):
	permission.append("administrator")

df = pd.DataFrame(list(zip(users, mobile, email, address, password, permission)))
df.to_csv("./user.csv")




