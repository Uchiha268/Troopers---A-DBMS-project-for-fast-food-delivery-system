import mysql.connector

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = ""
# )

# c = mydb.cursor()

import streamlit as st
from database import create_table
from functions import delete, create, update, query
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

user_names = []
passwords = []



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fast_food"
)

c = mydb.cursor()
c.execute("USE fast_food")
# user_names = []
# passwords = []
# names = []
# c.execute("select user_id from user;")
# data = c.fetchall()
# for name in data:
#     user_names.append(name[0])

# c.execute("select password from user;")
# data = c.fetchall()
# for password in data:
#     passwords.append(password[0])

# c.execute("select name from user;")
# data = c.fetchall()
# for name in data:
#     names.append(name[0])


# credentials = {}

# credentials["usernames"] = {}
# for i in range(len(user_names)):
#     temp = {}
#     temp["name"] = names[i]
#     temp["password"] = passwords[i]
#     credentials["usernames"][user_names[i]] = temp

# authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
# name, authentication_status, username = authenticator.login("Login", "main")



def main():
    user_names = []
    passwords = []
    names = []
    c.execute("select user_id from user;")
    data = c.fetchall()
    for name in data:
        user_names.append(name[0])

    c.execute("select password from user;")
    data = c.fetchall()
    for password in data:
        passwords.append(password[0])

    hashed_passwords = hashed_passwords = stauth.Hasher(passwords).generate()

    c.execute("select name from user;")
    data = c.fetchall()
    for name in data:
        names.append(name[0])


    credentials = {}

    credentials["usernames"] = {}
    for i in range(len(user_names)):
        temp = {}
        temp["name"] = names[i]
        temp["password"] = hashed_passwords[i]
        credentials["usernames"][user_names[i]] = temp

    authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=0)
    name, authentication_status, username = authenticator.login("Login", "main")
    print(authentication_status)
    if authentication_status == False:
        st.error("Username/Password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")


    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")
        c.execute('select permissions from user where user_id = ' + '\'' + username + '\'' + ';')
        data = c.fetchall()
        permission = data[0][0]
        st.title("Troopers")
        # menu = ["Add", "View", "Edit", "Remove"]

        admin_menu = ["Add", "Edit", "Remove", "Misc Queries"]
        user_menu = ["Add", "Edit", "Remove"]
        delivery_menu = ["Edit"]
        if(permission == 'end_user'):
            choice = st.sidebar.selectbox("Menu", user_menu)
        elif(permission == "administrator"):
            choice = st.sidebar.selectbox("Menu", admin_menu)
        else:
            choice = st.sidebar.selectbox("Menu", delivery_menu)


        # create_table()
        if choice == "Add":
            st.subheader("Enter details:")
            create()
        elif choice == "Misc Queries":
            st.subheader("Enter any query -")
            query()
        elif choice == "Edit":
            st.subheader("Update tasks")
            update()
        elif choice == "Remove":
            st.subheader("Delete tasks")
            delete()
        else:
            st.subheader("About tasks")

    c.close()

if __name__ == '__main__':
    main()
