from Cryptodome.Cipher import AES
import string, base64


class AESCipher(object):
    def __init__(self, key,iv):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB,self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    def decrypt(self, raw):
        decoded = base64.b64decode(raw + b'===')
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decrypted = self.cipher.decrypt(decoded)
        try:
            return str(decrypted, 'utf-8')
        except:
            try:
                return str(decrypted, 'cp1252')

            except Exception as e:
                print('unable to decrypt message: ', e)
                raise Exception('unable to decrypt message')



key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

cipher = AESCipher(key,iv)
