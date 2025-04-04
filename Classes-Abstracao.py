from abc import ABC, abstractmethod
import math

# Classe abstrata Forma
class Forma(ABC):
    @abstractmethod
    def calcular_area(self):
        pass  # Método abstrato, deve ser implementado pelas subclasses


# Classe Retangulo
class Retangulo(Forma):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura


# Classe Circulo
class Circulo(Forma):
    def __init__(self, raio):
        self.raio = raio

    def calcular_area(self):
        return math.pi * (self.raio ** 2)


# Classe Triangulo
class Triangulo(Forma):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return (self.base * self.altura) / 2
    
# Classe Regiao anular circular entre R2 e R1
class RegAnularCircular(Forma):
    def __init__(self, raio_1, raio_2):
        self.raio_1 = raio_1
        self.raio_2 = raio_2

    def calcular_area(self):
        return math.pi * (self.raio_2 ** 2-self.raio_1 ** 2)
    
# Classe Regiao anular circular entre R2 e R1
class Trapezio(Forma):
    def __init__(self, base_1, base_2, altura):
        self.base_1 = base_1
        self.base_2 = base_2
        self.altura = altura

    def calcular_area(self):
        return (self.base_1+self.base_2)* self.altura / 2

# Função para demonstrar polimorfismo
def exibir_area(forma):
    print(f"A área da forma é: {forma.calcular_area():.2f}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando objetos das classes derivadas
    retangulo = Retangulo(base=5, altura=10)
    circulo = Circulo(raio=7)
    triangulo = Triangulo(base=6, altura=8)
    regAnularCircular = RegAnularCircular(raio_1=3, raio_2=7)
    trapezio = Trapezio(base_1=6, base_2=3, altura=8)

    # Usando polimorfismo para tratar objetos de diferentes classes de forma uniforme
    exibir_area(retangulo)  # Saída: A área da forma é: 50.00
    exibir_area(circulo)    # Saída: A área da forma é: 153.94
    exibir_area(triangulo)  # Saída: A área da forma é: 24.00
    exibir_area(regAnularCircular)  # Saída: A área da forma é: 125.66
    exibir_area(trapezio)  # Saída: A área da forma é: 36.00

    # Armazenando objetos em uma lista e iterando sobre eles
    formas = [retangulo, circulo, triangulo, regAnularCircular, trapezio]
    for forma in formas:
        exibir_area(forma)