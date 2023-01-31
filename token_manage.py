import jwt
import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Token_Manage:
    def __init__(self):
        self.key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16'
        self.secretkey = 'S3cr3t#K3y'

    def create_token(self, result):
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({'user_id': result[0], 'username': result[1], 'login': result[2], 'exp': int(
            expires.timestamp())}, self.secretkey, algorithm='HS256')
        return token

    def check_token(self, token):
        try:
            data = jwt.decode(token, self.secretkey, algorithms=['HS256'])
            user_id = data.get('user_id')
            username = data.get('username')
            login = data.get('login')
            return {'id': user_id, 'name': username, 'login': login}

        except jwt.exceptions.InvalidSignatureError:
            print('Assinatura Invalida!')
            return False

        except jwt.exceptions.ExpiredSignautreError:
            print('Sessão expirada!')
            return False

        except Exception as e:
            print(e)
            return False

    def encrypt_password(self, password):
        try:
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padding = 16 - len(password) % 16
            password += chr(padding) * padding
            ciphertext = iv + cipher.encrypt(password.encode())
            return ciphertext
        except Exception as e:
            print(e)
            return False

    def decrypt_password(self, ciphertext):
        try:
            iv = ciphertext[:16]
            ciphertext = ciphertext[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            password = cipher.decrypt(ciphertext).decode()
            padding = ord(password[-1])
            password = password[:-padding]

            return password
        except Exception as e:
            print(e)
            return False
