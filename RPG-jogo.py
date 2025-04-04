from abc import ABC, abstractmethod
import random

# Classe base para Personagem
"""class Personagem(ABC):
    def __init__(self, nome, vida, mana, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.ataque = ataque
        self.defesa = defesa
        self.nivel = 1
        self.experiencia = 0

    @abstractmethod
    def usar_habilidade(self, inimigo):
        pass  # Método abstrato, deve ser implementado pelas subclasses

    def receber_dano(self, dano):
        dano_final = max(0, dano - self.defesa)  # Reduz o dano pela defesa
        self.vida -= dano_final
        print(f"{self.nome} recebeu {dano_final} de dano e agora tem {self.vida} de vida.")

    def esta_vivo(self):
        return self.vida > 0

    def __str__(self):
        return f"{self.nome} (Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa})" """""
from abc import ABC, abstractmethod

class Personagem(ABC):
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa

    @abstractmethod
    def atacar(self, alvo):
        pass

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
        print(f"{self.nome} recebeu {dano} de dano e agora tem {self.vida} de vida.")

    def esta_vivo(self):
        return self.vida > 0

    def __str__(self):
        return f"{self.nome} (Vida: {self.vida}, Ataque: {self.ataque}, Defesa: {self.defesa})"        

class Heroi(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=100, ataque=20, defesa=15)
        self.habilidades = []
        self.inventario = []

    def atacar(self, alvo):
        print(f"{self.nome} ataca {alvo.nome}!")
        dano = self.ataque - alvo.defesa
        if dano > 0:
            alvo.receber_dano(dano)
        else:
            print(f"{alvo.nome} defendeu o ataque!")

    def adicionar_habilidade(self, habilidade):
        self.habilidades.append(habilidade)

    def usar_habilidade(self, habilidade, alvo):
        if habilidade in self.habilidades:
            habilidade.usar(self, alvo)
        else:
            print(f"{self.nome} não conhece a habilidade {habilidade.nome}.")

    def adicionar_item(self, item):
        self.inventario.append(item)
        print(f"{self.nome} coletou {item.nome}.")

    def usar_item(self, item):
        if item in self.inventario:
            item.usar(self)
            self.inventario.remove(item)
        else:
            print(f"{self.nome} não possui {item.nome}.")

class Inimigo(Personagem):
    def __init__(self, nome, vida, ataque, defesa):
        super().__init__(nome, vida, ataque, defesa)

    def atacar(self, alvo):
        print(f"{self.nome} ataca {alvo.nome}!")
        dano = self.ataque - alvo.defesa
        if dano > 0:
            alvo.receber_dano(dano)
        else:
            print(f"{alvo.nome} defendeu o ataque!")

class Habilidade:
    def __init__(self, nome, custo_mana, dano):
        self.nome = nome
        self.custo_mana = custo_mana
        self.dano = dano

    def usar(self, usuario, alvo):
        if usuario.vida > 0:
            print(f"{usuario.nome} usou {self.nome} em {alvo.nome}!")
            alvo.receber_dano(self.dano)
        else:
            print(f"{usuario.nome} não pode usar habilidades enquanto estiver derrotado.")

class Item:
    def __init__(self, nome, efeito):
        self.nome = nome
        self.efeito = efeito

    def usar(self, alvo):
        self.efeito(alvo)
        print(f"{alvo.nome} usou {self.nome}.")

class Mundo:
    def __init__(self):
        self.heroi = None
        self.inimigos = []
        self.itens = []

    def adicionar_heroi(self, heroi):
        self.heroi = heroi

    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)

    def adicionar_item(self, item):
        self.itens.append(item)

    def iniciar_batalha(self):
        if not self.heroi:
            print("Nenhum herói no mundo.")
            return

        for inimigo in self.inimigos:
            while self.heroi.esta_vivo() and inimigo.esta_vivo():
                self.heroi.atacar(inimigo)
                if inimigo.esta_vivo():
                    inimigo.atacar(self.heroi)

            if not self.heroi.esta_vivo():
                print(f"{self.heroi.nome} foi derrotado!")
                break
            else:
                print(f"{inimigo.nome} foi derrotado!")

# Criando o mundo do jogo
mundo = Mundo()

# Criando o herói
heroi = Heroi(nome="Aragorn")
mundo.adicionar_heroi(heroi)

# Criando inimigos
inimigo1 = Inimigo(nome="Orc", vida=50, ataque=15, defesa=10)
inimigo2 = Inimigo(nome="Dragão", vida=200, ataque=30, defesa=20)
mundo.adicionar_inimigo(inimigo1)
mundo.adicionar_inimigo(inimigo2)

# Criando habilidades
habilidade_fogo = Habilidade(nome="Bola de Fogo", custo_mana=10, dano=25)
heroi.adicionar_habilidade(habilidade_fogo)

# Criando itens
pocao_vida = Item(nome="Poção de Vida", efeito=lambda p: setattr(p, 'vida', p.vida + 20))
mundo.adicionar_item(pocao_vida)

# Coletando itens
heroi.adicionar_item(pocao_vida)

# Usando itens
heroi.usar_item(pocao_vida)

# Iniciando a batalha
mundo.iniciar_batalha()