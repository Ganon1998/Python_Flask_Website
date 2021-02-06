import sqlite3

# get access to a db file I made named MyTable.db
conn = sqlite3.connect('AgentDB.db')
# create cursor object to gain access to methods like commit and execute
cur = conn.cursor()

conn.commit()

cur.execute('''DROP TABLE SecretAgent''')

# create a new table
cur.execute('''CREATE TABLE SecretAgent(
Name CHAR(40),
Alias CHAR(20),
SecurityLevel INT,
LoginPassword CHAR(20));''')

conn.commit()

# inserts 6 rows into the table
cur.execute('''INSERT INTO SecretAgent (Name, Alias, SecurityLevel, LoginPassword)
VALUES('Princess Diana', 'Lady Di', 1, 'test123');''')

conn.commit()