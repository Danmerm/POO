# Classe base Animal
class Animal:
    def fazer_som(self):
        raise NotImplementedError("Subclasses devem implementar este método.")


# Classe derivada Cachorro
class Cachorro(Animal):
    def fazer_som(self):
        return "Au Au!"


# Classe derivada Gato
class Gato(Animal):
    def fazer_som(self):
        return "Miau!"


# Classe derivada Pato
class Pato(Animal):
    def fazer_som(self):
        return "Quack Quack!"
    
# Classe derivada Vaca
class Vaca(Animal):
    def fazer_som(self):
        return "Mu Mu!" 

# Classe derivada Vaca
class Galo(Animal):
    def fazer_som(self):
        return "Co co ri co!"    


# Função para demonstrar polimorfismo
def ouvir_som(animal):
    print(animal.fazer_som())


# Exemplo de uso
if __name__ == "__main__":
    # Criando objetos das classes derivadas
    cachorro = Cachorro()
    gato = Gato()
    pato = Pato()
    vaca = Vaca()
    galo = Galo()

    # Usando polimorfismo para tratar objetos de diferentes classes de forma uniforme
    ouvir_som(cachorro)  # Saída: Au Au!
    ouvir_som(gato)      # Saída: Miau!
    ouvir_som(pato)      # Saída: Quack Quack!
    ouvir_som(vaca)      # Saída: Mu Mu!
    ouvir_som(galo)      # Saída: Co co ri co!

    # Armazenando objetos em uma lista e iterando sobre eles
    animais = [cachorro, gato, pato, vaca, galo]
    for animal in animais:
        ouvir_som(animal)