from abc import ABC, abstractmethod

# Classe base Personagem
class Personagem(ABC):
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa

    @abstractmethod
    def atacar(self, inimigo):
        pass  # Método abstrato, deve ser implementado pelas subclasses

    @abstractmethod
    def receber_dano(self, dano):
        pass  # Método abstrato, deve ser implementado pelas subclasses

    def esta_vivo(self):
        return self.vida > 0

    def __str__(self):
        return f"{self.nome} (Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa})"


# Classe Guerreiro
class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=100, ataque=20, defesa=15)

    def atacar(self, inimigo):
        print(f"{self.nome} ataca com sua espada!")
        dano = self.ataque - inimigo.defesa
        if dano > 0:
            inimigo.receber_dano(dano)
        else:
            print(f"{inimigo.nome} defendeu o ataque!")

    def receber_dano(self, dano):
        self.vida -= dano
        print(f"{self.nome} recebeu {dano} de dano e agora tem {self.vida} de vida.")

    def habilidade_especial(self):
        print(f"{self.nome} usa Fúria do Guerreiro! Ataque aumentado em 10!")
        self.ataque += 10


# Classe Mago
class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=80, ataque=25, defesa=10)

    def atacar(self, inimigo):
        print(f"{self.nome} lança uma bola de fogo!")
        dano = self.ataque - inimigo.defesa
        if dano > 0:
            inimigo.receber_dano(dano)
        else:
            print(f"{inimigo.nome} defendeu o ataque!")

    def receber_dano(self, dano):
        self.vida -= dano
        print(f"{self.nome} recebeu {dano} de dano e agora tem {self.vida} de vida.")

    def habilidade_especial(self):
        print(f"{self.nome} usa Cura Mágica! Vida restaurada em 20!")
        self.vida += 20


# Função para simular uma batalha
def batalha(personagem1, personagem2):
    print("=== Início da Batalha ===")
    turno = 10

    while personagem1.esta_vivo() and personagem2.esta_vivo():
        print(f"\nTurno {turno}:")
        print(personagem1)
        print(personagem2)

        # Personagem 1 ataca
        personagem1.atacar(personagem2)
        if not personagem2.esta_vivo():
            break

        # Personagem 2 ataca
        personagem2.atacar(personagem1)
        if not personagem1.esta_vivo():
            break

        # Habilidades especiais
        if turno % 3 == 0:  # Usar habilidade especial a cada 3 turnos
            personagem1.habilidade_especial()
            personagem2.habilidade_especial()

        turno += 1

    # Resultado da batalha
    if personagem1.esta_vivo():
        print(f"\n{personagem1.nome} venceu a batalha!")
    else:
        print(f"\n{personagem2.nome} venceu a batalha!")


# Exemplo de uso
if __name__ == "__main__":
    # Criando personagens
    guerreiro = Guerreiro(nome="Conan")
    mago = Mago(nome="Gandalf")

    # Iniciando a batalha
    batalha(guerreiro, mago)