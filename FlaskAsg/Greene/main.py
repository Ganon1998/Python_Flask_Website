import sqlite3 as sql
import sys
import pandas as pd
import Encrypt
from flask import Flask, render_template, request, session, flash
import os
import socket
import hmac, hashlib, _sha3

"""

Name: Jordan Greene
Date: 3/21/2021
Assignment: (Assignment #10)
Due Date: 3/21/2021
About this project: Have a process run using threadinge.

"""

app = Flask(__name__)
MessagesArray = [" " for x in range(5)]

# default page that's loaded
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')


# function for when the user wants to add a new agent
@app.route('/enternew')
def new_Secret_Agent():
    if not session.get('logged_in') or session.get('SecurityLevel') != 1:
        Message[5] = [" " for x in range(5)]
        Message[0] = "Query Result: Page Not Found"
        return render_template('result.html', msg=Message)
    else:
        return render_template('agent.html')


# this function loads when the user inputs data for new agent while using POST
# only runs if the person is logged in
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if session.get('logged_in') and session.get('SecurityLevel') == 1:
        if request.method == 'POST':
            try:
                name = request.form['Name']
                alias = request.form['Alias']
                secureLv = request.form['Security Level']
                login = request.form['Login Password']

                # encrypt the information before accessing the database
                ename = str(Encrypt.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
                ealias = str(Encrypt.cipher.encrypt(bytes(alias, 'utf-8')).decode("utf-8"))
                elogin = str(Encrypt.cipher.encrypt(bytes(login, 'utf-8')).decode("utf-8"))

                MessagesArray = [" " for x in range(5)]

                messageName = "Please don't leave Name empty. Try again"
                messageAl = "Please don't leave Alias empty. Try again"
                messageSecLv = "Please input a Security Level value between 1-10. Try again"
                messageLogin = "Please don't leave Login empty. Try again"

                if not name or not alias or not secureLv or not login:
                    pass
                else:
                    with sql.connect("AgentDB.db") as con:

                        cur = con.cursor()
                        cur.execute("INSERT INTO SecretAgent (Name, Alias, SecurityLevel, LoginPassword) VALUES (?,?,?,?)", (ename, ealias, secureLv, elogin))
                        con.commit()
                        message = "Record successfully added"
                        MessagesArray[0] = message

            except:
                con.rollback()
                message = "error in insert operation"
                MessagesArray[0] = message

            finally:

                # error checking for empty inputs
                if not name:
                    MessagesArray[1] = messageName
                if not alias:
                    MessagesArray[2] = messageAl
                if not secureLv or int(secureLv) > 10 or int(secureLv) < 1:
                    MessagesArray[3] = messageSecLv
                if not login:
                    MessagesArray[4] = messageLogin

                return render_template("result.html", msg=MessagesArray)

            con.close()
    else:
        return render_template('login.html')


# this function list all the rows in the SecretAgent table from AgentDB.db
# this only runs if the person is logged in
@app.route('/list')
def list():
    if session.get('logged_in') and session.get('SecurityLevel') < 3:
        con = sql.connect("AgentDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM SecretAgent")
        Info = pd.DataFrame(cur.fetchall(), columns=['MessageID', 'AgentID','Name', 'Alias','SecurityLevel', 'LoginPassword'])

        # decrypt the info from the database
        index = 0
        for i in Info['Name']:
            i = str(Encrypt.cipher.decrypt(i))
            Info._set_value(index, 'Name', i)
            index += 1

        index = 0
        for i in Info['Alias']:
            i = str(Encrypt.cipher.decrypt(i))
            Info._set_value(index, 'Alias', i)
            index += 1

        index = 0
        for i in Info['LoginPassword']:
            i = str(Encrypt.cipher.decrypt(i))
            Info._set_value(index, 'LoginPassword', i)
            index += 1

        con.close()
        return render_template("list.html", rows=Info)
    else:
        return home()


# login function
@app.route('/login', methods=['POST'])
def login():
    try:
        nm = request.form['username']
        password = request.form['password']

        # encrypt name and password after receiving info
        ename = str(Encrypt.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
        elogin = str(Encrypt.cipher.encrypt(bytes(password, 'utf-8')).decode("utf-8"))

        # get connection to database
        with sql.connect("AgentDB.db") as con:

            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = '''SELECT * FROM SecretAgent WHERE Name = ? AND LoginPassword = ?'''
            cur.execute(sql_select_query, (ename, elogin))

            row = cur.fetchone()
            # checks to see if the row retrieved is actually in the database or not
            if row != None:
                session['name'] = nm
                session['logged_in'] = True
                session['SecurityLevel'] = int(row['SecurityLevel'])
                # go to home.html with info about the person who logged in via session SecurityLevel
                # the SecurityLevel determines what the user is allowed to see on the homepage.
                return render_template("home.html")
            else:
                session['logged_in'] = False
                flash('error in login.')
    except:
        # if for some reason the connection fails
        con.rollback()
        flash('error in login process')

    finally:
        con.close()

    # return home in case there's no data in the database for the login
    return home()


@app.route("/logout")
def logout():
    session['name'] = ""
    session['logged_in'] = False
    session['SecurityLevel'] = 3
    return home()


@app.route('/message')
def help():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('SendMsg.html', name=session['name'])

# function that controls message
@app.route('/message', methods=['POST'])
def message():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            try:
                # connect to database to get agentID
                with sql.connect("AgentDB.db") as con:
                    # setup variables for connection to server and encrypt message
                    msg = request.form['message']
                    HOST, PORT = "localhost", 8888
                    MessagesArray[0] = "Error - Message NOT sent to boss"

                    # if a message was actually typed in
                    if msg and not msg.isspace():
                        # get name
                        nm = session.get('name')
                        enm = str(Encrypt.cipher.encrypt(bytes(nm, 'utf-8')).decode('utf-8'))

                        # setup cursor
                        con.row_factory = sql.Row
                        cur = con.cursor()

                        # get ID from database
                        sql_select_query = '''SELECT * FROM SecretAgent WHERE Name = ? AND SecurityLevel = ?'''
                        cur.execute(sql_select_query, (enm, session.get('SecurityLevel')))
                        row = cur.fetchone()
                        session['ID'] = str(row['AgentID'])

                        # add ID to the message and add a marker so the split() know what to split
                        data = session.get('ID') + ":::::::::::" + msg

                        # create tag
                        secret = b'1234'
                        computedTag = hmac.new(secret, bytes(data, 'utf-8'), digestmod=hashlib.sha3_512).digest()

                        # encrypt the data then append tag
                        data = str(Encrypt.cipher.encrypt(bytes(data, 'utf-8')).decode('utf-8')) + str(computedTag)

                        # get sockets ready and connect to host, send all, then close
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((HOST, PORT))
                        sock.sendall(bytes(data, 'utf-8'))
                        sock.close()

                        # success message
                        MessagesArray[0] = "Message successfully sent to boss"

                    elif msg.strip() == "":
                        MessagesArray[0] = "You can not enter in an empty message"
                        return render_template("result.html", msg=MessagesArray)
                    else:
                        return render_template("result.html", msg=MessagesArray)

            except Exception as e:
                MessagesArray[0] = "Error - Message NOT sent to boss"

            finally:
                con.close()
                return render_template("result.html", msg=MessagesArray)



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
