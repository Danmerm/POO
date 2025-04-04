# Função para converter a Ks do usuário em um valor booleano
def str_to_bool(valor):
    return valor.lower() in ('sim', 's', 'true', 't', '1', 'yes', 'y')

# Exemplo de uso
j = 0  # Supondo que j seja o índice da camada
Bool = input(f"Digite 'sim' ou 'não' para casos com Skin {j+1} (True/False): ")

# Convertendo a Ks_Bool para booleano
Ks_Bool = str_to_bool(Bool)

# Exibindo o resultado
print(f"O valor booleano de Phi para a camada {j+1} é: {Ks_Bool}")