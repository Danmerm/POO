from abc import ABC, abstractmethod

# Classe base Funcionario
class Funcionario(ABC):
    def __init__(self, nome, salario_base):
        self.nome = nome
        self.salario_base = salario_base

    @abstractmethod
    def calcular_salario(self):
        pass  # Método abstrato, deve ser implementado pelas subclasses

    @abstractmethod
    def calcular_bonus(self):
        pass  # Método abstrato, deve ser implementado pelas subclasses


# Classe Gerente
class Gerente(Funcionario):
    def __init__(self, nome, salario_base, bonus_gerencia):
        super().__init__(nome, salario_base)
        self.bonus_gerencia = bonus_gerencia

    def calcular_salario(self):
        return self.salario_base + self.bonus_gerencia

    def calcular_bonus(self):
        return self.bonus_gerencia * 1.5  # Bônus adicional para gerentes


# Classe Estagiario
class Estagiario(Funcionario):
    def __init__(self, nome, salario_base):
        super().__init__(nome, salario_base)

    def calcular_salario(self):
        return self.salario_base  # Estagiários não recebem bônus

    def calcular_bonus(self):
        return 0  # Estagiários não recebem bônus


# Função para exibir informações dos funcionários
def exibir_informacoes(funcionario):
    print(f"Nome: {funcionario.nome}")
    print(f"Salário: R${funcionario.calcular_salario():.2f}")
    print(f"Bônus: R${funcionario.calcular_bonus():.2f}")
    print("-" * 30)


# Exemplo de uso
if __name__ == "__main__":
    # Criando funcionários
    gerente = Gerente(nome="João Silva", salario_base=10000, bonus_gerencia=2000)
    estagiario = Estagiario(nome="Maria Oliveira", salario_base=1500)

    # Exibindo informações dos funcionários
    exibir_informacoes(gerente)
    # Saída:
    # Nome: João Silva
    # Salário: R$12000.00
    # Bônus: R$3000.00
    # ------------------------------

    exibir_informacoes(estagiario)
    # Saída:
    # Nome: Maria Oliveira
    # Salário: R$1500.00
    # Bônus: R$0.00
    # ------------------------------

    # Armazenando funcionários em uma lista e iterando sobre eles
    funcionarios = [gerente, estagiario]
    for funcionario in funcionarios:
        exibir_informacoes(funcionario)