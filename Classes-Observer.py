from abc import ABC, abstractmethod

# Classe Observador (Interface)
class Observador(ABC):
    @abstractmethod
    def atualizar(self, mensagem):
        pass  # Método abstrato, deve ser implementado pelas subclasses


# Classe Sujeito
class Sujeito:
    def __init__(self):
        self.__observadores = []  # Lista de observadores
        self.__estado = None  # Estado do sujeito

    # Adiciona um observador à lista
    def adicionar_observador(self, observador):
        self.__observadores.append(observador)

    # Remove um observador da lista
    def remover_observador(self, observador):
        self.__observadores.remove(observador)

    # Notifica todos os observadores
    def notificar_observadores(self, mensagem):
        for observador in self.__observadores:
            observador.atualizar(mensagem)

    # Altera o estado e notifica os observadores
    def alterar_estado(self, novo_estado):
        self.__estado = novo_estado
        self.notificar_observadores(f"Estado alterado para: {self.__estado}")


# Classe ObservadorConcreto
class ObservadorConcreto(Observador):
    def __init__(self, nome):
        self.nome = nome

    # Implementação do método atualizar
    def atualizar(self, mensagem):
        print(f"{self.nome} recebeu a notificação: {mensagem}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando o sujeito
    sujeito = Sujeito()

    # Criando observadores
    observador1 = ObservadorConcreto(nome="Observador 1")
    observador2 = ObservadorConcreto(nome="Observador 2")
    observador3 = ObservadorConcreto(nome="Observador 3")

    # Adicionando observadores ao sujeito
    sujeito.adicionar_observador(observador1)
    sujeito.adicionar_observador(observador2)
    sujeito.adicionar_observador(observador3)

    # Alterando o estado do sujeito (os observadores são notificados)
    sujeito.alterar_estado("Estado 1")
    # Saída:
    # Observador 1 recebeu a notificação: Estado alterado para: Estado 1
    # Observador 2 recebeu a notificação: Estado alterado para: Estado 1
    # Observador 3 recebeu a notificação: Estado alterado para: Estado 1

    # Removendo um observador
    sujeito.remover_observador(observador2)

    # Alterando o estado novamente (apenas observadores restantes são notificados)
    sujeito.alterar_estado("Estado 2")
    # Saída:
    # Observador 1 recebeu a notificação: Estado alterado para: Estado 2
    # Observador 3 recebeu a notificação: Estado alterado para: Estado 2