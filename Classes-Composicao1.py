# Classe Autor
class Autor:
    def __init__(self, nome, nacionalidade):
        self.nome = nome
        self.nacionalidade = nacionalidade

    def __str__(self):
        return f"{self.nome} ({self.nacionalidade})"


# Classe Livro
class Livro:
    def __init__(self, titulo, ano_publicacao, autor):
        self.titulo = titulo
        self.ano_publicacao = ano_publicacao
        self.autor = autor  # Composição: Livro tem um Autor

    def __str__(self):
        return f"'{self.titulo}' por {self.autor} ({self.ano_publicacao})"


# Classe Biblioteca
class Biblioteca:
    def __init__(self):
        self.livros = []  # Lista para armazenar os livros

    def adicionar_livro(self, livro):
        self.livros.append(livro)

    def listar_livros(self):
        if not self.livros:
            print("A biblioteca está vazia.")
        else:
            print("Livros na biblioteca:")
            for livro in self.livros:
                print(livro)

    def buscar_livros_por_autor(self, nome_autor):
        livros_autor = [livro for livro in self.livros if livro.autor.nome == nome_autor]
        if livros_autor:
            print(f"Livros do autor {nome_autor}:")
            for livro in livros_autor:
                print(livro)
        else:
            print(f"Nenhum livro encontrado para o autor {nome_autor}.")


# Exemplo de uso
if __name__ == "__main__":
    # Criando autores
    autor1 = Autor(nome="Machado de Assis", nacionalidade="Brasileiro")
    autor2 = Autor(nome="George Orwell", nacionalidade="Britânico")
    autor3 = Autor(nome="Mario V. Llosa", nacionalidade="Peruano")
    autor4 = Autor(nome="Gabriel Garcia Marques", nacionalidade="Colombiano")

    # Criando livros
    livro1 = Livro(titulo="Dom Casmurro", ano_publicacao=1899, autor=autor1)
    livro2 = Livro(titulo="1984", ano_publicacao=1949, autor=autor2)
    livro3 = Livro(titulo="Memórias Póstumas de Brás Cubas", ano_publicacao=1881, autor=autor1)
    livro4 = Livro(titulo="La tia Julia y el escribidor", ano_publicacao=1977, autor=autor3)
    livro5 = Livro(titulo="Cem anos de solidao", ano_publicacao=1967, autor=autor4)

    # Criando a biblioteca e adicionando livros
    biblioteca = Biblioteca()
    biblioteca.adicionar_livro(livro1)
    biblioteca.adicionar_livro(livro2)
    biblioteca.adicionar_livro(livro3)
    biblioteca.adicionar_livro(livro4)
    biblioteca.adicionar_livro(livro5)

    # Listando todos os livros na biblioteca
    biblioteca.listar_livros()

    # Buscando livros por autor
    biblioteca.buscar_livros_por_autor("Machado de Assis")
    biblioteca.buscar_livros_por_autor("George Orwell")
    biblioteca.buscar_livros_por_autor("Mario V. Llosa")
    biblioteca.buscar_livros_por_autor("Gabriel Garcia Marques")
    biblioteca.buscar_livros_por_autor("J.K. Rowling")  # Autor não existente