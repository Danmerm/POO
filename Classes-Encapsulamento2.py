class ContaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.__titular = titular  # Atributo privado
        self.__saldo = max(0, saldo_inicial)  # Garante que o saldo inicial não seja negativo

    # Getter para o titular
    @property
    def titular(self):
        return self.__titular

    # Setter para o titular
    @titular.setter
    def titular(self, novo_titular):
        if isinstance(novo_titular, str) and len(novo_titular) > 0:
            self.__titular = novo_titular
        else:
            print("Erro: O titular deve ser uma string não vazia.")

    # Getter para o saldo
    @property
    def saldo(self):
        return self.__saldo

    # Método para depositar dinheiro
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"Depósito de R${valor:.2f} realizado. Novo saldo: R${self.__saldo:.2f}")
        else:
            print("Erro: O valor do depósito deve ser positivo.")

    # Método para sacar dinheiro
    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            print(f"Saque de R${valor:.2f} realizado. Novo saldo: R${self.__saldo:.2f}")
        else:
            print("Erro: Valor de saque inválido ou saldo insuficiente.")

    # Método para exibir informações da conta
    def exibir_informacoes(self):
        print(f"Titular: {self.__titular}, Saldo: R${self.__saldo:.2f}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando uma conta bancária
    conta = ContaBancaria(titular="João Silva", saldo_inicial=100)

    # Exibindo informações iniciais
    conta.exibir_informacoes()  # Saída: Titular: João Silva, Saldo: R$100.00

    # Realizando operações
    conta.depositar(50)  # Saída: Depósito de R$50.00 realizado. Novo saldo: R$150.00
    conta.sacar(30)      # Saída: Saque de R$30.00 realizado. Novo saldo: R$120.00

    # Tentando sacar um valor maior que o saldo
    conta.sacar(200)     # Saída: Erro: Valor de saque inválido ou saldo insuficiente.

    # Tentando depositar um valor negativo
    conta.depositar(-10) # Saída: Erro: O valor do depósito deve ser positivo.
    
    # Realizando operações
    conta.depositar(50)  # Saída: Depósito de R$50.00 realizado. Novo saldo: R$150.00

    # Alterando o titular
    conta.titular = "Maria Oliveira"
    conta.exibir_informacoes()  # Saída: Titular: Maria Oliveira, Saldo: R$120.00

    # Tentando definir um titular inválido
    conta.titular = ""  # Saída: Erro: O titular deve ser uma string não vazia.