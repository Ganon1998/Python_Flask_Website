import socketserver
import Encrypt
import sqlite3 as sql
import hmac, hashlib

# prepares server for message to be received (Boss Server)
class MyTCPHandler(socketserver.BaseRequestHandler):

    def verify(self, message, received):
        # do encryption then check to see if the one that we received matches
        secret = b'1234'
        computed_sha = hmac.new(secret, bytes(message, 'utf-8'), digestmod=hashlib.sha3_512).digest()
        check = str(Encrypt.cipher.encrypt(bytes(message, 'utf-8')).decode('utf-8')) + str(computed_sha)

        # if the encryption generated here doesn't matches the encryption that we received, retun false
        if received != bytes(check, 'utf-8'):
            return False
        else:
            return True

    def handle(self):
        # get message
        self.data = self.request.recv(1024).strip()
        receivedData = self.data

        # get message by removing tag
        messageEncrypted = self.data[:len(self.data) - 64]
        msgData = str(Encrypt.cipher.decrypt(messageEncrypted))

        # verify authenticity
        authentic = self.verify(msgData, receivedData)

        if authentic:
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

                try:
                    cur.execute("INSERT INTO Messages (AgentID, Message) VALUES (?,?)", (x[0], x[1]))
                    con.commit()
                except:
                    con.rollback()
        else:
            print('Unauthenticated message received! Be on alert! Watch out for bad guys !!!')




if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 8888
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

        server.serve_forever()

    except server.error as e:
        print("Error: ", e)
        exit(1)

    finally:
        server.close()
