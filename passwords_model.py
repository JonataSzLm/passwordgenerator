import random
import string

from token_manage import Token_Manage
from database import _connect_db


class Passwords_Model:
    def __init__(self):
        self.connection = _connect_db()
        self.cursor = self.connection.cursor()
        self.token_manage = Token_Manage()

    def random_generate(self, size=8, complexity=2):
        charcters = string.ascii_letters
        if complexity > 0:
            charcters += string.digits
            if complexity >= 2:
                charcters += string.punctuation

        password = ''.join(random.choice(charcters) for i in range(size))
        return password

    def create_password(self, token, name, login, password):
        try:
            data = self.token_manage.check_token(token)

            if data:
                user_id = data['id']

                if user_id and name and login and password:
                    password = self.token_manage.encrypt_password(password)
                    params = (user_id, name, login, password)
                else:
                    print('Informações insuficientes!')
                    return False

                sql = 'INSERT INTO passwords (user_id, name, login, password) VALUES (%s, %s, %s, %s)'
                self.cursor.execute(sql, params)
                self.connection.commit()
                return True

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False

    def read_all_passwords(self, token):
        try:
            data = self.token_manage.check_token(token)
            if data:
                sql = 'SELECT * FROM passwords WHERE user_id = %s'
                params = tuple(str(data['id']))
                self.cursor.execute(sql, params)
                result = self.cursor.fetchall()
                return result

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False

    def read_password(self, token, id):
        try:
            data = self.token_manage.check_token(token)
            if data:

                if id:
                    params = (id, data['id'])
                else:
                    print('Usuario nao informado!')
                    return False

                sql = 'SELECT * FROM passwords WHERE id = %s AND user_id = %s'
                self.cursor.execute(sql, params)
                result = self.cursor.fetchone()
                password = self.token_manage.decrypt_password(bytes(result[4]))
                return result[2], result[3], password

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False

    def update_password(self, token, id, name, login, password):
        try:
            data = self.token_manage.check_token(token)
            if data:

                user_id = data['id']

                if id:
                    params = (name, login, password, id, user_id)
                else:
                    print('Usuario nao informado!')
                    return False

                sql = 'UPDATE passwords SET name = %s, login = %s, password = %s WHERE id = %s AND user_id = %s'
                self.cursor.execute(sql, params)
                self.connection.commit()
                return True

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False

    def delete_password(self, token, id):
        try:
            data = self.token_manage.check_token(token)
            if data:

                if id:
                    params = (id, data['id'])
                else:
                    print('Usuario nao informado!')
                    return False

                sql = 'DELETE FROM passwords WHERE id = %s AND user_id = %s'
                self.cursor.execute(sql, params)
                self.connection.commit()
                return True

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False

    def delete_all_passwords(self, token):
        try:
            data = self.token_manage.check_token(token)
            if data:

                if id:
                    params = tuple(str(data['id']))
                else:
                    print('Usuario nao informado!')
                    return False

                sql = 'DELETE FROM passwords WHERE user_id = %s'
                self.cursor.execute(sql, params)
                self.connection.commit()
                return True

            else:
                print('Usuario não autenticado!')
                return False

        except Exception as e:
            print(e)
            return False