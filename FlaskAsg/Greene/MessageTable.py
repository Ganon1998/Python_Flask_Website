import sqlite3

# get access to a db file
conn = sqlite3.connect('Messages.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()

conn.commit()

try:
    cur.execute('''DROP TABLE Messages''')
    conn.commit()
except:
    pass

# create a new table
cur.execute('''CREATE TABLE Messages(
MessageID INTEGER IDENTITY(1,1) PRIMARY KEY,
AgentID INTEGER,
Message TEXT);''')

conn.commit()