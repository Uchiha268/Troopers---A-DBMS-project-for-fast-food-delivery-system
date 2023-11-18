import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost", user="root", password="")
c = mydb.cursor()
c.execute("USE fast_food")

def create_table(table, columns, datatypes):
	command = 'create table if not exists ' + table + ' ('
	for i in range(len(columns)):
		command += columns[i] + ' ' + datatypes[i] + ','

	command = command[:-1]
	command += ');'
	c.execute(command)


def add_data(table, values):
	command = 'insert into ' + table + ' values('
	for i in range(len(values)):
		command += values[i] + ','

	command = command[:-1]
	command += ');'
	try:
		c.execute(command)
		mydb.commit()
		return ''
	except mysql.connector.Error as err:
		return err.msg
	

def view_table(table, columns):
	command = 'select distinct '
	if len(columns) != 0:
		for i in range(len(columns)):
			command += columns[i] + ','
	else:
		command += '* '
	command = command[:-1]
	command += ' from ' + table + ' ;'

	c.execute(command)
	data = c.fetchall()
	return data

def edit_details(table, columns, values, keys, keys_values):
	command = 'update ' + table + ' set '
	for i in range(len(columns)):
		command += columns[i] + '=' + values[i] + ','

	command = command[:-1]
	command += " where "
	for i in range(len(keys)):
		command += keys[i] + '=' + keys_values[i] + ' and '

	command = command[:-4]
	command += ';'
	try:
		c.execute(command)
		mydb.commit()
		return ''
	except mysql.connector.Error as err:
		return err.msg
	

def delete_data(table, keys, keys_values):
	command = 'delete from ' + table + ' where '
	for i in range(len(keys)):
		command += keys[i] + '=' + keys_values[i] + ' and '

	command = command[:-4]
	command += ';'
	try:
		c.execute(command)
		mydb.commit()
		return ''
	except mysql.connector.Error as err:
		return err.msg

def show_tables():
	command = 'show tables;'
	c.execute(command)
	data = c.fetchall()
	return data

def get_attribute(table, keys, keys_values, attribute):
	command = 'select ' + attribute + ' from ' + table + ' where '
	for i in range(len(keys)):
		command += keys[i] + '=' + keys_values[i] + ' and '

	command = command[:-4]
	command += ';'

	try:
		c.execute(command)
	except mysql.connector.Error as err:
		return []
	data = c.fetchall()
	return data
	# print(command)
	# # c.execute(command)
	# # data = c.fetchall()
	# # return data

def misc_query(command):
	try:
		c.execute(command)
		cols = [i[0] for i in c.description]
		data = c.fetchall()
		try:
			mydb.commit()
		except mysql.connector.Error as err:
			pass
		finally:
			return (0, data, cols)
	except mysql.connector.Error as err:
		return (1, err.msg, '')





