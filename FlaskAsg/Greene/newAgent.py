import sqlite3 as sql
import sys

from flask import Flask, render_template, request, session, flash
import os

"""

Name: Jordan Greene
Date:2/3/2021
Assignment: (Assignment #5)
Due Date: 2/7/2021
About this project: Add a login page and maintain sessions throughout the traversal of the website.

"""

app = Flask(__name__)


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
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('agent.html')


# this function loads when the user inputs data for new agent while using POST
# only runs if the person is logged in
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if session.get('logged_in'):
        if request.method == 'POST':
            try:
                name = request.form['Name']
                alias = request.form['Alias']
                secureLv = request.form['Security Level']
                login = request.form['Login Password']

                messageName = "Please don't leave Name empty. Try again"
                messageAl = "Please don't leave Alias empty. Try again"
                messageSecLv = "Please input a Security Level value between 1-10. Try again"
                messageLogin = "Please don't leave Login empty. Try again"

                if not name or not alias or not secureLv or not login:
                    pass
                else:
                    with sql.connect("AgentDB.db") as con:

                        cur = con.cursor()
                        cur.execute("INSERT INTO SecretAgent VALUES (?,?,?,?)", (name, alias, secureLv, login))
                        con.commit()
                        message = "Record successfully added"

            except:
                con.rollback()
                message = "error in insert operation"

            finally:

                # error checking for empty inputs
                if not name:
                    return render_template("result.html", msg=messageName)
                if not alias:
                    return render_template("result.html", msg=messageAl)
                if not secureLv or int(secureLv) > 10 or int(secureLv) < 1:
                    return render_template("result.html", msg=messageSecLv)
                if not login:
                    return render_template("result.html", msg=messageLogin)

                return render_template("result.html", msg=message)

            con.close()
    else:
        return render_template('result.html', msg=" Page not found.")


# this function list all the rows in the SecretAgent table from AgentDB.db
# this only runs if the person is logged in
@app.route('/list')
def list():
    if session.get('logged_in'):
        con = sql.connect("AgentDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM SecretAgent")

        rows = cur.fetchall()
        return render_template("list.html", rows=rows)
    else:
        return render_template('result.html', msg=" Page not found.")


# login function
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        nm = request.form['username']
        password = request.form['password']

        # get connection to database
        with sql.connect("AgentDB.db") as con:

            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = '''SELECT * FROM SecretAgent WHERE Name = ? AND LoginPassword = ?'''
            cur.execute(sql_select_query, (nm, password))

            row = cur.fetchone()

            # checks to see if the row retreived is actually in the database or not
            if row != None:
                session['name'] = nm
                session['logged_in'] = True
                session['SecurityLevel'] = int(row['SecurityLevel'])
                # go to home.html with info about the person who logged in via secureLv
                # the secureLv determines what the user is allowed to see on the homepage.
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
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
