import sqlite3

# get access to a db file
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
AgentID INTEGER IDENTITY(7,1) PRIMARY KEY,
Name TEXT,
Alias TEXT,
SecurityLevel INT,
LoginPassword TEXT);''')

conn.commit()