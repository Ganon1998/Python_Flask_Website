import socketserver
import Encrypt
import sqlite3 as sql

# prepares server for message to be received (Boss Server)
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''        self.data = self.request.recv(1024)
        print("{}  sent message:  " .format(self.client_address[0]))
        self.data = str(Encrypt.cipher.decrypt(self.data))
        print(self.data)'''

        # get message
        self.data = self.request.recv(1024).strip()
        #self.data = str(Encrypt.cipher.decrypt(self.data))
        msgData = str(Encrypt.cipher.decrypt(self.data))

        # parse the filler text out of it
        x = msgData.split(":::::::::::")

        # the list that returns from split() will have the ID first
        print((x[0]))
        print("   sent message:    ".format(self.client_address[0]))
        # the second element in the list will have the message
        print(x[1])
        # connect to messages database
        with sql.connect("Messages.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            # insert encrypted data into database
            eID = str(Encrypt.cipher.encrypt(bytes(x[0], 'utf-8')).decode("utf-8"))
            eMess = str(Encrypt.cipher.encrypt(bytes(x[1], 'utf-8')).decode("utf-8"))

            try:
                cur.execute("INSERT INTO Messages (AgentID, Message) VALUES (?,?)", (eID, eMess))
                con.commit()
            except:
                con.rollback()



if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

        server.serve_forever()

    except server.error as e:
        print("Error: ", e)
        exit(1)

    finally:
        server.close()