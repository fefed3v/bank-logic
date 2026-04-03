import json
import os


def save_account(account):
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    else:
        accounts = []

    accounts.append(account)

    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)


def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            return json.load(file)
    return []


def format_cpf(cpf):
    cpf = "".join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        raise ValueError("CPF deve conter 11 dígitos.")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def format_phone_number(phone):
    phone = "".join(filter(str.isdigit, phone))
    if len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    elif len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    else:
        raise ValueError("Número de telefone deve conter 10 ou 11 dígitos.")


def format_email(email):
    if "@" not in email or "." not in email:
        raise ValueError("Email inválido.")
    return email.strip().lower()


def format_gender(gender):
    gender = gender.strip().lower()
    if gender not in ["masculino", "feminino", "outro"]:
        raise ValueError("Gênero inválido.")
    return gender


def format_age(age):
    if age < 0 or age > 120:
        raise ValueError("Idade inválida.")
    return age


def show_balance(balance):
    def get_balance_by_cpf(cpf):
        accounts = load_accounts()
        for account in accounts:
            if account.get("cpf") == cpf:
                return account.get("balance", 0)
        raise ValueError("CPF não encontrado.")

    print(f"Saldo da sua conta: R$ {balance:.2f}")
    line()


def get_account_by_cpf(cpf):
    accounts = load_accounts()
    return next((acc for acc in accounts if acc.get("cpf") == cpf), None)


def update_account(account):
    accounts = load_accounts()
    for idx, acc in enumerate(accounts):
        if acc.get("cpf") == account.get("cpf"):
            accounts[idx] = account
            break
    else:
        accounts.append(account)
    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)


def deposit(balance):
    cpf = input("Digite o CPF da conta: ")
    cpf_formatted = format_cpf(cpf)
    account = get_account_by_cpf(cpf_formatted)
    if not account:
        print("CPF não encontrado.")
        line()
        return balance

    try:
        amount = float(input("Digite o valor a ser depositado: R$ "))
        if amount <= 0:
            print("Valor inválido. O depósito deve ser maior que zero.")
            line()
            return balance
        account["balance"] = account.get("balance", 0) + amount
        update_account(account)
        print(f"Depósito de R$ {amount:.2f} realizado com sucesso!")
        line()
        return account["balance"]
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        line()
        return balance


def withdraw(balance):
    cpf = input("Digite o CPF da conta: ")
    cpf_formatted = format_cpf(cpf)
    account = get_account_by_cpf(cpf_formatted)
    if not account:
        print("CPF não encontrado.")
        line()
        return balance

    try:
        amount = float(input("Digite o valor a ser sacado: R$ "))
        if amount <= 0:
            print("Valor inválido. O saque deve ser maior que zero.")
            line()
            return balance
        if amount > account.get("balance", 0):
            print("Saldo insuficiente para realizar o saque.")
            line()
            return balance
        account["balance"] = account.get("balance", 0) - amount
        update_account(account)
        print(f"Saque de R$ {amount:.2f} realizado com sucesso!")
        line()
        return account["balance"]
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        line()
        return balance


def transfer(balance):
    sender_cpf = input("Digite o CPF da sua conta: ")
    cpf_formatted = format_cpf(sender_cpf)
    sender_account = get_account_by_cpf(cpf_formatted)
    if not sender_account:
        print("CPF do remetente não encontrado.")
        line()
        return balance

    recipient_cpf = input("Digite o CPF do destinatário: ")
    cpf_formatted = format_cpf(recipient_cpf)
    recipient_account = get_account_by_cpf(cpf_formatted)
    if not recipient_account:
        print("CPF do destinatário não encontrado.")
        line()
        return balance

    try:
        amount = float(input("Digite o valor a ser transferido: R$ "))
        if amount <= 0:
            print("Valor inválido. A transferência deve ser maior que zero.")
            line()
            return balance
        if amount > sender_account.get("balance", 0):
            print("Saldo insuficiente para realizar a transferência.")
            line()
            return balance

        sender_account["balance"] -= amount
        recipient_account["balance"] = recipient_account.get("balance", 0) + amount
        update_account(sender_account)
        update_account(recipient_account)

        print(
            f"Transferência de R$ {amount:.2f} para CPF {recipient_cpf} realizada com sucesso!"
        )
        line()
        return sender_account["balance"]
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        line()
        return balance


def generate_account_id():
    import uuid

    return str(uuid.uuid4())


def line(size=50):
    print("-" * size)
