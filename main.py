from users_model import Users_Model
from passwords_model import Passwords_Model

OPS_SIM = ['sim', 's', 'S', 'SIM', 'SIm',
           'SiM', 'sIM', 'sIm', 'ss', 'Ss', 'yes', 'y']

if __name__ == '__main__':
    try:
        user = Users_Model()
        passwords = Passwords_Model()
        print('Bem vindo ao Gerenciador de Senhas!!')
        print('[        LOGIN:      ]\n\n')
        username = input('Insira seu Usuario: ')
        password = input('Insira sua Senha: ')
        token, current_name, current_login = user.login(username, password)
        if token:
            print('Seja Bem-vindo {}!\n'.format(current_name))
            while True:
                print(
                    '[        MENU        ]\n1 - Atualizar Usuario:\n2 - Salvar senha:\n3 - Vizualizar senhas salvas:\n4 - Gerar senha aleatoria:\n\n0 - SAIR')
                op = input('Inisira a ação desejada: ')
                if op == '1':
                    new_name = input(
                        'Insira o novo nome para o usuario (vazio para manter {}): '.format(current_name))
                    if not new_name or new_name == ' ' or new_name == '':
                        new_name = None
                    new_login = input(
                        'Insira o novo login para o usuario (vazio para manter {}): '.format(current_login))
                    if not new_login or new_login == ' ' or new_login == '':
                        new_login = None
                    new_password = input(
                        'Insira a nova senha para o usuario (vazio para manter a senha anterior): ')
                    if not new_password or new_password == ' ' or new_password == '':
                        new_password = None

                    if (user.update_user(token, new_name, new_login, new_password)):
                        print('Usuario atualizado com sucesso!')
                    else:
                        print('Falha ao tentar atualizar o usuario!')

                if op == '2':
                    name_password = input(
                        'Insira um nome para Identificar a senha salva: ')
                    if not name_password or name_password == ' ' or name_password == '':
                        name_password = None
                    login_password = input(
                        'Insira o login para esta senha: ')
                    if not login_password or login_password == ' ' or login_password == '':
                        login_password = None
                    password_save = input(
                        'Insira a senha para ser salva: ')
                    if not password_save or password_save == ' ' or password_save == '':
                        password_save = None

                    if (passwords.create_password(token, name_password, login_password, password_save)):
                        print('Senha salva com sucesso!')
                    else:
                        print('Falha ao tentar salvar a senha!')

                if op == '3':
                    all_passwords = passwords.read_all_passwords(token)
                    print('Senhas salvas:')
                    for one_password in all_passwords:
                        print('{} - {} \n'.format(
                            one_password[0], one_password[2]))

                    id_password = input('Selecione um registro: ')
                    if id_password:
                        name_password, login_password, password_save = passwords.read_password(token, id_password)
                        print(' -----   {}  -----\nLOGIN: {}\nSENHA: {}'.format(name_password, login_password, password_save))

                if op == '4':
                    complexity = input(
                        'Informe a complexidade da senha\n0 - FRACA (apenas letras)\n1 - MEDIA (letras e numeros)\n2 - ALTA (letras, numeros e caracteres especiais)\nInisira o valor (Padrão: ALTA): ')
                    size = input('Informe o tamanho da senha (Padrão: 8): ')
                    random_password = passwords.random_generate(
                        int(size), int(complexity))
                    print('Senha Aleatoria: {}'.format(random_password))

                if op == '0':
                    print('Encerrando Aplicação...')
                    token = False
                    user.logout()
                    break

        else:
            print('Falha na Autenticação!')
            op_sim = input('Deseja Criar um usuario? ')
            if op_sim in OPS_SIM:
                print('[        NOVO USUARIO        ]')
                name = input('Insira o nome para o seu usuario: ')
                login = input('Insira o login que sera usado: ')
                password = input('Insira a senha a ser utilizada: ')
                if (user.create_user(name, login, password)):
                    print('Usuario Criado com Sucesso!')
                else:
                    print('Falha ao tentar criar o usuario!')

    except KeyboardInterrupt:
        user.logout()
    except Exception as e:
        print(e)
        user.logout()
