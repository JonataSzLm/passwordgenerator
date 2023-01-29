import hashlib

from token_manage import Token_Manage
from database import _connect_db


class Users_Model:
    def __init__(self):
        self.connection = _connect_db()
        self.cursor = self.connection.cursor()
        self.token_manage = Token_Manage()

    def login(self, login, password):
        try:
            if login and password:
                obj_hash = hashlib.sha3_512()
                obj_hash.update(password.encode())
                password = obj_hash.hexdigest()
                params = (login, password)
            else:
                print('Informar usuario e senha validos!')
                return False, False, False

            sql = 'SELECT * FROM users WHERE login = %s AND password = %s'
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            if result:
                token = self.token_manage.create_token(result)
                return token, result[1], result[2]
            else:
                print('Usuario ou senha invalidos!')
                return False, False, False

        except Exception as e:
            print(e)
            return False, False, False

    def logout(self):
        self.cursor.close()
        self.connection.close()

    def create_user(self, name, login, password):
        try:
            if name and login and password:
                obj_hash = hashlib.sha3_512()
                obj_hash.update(password.encode())
                password = obj_hash.hexdigest()
                params = (name, login, password)
            else:
                print('Usuario nao informado!')
                return False

            sql = 'INSERT INTO users (name, login, password) VALUES (%s, %s, %s)'
            self.cursor.execute(sql, params)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return True

        except Exception as e:
            print(e)
            return False

    def update_user(self, token, name=None, login=None, password=None):
        try:
            data = self.token_manage.check_token(token)
            if data:

                if not name:
                    name = data['name']

                if not login:
                    login = data['login']

                if password:
                    obj_hash = hashlib.sha3_512()
                    obj_hash.update(password.encode())
                    password = obj_hash.hexdigest()
                    sql = 'UPDATE users SET name = %s, login = %s, password = %s WHERE id = %s'
                    params = (name, login, password, data['id'])

                else:
                    sql = 'UPDATE users SET name = %s, login = %s WHERE id = %s'
                    params = (name, login, data['id'])

                self.cursor.execute(sql, params)
                self.connection.commit()
                self.cursor.close()
                self.connection.close()
                return True

            else:
                print('Token Invalido!')
                return False

        except Exception as e:
            print(e)
            return False

    def delete_user(self, token):
        try:
            data = self.token_manage.check_token(token)
            if data:
                params = tuple(data['id'])
            else:
                print('Token Invalido!')
                return False

            sql = 'DELETE FROM users WHERE id = %s'
            self.cursor.execute(sql, params)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            return True

        except Exception as e:
            print(e)
            return False
