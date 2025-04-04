# Classe Produto
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome  # Nome do produto
        self.preco = preco  # Preço do produto

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}"


# Classe Cliente
class Cliente:
    def __init__(self, nome, email):
        self.nome = nome  # Nome do cliente
        self.email = email  # Email do cliente

    def __str__(self):
        return f"Cliente: {self.nome} (Email: {self.email})"


# Classe Pedido
class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente  # Composição: Pedido tem um Cliente
        self.produtos = []  # Lista de produtos no pedido

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def calcular_total(self):
        return sum(produto.preco for produto in self.produtos)

    def __str__(self):
        produtos_str = "\n".join(f"  {produto}" for produto in self.produtos)
        return (f"Pedido de {self.cliente.nome}:\n"
                f"{produtos_str}\n"
                f"Total: R${self.calcular_total():.2f}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando produtos
    produto1 = Produto(nome="Notebook", preco=3500.0)
    produto2 = Produto(nome="Mouse", preco=50.0)
    produto3 = Produto(nome="Teclado", preco=150.0)

    # Criando cliente
    cliente = Cliente(nome="João Silva", email="joao.silva@example.com")

    # Criando pedido e adicionando produtos
    pedido = Pedido(cliente=cliente)
    pedido.adicionar_produto(produto1)
    pedido.adicionar_produto(produto2)
    pedido.adicionar_produto(produto3)
    pedido.adicionar_produto(produto2)
    # Exibindo o pedido
    print(pedido)

    # Criando cliente
    cliente = Cliente(nome="Maria Cavalcanti", email="maria.cavalcanti@example.com")

    # Criando pedido e adicionando produtos
    pedido = Pedido(cliente=cliente)
    pedido.adicionar_produto(produto1)
    pedido.adicionar_produto(produto1)
    pedido.adicionar_produto(produto2)
    pedido.adicionar_produto(produto3)

    # Exibindo o pedido
    print(pedido)