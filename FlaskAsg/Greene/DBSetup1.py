import sqlite3

# get access to a db file I made named MyTable.db
conn = sqlite3.connect('AgentDB.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()

conn.commit()

try:
    cur.execute('''DROP TABLE SecretAgent''')
    conn.commit()
except:
    pass

# create a new table
cur.execute('''CREATE TABLE SecretAgent(
AgentID INTEGER PRIMARY KEY,
Name TEXT NOT NULL,
Alias TEXT NOT NULL,
SecurityLevel INT,
LoginPassword TEXT NOT NULL);''')

conn.commit()