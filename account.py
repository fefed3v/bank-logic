import json
import os

from functions import *


def create_account():
    print("Crie sua conta!")
    line()

    cpf = input("Digite seu CPF: ")
    email = input("Digite seu email: ")
    phone_number = input("Digite seu número de telefone: ")

    password = input("Digite sua senha: ")
    matched_password = input("Confirme sua senha: ")

    first_name = input("Digite seu nome: ")
    last_name = input("Digite seu sobrenome: ")

    age = int(input("Digite sua idade: "))
    gender = input("Digite seu gênero: ")

    line()

    if password != matched_password:
        print("As senhas não coincidem. Tente novamente.")
        line()
        return

    if len(password) < 6:
        print("A senha deve conter pelo menos 6 caracteres.")
        line()
        return

    if "@" not in email or "." not in email:
        print("Email inválido. Tente novamente.")
        line()
        return

    try:
        email = format_email(email)
        gender = format_gender(gender)
        age = format_age(age)
        cpf = format_cpf(cpf)
        phone_number = format_phone_number(phone_number)
    except ValueError as e:
        print(f"Erro de validação: {e}")
        line()
        return

    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
        if any(acc["email"] == email for acc in accounts):
            print("Email já cadastrado. Tente novamente.")
            line()
            return
        if any(acc["cpf"] == cpf for acc in accounts):
            print("CPF já cadastrado. Tente novamente.")
            line()
            return
        if any(acc["phone_number"] == phone_number for acc in accounts):
            print("Número de telefone já cadastrado. Tente novamente.")
            line()
            return

    account = {
        "id": generate_account_id(),
        "cpf": cpf,
        "phone_number": phone_number,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "gender": gender,
        "balance": 0.0,
    }

    save_account(account)

    print("Conta criada com sucesso!")
    print(f"Bem-vindo, {first_name}!")
    line()

    print('Agora clique em "Logar" para acessar sua conta.')
    line()

    log_in()


def log_in():
    print("Faça login na sua conta!")
    line()

    cpf = input("Digite seu CPF: ")
    password = input("Digite sua senha: ")
    line()

    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            accounts = json.load(file)

        cpf_formatted = format_cpf(cpf)
        account_found = next(
            (acc for acc in accounts if acc["cpf"] == cpf_formatted),
            None,
        )

        if not account_found:
            print("CPF não encontrado. Tente novamente.")
            line()
            return

    cpf_formatted = format_cpf(cpf)

    accounts = load_accounts()
    account = next(
        (
            acc
            for acc in accounts
            if acc["cpf"] == cpf_formatted and acc["password"] == password
        ),
        None,
    )

    if account:
        while True:
            print(f"Login bem-sucedido! Bem-vindo de volta, {account['first_name']}!")
            line()

            print("\nEscolha uma opção do menu:")
            print("1. Ver saldo")
            print("2. Depositar")
            print("3. Sacar")
            print("4. Transferir")
            print("5. Sair")
            line()

            opt = input("Digite o número da opção desejada: ")
            line()

            match opt:
                case "1":
                    show_balance(account["balance"])
                case "2":
                    deposit(account["balance"])
                case "3":
                    withdraw(account["balance"])
                case "4":
                    transfer(account["balance"])
                case "5":
                    print("Obrigado por usar nosso banco digital. Até logo!")
                    exit()
                case _:
                    return
    else:
        print("CPF ou senha incorretos. Tente novamente.")
        line()
