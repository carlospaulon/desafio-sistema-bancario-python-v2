print("Seja bem-vindo ao Sistema Bancário Python!")

def menu():
    menu = """
    ========== MENU ==========

    1 - Depositar
    2 - Sacar
    3 - Extrato
    4 - Cadastrar usuário
    5 - Cadastrar conta
    6 - Listar contas
    7 - Sair

    ========================== 

=> """
    return int(input(menu))


def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"Depósito: \tR$ {valor_deposito:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:        
        print("\n @@@ Operação falhou! O valor informado é inválido! @@@")

    return saldo, extrato


def sacar(*, saldo, valor_saque, extrato, numero_saques, limite, LIMITE_SAQUES):

    if numero_saques < LIMITE_SAQUES:
            excedeu_saldo = valor_saque > saldo
            excedeu_limite = valor_saque > limite

            if excedeu_saldo:
                print("\n@@@ Operação falhou! Você não possui saldo suficiente. @@@")

            elif excedeu_limite:
                print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

            elif valor_saque > 0:
                saldo -= valor_saque
                extrato += f"Saque: \t\tR$ {valor_saque:.2f}\n"
                numero_saques += 1
                print("\n=== Saque realizado com sucesso! ===")

            else:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    else:
            print("\n@@@ Operação falhou! Limite de saques diários excedidos! @@@")
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print(" Extrato ".center(38, "="))
    print(f"Não foram realizadas movimentações.\n{extrato}" if not extrato else extrato)
    print(f"\nSaldo atual: \tR$ {saldo:.2f}")
    print("".center(38, "="))


def cadastrar_usuario(usuarios):
    cpf = input("Informe o seu CPF: ")
    cpf_valido = verificar_cpf_valido(cpf)
    if cpf_valido:
        usuario = filtrar_usuario(cpf, usuarios)
        
        if usuario:
            print("Já existe um usuário com este CPF!".center(42, "-"))
            return

        nome = input("Informe o seu nome completo: ")
        data_nascimento = input("Informe a sua data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco })

        print("\n" + " Usuário criado com sucesso! ".center(35, "="))
    else: 
        print("Operação falhou! Insira um CPF válido!")
        

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios, contas):   
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n" + " Conta criada com sucesso! ".center(27, "="))
        #retorno da criação de contas
        contas = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        return contas
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def verificar_cpf_valido(cpf):
        tamanho_cpf = len(cpf)
        if tamanho_cpf == 11:
            return True
        else:
            return False


def verificar_cpf_existente(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False


def listar_contas_por_cpf(cpf, contas):
    contas_usuario = []
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf:
            contas_usuario.append(conta)
    return contas_usuario


def listar_contas(contas, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    
    if verificar_cpf_existente(cpf, usuarios):
        contas_usuario = listar_contas_por_cpf(cpf, contas)
        
        if contas_usuario:
            print("".center(38, "="))
            print(f"\nContas associadas ao CPF - {cpf}:")
            for conta in contas_usuario:
                linha = f"""\
                Agência:  {conta['agencia']}
                Conta Corrente:  {conta['numero_conta']}
                Titular:  {conta['usuario']['nome'].title()}
            """
                linha_organizada = '\n'.join(line.strip() for line in linha.split('\n'))
                print(linha_organizada)
                print("".center(38, "="))
        else:
            print("\nNenhuma conta encontrada para este CPF.")
    else:
        print("\nCPF não encontrado.")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        try:
            opcao = menu()

            if opcao == 1:
                valor = float(input("Informe o valor para depósito: "))

                saldo, extrato = depositar(saldo, valor, extrato )
                #funcao deposito

            elif opcao == 2:
                valor_saque = float(input("Informe o valor para saque: "))
                
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor_saque = valor_saque,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    LIMITE_SAQUES=LIMITE_SAQUES,  
                )
                #funcao saque

            elif opcao == 3:
                exibir_extrato(saldo, extrato=extrato)
                #funcao extrato

            elif opcao == 4:
                cadastrar_usuario(usuarios)
                #funcao cadastrar cliente

            elif opcao == 5:
                numero_conta = len(contas) + 1 
                conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)

                if conta:
                    contas.append(conta)
                #funcao cadastrar conta

            elif opcao == 6:
                listar_contas(contas, usuarios)
            
            elif opcao == 7:
                break

            else:
                print("Opção inválida, por favor selecione novamente a operação desejada.")

        except ValueError:
                print("Operação falhou! Por favor tente novamente!")


main()