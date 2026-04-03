from account import create_account, log_in
from functions import line


class Main:
    def __init__(self):
        line()
        print("Olá! Bem-vindo ao nosso banco digital!")
        line()

        while True:
            print("\nEscolha uma opção do menu:")
            print("1. Criar conta")
            print("2. Logar")
            print("3. Sair")
            line()

            opt = input("Digite o número da opção desejada: ")
            line()

            match opt:
                case "1":
                    create_account()
                case "2":
                    log_in()
                case "3":
                    print("Obrigado por usar nosso banco digital. Até logo!")
                    exit()
                case _:
                    break


Main()
