import getpass
import re

from users_model import Users_Model
from passwords_model import Passwords_Model

yes_variations = ["yes", "YES", "y", "Y", "s", "S",
                  "sim", "SIM", "ye", "YE", "si", "SI", "yea", "YEA"]
yes_typos = ["yea", "ys", "ye", "sy", "ess",
             "es", "sye", "sey", "yeas", "yesi", "ysi"]

all_yes_variations = yes_variations + yes_typos


def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*()]", password):
        return False
    return True


def start_menu():
    print('1. Fazer Login\n2. Criar Usuario\n\n0. Fechar')
    return int(input("Opção: "))


def create_user_menu():
    print('[        CRIAR USUARIO       ]\n\n')
    username = input('Informe o seu nome: ')
    userlogin = input('Informe o seu login: ')
    userpassword = input(
        'SENHA (a senha deverá possuir 8 caracteres no minimo, letras maiusculas, letras minusculas e numeros)\nInforme a sua senha: ')
    confirmpassword = input('Confirme a senha digitada anteriormente: ')
    if username and userlogin and userpassword and confirmpassword:
        if not username == ' ' and not userlogin == ' ':
            if is_strong_password(userpassword):
                if userpassword == confirmpassword:
                    return username, userlogin, userpassword
                else:
                    print('As senhas informadas não correspondem!')
            else:
                print('A senha informada não atende os requisitos exigidos!\n(As senhas deveram possuir no minimo 8 caracteres, possuir letras maiusculas e minusculas, numeros e caracteres especiais)')
        else:
            print('Informe valores validos nos campos de Nome e Login!')
    else:
        print('Valores invalidos!')

    option = input('Deseja tentar novamente? SIM ou NÃO (padrão NÃO): ')
    if option in all_yes_variations:
        create_user_menu()
    else:
        return False, False, False


def login_menu():
    print('[        FAZER LOGIN       ]\n\n')
    username = input('Login: ')
    password = getpass.getpass('Senha: ')
    if all([username, password]):
        return username, password
    op = input('Falha, informe valores validos!\n\nTentar novamente? (Padrão NÃO): ')
    
    if op in all_yes_variations:
        login_menu()
    
    return None, None


def main_menu():
    print("Escolha uma opção:")
    print("1. Gerenciar dados de usuário")
    print("2. Gerenciar senhas salvas")
    print("3. Gerar senha aleatória")
    print("0. Sair")
    return int(input("Opção: "))


def manage_user_data():
    print("Escolha uma opção:")
    print("1. Alterar a Senha")
    print("2. Alterar o Nome")
    print("3. Alterar o Login")
    print("4. Excluir usuário")
    print("0. Voltar")
    return int(input("Opção: "))


def manage_passwords():
    print("Escolha uma opção:")
    print("1. Adicionar novo registro de senha")
    print("2. Remover registro de senha")
    print("3. Atualizar registro de senha")
    print("4. Vizualizar registro de senha")
    print("0. Voltar")
    return int(input("Opção: "))


def show_passwords(token):
    all_passwords = passwords.read_all_passwords(token)
    if all_passwords:
        print('Senhas Cadastradas:')
        for one_password in all_passwords:
            print('{} - {}'.format(one_password[0], one_password[2]))
        print('\n')
    else:
        print('\nNão há nenhuma senha salva!\n')
    return False


def passwords_menu(current_name=None, current_login=None, current_password=None):
    if current_name and current_login and current_password:
        name = input('Nome do registro ({}): '.format(
            current_name)) or current_name
        login = input('Login utilizado ({}): '.format(
            current_login)) or current_login
        password = input('Senha utilzada ({}): '.format(
            current_password)) or current_password
    else:
        name = input('Nome do registro: ')
        login = input('Login utilizado: ')
        password = input('Senha utilzada: ')

    if name and login and password:
        return name, login, password
    else:
        return False, False, False


def random_gen_menu():
    size = int(input('Defina o tamanho da senha: ')) or 8
    complex = int(input('Defina a comlpexidade da senha\n[0 - Baixa, 1 - Media, 2 - Forte]: ')) or 2
    if size and complex:
        return size, complex
    return None, None


if __name__ == '__main__':
    print('[        GERENCIADOR DE SENHAS       ]\n\n')
    try:
        token = False
        while True:
            user = Users_Model()
            passwords = Passwords_Model()
            if not token:
                option_start = start_menu()
                if option_start == 1:
                    # REALIZAR LOGIN
                    username, password = login_menu()
                    if all([username, password]):
                        token, current_name, current_login = user.login(username, password)
                        if not token:
                            print('Falha na autenticação!')
                    continue

                elif option_start == 2:
                    # CRIAR NOVO USUARIO
                    createname, createlogin, createpassword = create_user_menu()
                    if createname and createlogin and createpassword:
                        if user.create_user(createname, createlogin, createpassword):
                            print('Usuario criado com Sucesso!')
                            continue
                        else:
                            print('Falha ao tentar criar o usuario!')
                            continue
                    else:
                        print('Valores Invalidos!')
                        continue

                elif option_start == 0:
                    user.logout()
                    token = False
                    break
                else:
                    print('Opção Inválida!\nPor favor selecione uma opção valida:')

            if token:
                # Usuario autenticado
                print('\n\nSeja Bem Vindo {}!\n'.format(current_name))
                option = main_menu()
                if option == 1:
                    print(
                        '\nUsuario: {}      Login: {}       Senha: *****\n\n'.format(current_name, current_login))
                    user_data_option = manage_user_data()
                    if user_data_option == 1:
                        # Alterar senha
                        new_password = input(
                            'SENHA (a senha deverá possuir 8 caracteres no minimo, letras maiusculas, letras minusculas e numeros)\nInforme a sua nova senha: ')
                        confirm_new_password = input(
                            'Confirme a senha digitada anteriormente:')
                        if is_strong_password(new_password):
                            if new_password == confirm_new_password:
                                if user.update_user(token, None, None, new_password):
                                    print(
                                        'A senha foi atualizada com sucesso!')
                                    continue
                                else:
                                    print(
                                        'Falha ao tentar atualizar a senha!')
                                    continue
                            else:
                                print('Falha! As senhas não correspondem!')
                                continue
                        else:
                            print(
                                'Falha! a senha inserida não corresponde as exigencias!')
                            continue
                    elif user_data_option == 2:
                        # Alterar Nome
                        new_name = input('Insira o novo nome: ')
                        if new_name and not new_name == ' ':
                            if user.update_user(token, new_name, None, None):
                                print('O Nome foi atualizado com sucesso!')
                                current_name = new_name
                                continue
                            else:
                                print('Falha ao tentar atualizar o nome!')
                                continue
                        else:
                            print('Valor invalido para o nome!')
                            continue
                    elif user_data_option == 3:
                        # Alterar login
                        new_login = input('Insira o novo nome: ')
                        if new_login and not new_login == ' ':
                            if user.update_user(token, None, new_login, None):
                                print('O Login foi atualizado com sucesso!')
                                current_login = new_login
                                continue
                            else:
                                print('Falha ao tentar atualizar o login!')
                                continue
                        else:
                            print('Valor invalido para o login!')
                            continue
                    elif user_data_option == 4:
                        confirm_op = input(
                            'Tem certeza que deseja excluir o usuario {}?\nSim ou Não (Padrão NÃO): '.format(current_name))
                        if confirm_op in all_yes_variations:
                            if passwords.delete_all_passwords(token):
                                if user.delete_user(token):
                                    print('Usuario excluido com sucesso!')
                                    user.logout()
                                    token = False
                                    continue
                            
                            print('Falha ao tentar excluir o usuario!')
                            continue
                        else:
                            continue
                    elif user_data_option == 0:
                        continue
                    else:
                        print('Opção Inválida!\nPor favor selecione uma opção valida:')

                elif option == 2:
                    show_passwords(token)
                    password_option = manage_passwords()
                    if password_option == 1:
                        # Adicionar nova senha
                        new_pass_name, new_pass_login, new_pass_password = passwords_menu()
                        if new_pass_name and new_pass_login and new_pass_password:
                            if passwords.create_password(token, new_pass_name, new_pass_login, new_pass_password):
                                print('Registro de senha criado com sucesso!')
                            else:
                                print(
                                    'Falha ao tentar salvar novo registro de senha!')
                        else:
                            print('Valores inseridos invalidos')
                        continue

                    elif password_option == 2:
                        pass_id = input('Informe o registro que deseja apagar: ')
                        pass_id = int(pass_id)
                        if pass_id:
                            if passwords.delete_password(token, pass_id):
                                print("Registro de senha removido com sucesso")
                                continue
                            print('Falha ao tentar remover o registro de senha {}!'.format(pass_id))
                            continue
                        print('Valor invalido!')
                        continue
                        # <----- CRIAR DEPOIS A EXCLUSAO CORRETA DE USUARIO (ANTES DE EXCLUIR VERIFICAR SE EXISTEM SENHAS SALVAS, CASO SIM EXCLUIR TODAS PRIMEIRO)
                        # Criar tambem uma opção de geração automatica de senha na parte do registro de senha...
                    elif password_option == 3:
                        pass_id = input('Informe o registro que deseja alterar: ')
                        pass_id = int(pass_id)
                        if pass_id:
                            old_pass_name, old_pass_login, old_pass_password = passwords.read_password(token, pass_id)
                            if all([old_pass_name, old_pass_login, old_pass_password]):
                                new_pass_name, new_pass_login, new_pass_password = passwords_menu(old_pass_name, old_pass_login, old_pass_password)
                                if all([new_pass_name, new_pass_login, new_pass_password]):
                                    if passwords.update_password(token, new_pass_name, new_pass_login, new_pass_password):
                                        print("Registro de senha atualizado com sucesso")
                                        continue
                                    print('Falha ao tentar remover o registro de senha {}!'.format(pass_id))
                                    continue

                        print('Valor invalido!')
                        continue
                    
                    elif password_option == 4:
                        #vizualizar senha
                        pass_id = input('Informe o registro que deseja vizualizar: ')
                        pass_id = int(pass_id)
                        if pass_id:
                            pass_name, pass_login, pass_password = passwords.read_password(token, pass_id)
                            if all([pass_name, pass_login, pass_password]):
                                print(" -----   {}   -----\nLogin: {}\nSenha: {}".format(pass_name, pass_login, pass_password))
                                pass_name, pass_login, pass_password = None
                                continue
                            print('Falha ao tentar remover o registro de senha {}!'.format(pass_id))
                            continue
                        print('Valor invalido!')
                        continue

                    elif password_option == 0:
                        continue
                    else:
                        print('Opção Inválida!\nPor favor selecione uma opção valida:')

                elif option == 3:
                    size, complexity = random_gen_menu()
                    if size and complexity:
                        print('Senha Gerada: {}'.format(passwords.random_generate(size, complexity)))
                    continue
                elif option == 0:
                    user.logout()
                    token = False
                    break
                else:
                    print(
                        'Opção Inválida!\nPor favor selecione uma opção valida:')

    except KeyboardInterrupt:
        user.logout()
    except Exception as e:
        print(e)
        user.logout()
