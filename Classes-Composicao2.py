# Classe Quarto
class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero  # Número do quarto
        self.tipo = tipo  # Tipo do quarto (ex: Single, Duplo, Suíte)
        self.preco_diaria = preco_diaria  # Preço da diária
        self.reservado = False  # Status de reserva

    def __str__(self):
        status = "Reservado" if self.reservado else "Disponível"
        return f"Quarto {self.numero} ({self.tipo}) - R${self.preco_diaria:.2f}/noite - {status}"


# Classe Cliente
class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome  # Nome do cliente
        self.cpf = cpf  # CPF do cliente

    def __str__(self):
        return f"Cliente: {self.nome} (CPF: {self.cpf})"


# Classe Reserva
class Reserva:
    def __init__(self, cliente, quarto, dias):
        self.cliente = cliente  # Composição: Reserva tem um Cliente
        self.quarto = quarto  # Composição: Reserva tem um Quarto
        self.dias = dias  # Número de dias da reserva
        self.quarto.reservado = True  # Marca o quarto como reservado

    def calcular_total(self):
        return self.dias * self.quarto.preco_diaria

    def __str__(self):
        return (f"Reserva para {self.cliente.nome}:\n"
                f"  Quarto: {self.quarto.numero} ({self.quarto.tipo})\n"
                f"  Diárias: {self.dias} dias\n"
                f"  Total: R${self.calcular_total():.2f}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando quartos
    quarto1 = Quarto(numero=101, tipo="Single", preco_diaria=150.0)
    quarto2 = Quarto(numero=202, tipo="Duplo", preco_diaria=250.0)

    # Criando clientes
    cliente1 = Cliente(nome="João Silva", cpf="123.456.789-00")
    cliente2 = Cliente(nome="Maria Oliveira", cpf="987.654.321-00")

    # Exibindo quartos disponíveis
    print("Quartos disponíveis:")
    print(quarto1)
    print(quarto2)
    print("-" * 30)

    # Fazendo reservas
    reserva1 = Reserva(cliente=cliente1, quarto=quarto1, dias=3)
    reserva2 = Reserva(cliente=cliente2, quarto=quarto2, dias=5)

    # Exibindo reservas
    print(reserva1)
    print("-" * 30)
    print(reserva2)
    print("-" * 30)

    # Exibindo status dos quartos após as reservas
    print("Status dos quartos após as reservas:")
    print(quarto1)
    print(quarto2)