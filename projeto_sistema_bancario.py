menu = """--------------------------------------------------------------------------------------------------------
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

 => """

limite = 500
total_conta = 0
numero_saques = 0
LIMITE_SAQUES = 3
extrato = ""

while True:
    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input("""
----------------------------------------------------------------------------------------------------------
                DEPÓSITO
VALOR PARA DEPOSITAR => """))

        if valor_deposito < 0:
            print("NÃO É POSSÍVEL DEPOSITAR VALORES NEGATIVOS.\n")
            valor_deposito = 0
        else:
            print(f"R${valor_deposito:.2f} depositado\n")
            extrato += f"Foi depositado R${valor_deposito}\n"
            total_conta += valor_deposito

    elif opcao == "s":
        saque = int(input("""
----------------------------------------------------------------------------------------------------------
                SAQUE
VALOR PARA SACAR => """))

        if saque > 500:
            print("O saque possui limite de R$500.00\n")
        elif saque > total_conta:
            print("Não será possível sacar o dinheiro por falta de saldo.")
        elif numero_saques < LIMITE_SAQUES:
            total_conta -= saque
            extrato += f"Foi sacado R${saque:.2f}\n"
            numero_saques += 1
        else:
            print("ALERTA: o limite de saques diário foi alcançado\n")

    elif opcao == "e":
        print(f"                  EXTRATO\n{extrato}")
        print(f" *SALDO DE CONTA: {total_conta:.2f}.\n")
    elif opcao == "q":
        break
    else:
        print("Operação inválida\n")