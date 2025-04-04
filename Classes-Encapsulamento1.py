class Pessoa:
    def __init__(self, nome, idade, cpf):
        self.__nome = nome  # Atributo privado
        self.__idade = idade  # Atributo privado
        self.__cpf = cpf  # Atributo privado

    # Getter para o atributo nome
    @property
    def nome(self):
        return self.__nome

    # Setter para o atributo nome
    @nome.setter
    def nome(self, novo_nome):
        if isinstance(novo_nome, str) and len(novo_nome) > 0:
            self.__nome = novo_nome
        else:
            print("Erro: Nome inválido.")

    # Getter para o atributo idade
    @property
    def idade(self):
        return self.__idade

    # Setter para o atributo idade
    @idade.setter
    def idade(self, nova_idade):
        if isinstance(nova_idade, int) and nova_idade > 0:
            self.__idade = nova_idade
        else:
            print("Erro: Idade inválida.")

    # Getter para o atributo cpf
    @property
    def cpf(self):
        return self.__cpf

    # Setter para o atributo cpf
    @cpf.setter
    def cpf(self, novo_cpf):
        if isinstance(novo_cpf, str) and len(novo_cpf) == 11:  # CPF deve ter 11 dígitos
            self.__cpf = novo_cpf
        else:
            print("Erro: CPF inválido.")

    # Método para exibir informações da pessoa
    def exibir_informacoes(self):
        print(f"Nome: {self.__nome}, Idade: {self.__idade}, CPF: {self.__cpf}")


# Exemplo de uso da classe Pessoa
pessoa1 = Pessoa(nome="João Silva", idade=30, cpf="12345678901")
pessoa1.exibir_informacoes() # Exibindo informações atualizadas

# Acessando atributos usando getters
print("Nome:", pessoa1.nome)  # Saída: João Silva
print("Idade:", pessoa1.idade)  # Saída: 30
print("CPF:", pessoa1.cpf)  # Saída: 12345678901

# Modificando atributos usando setters
pessoa1.nome = "Maria Oliveira"  # Nome válido
pessoa1.idade = 25  # Idade válida
pessoa1.cpf = "98765432100"  # CPF válido
pessoa1.exibir_informacoes() # Exibindo informações atualizadas Maria Oliveira, Idade: 25, CPF: 98765432100

# Tentando atribuir valores inválidos
pessoa1.nome = ""  # Erro: Nome inválido.
pessoa1.idade = -5  # Erro: Idade inválida.
pessoa1.cpf = "123"  # Erro: CPF inválido.
pessoa1.exibir_informacoes() # Exibindo informações atualizadas