import sqlite3
import Encrypt
import pandas as pd

# get access to a db file I made named MyTable.db
conn = sqlite3.connect('AgentDB.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()

conn.commit()

# encrypt the critical pieces of information to the database for 6 rows
ename = str(Encrypt.cipher.encrypt(b'Princess Diana').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Lady Di').decode("utf-8"))
elogin = str(Encrypt.cipher.encrypt(b'test123').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword) 
VALUES(1, ?, ?, 1, ?)''', (ename, ealias, elogin))

ename = str(Encrypt.cipher.encrypt(b'Henry Thorgood').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Goody 2 shoes').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword)
VALUES(2, ?, ?, 3, ?)''', (ename, ealias, elogin))

ename = str(Encrypt.cipher.encrypt(b'Tina Fairchild').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Happy').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword)
VALUES(3, ?, ?, 1, ?)''', (ename, ealias, elogin))

ename = str(Encrypt.cipher.encrypt(b'Tom Smith').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Sleepy').decode("utf-8"))
elogin = str(Encrypt.cipher.encrypt(b'test987').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword)
VALUES(4, ?, ?, 1, ?)''', (ename, ealias, elogin))

ename = str(Encrypt.cipher.encrypt(b'Kim Lovegood').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Snoozy').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword)
VALUES(5, ?, ?, 2, ?)''', (ename, ealias, elogin))

ename = str(Encrypt.cipher.encrypt(b'Tim Harris').decode("utf-8"))
ealias = str(Encrypt.cipher.encrypt(b'Doc').decode("utf-8"))
cur.execute('''INSERT INTO SecretAgent (AgentID, Name, Alias, SecurityLevel, LoginPassword)
VALUES(6, ?, ?, 3, ?)''', (ename, ealias, elogin))

conn.commit()

# loop through to print information
for row in cur.execute('''SELECT * FROM SecretAgent'''):
    print(row)

conn.commit()

cur.execute("SELECT * FROM SecretAgent")
Info = pd.DataFrame(cur.fetchall(), columns=['AgentID', 'Name', 'Alias', 'SecurityLevel', 'LoginPassword'])

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

print("\n")
# print the information that has been decrypted
print("Names: ")
for i in Info['Name']:
    print(i)

print("\n")

print("Alias: ")
for i in Info['Alias']:
    print(i)

print("\n")

print("LoginPasswords: ")
for i in Info['LoginPassword']:
    print(i)