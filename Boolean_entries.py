import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Mesh:
    def __init__(self):
        self.dim = 0
        self.totnds = 0
        self.nds = None

def gen_gridpnts3d(n, p, ln):
    """
    Generate 3D grid points

    Parameters:
    n : list or numpy array
        Number of points in each dimension [nx, ny, nz]
    p : list or numpy array
        Starting point coordinates [x, y, z]
    ln : list or numpy array
        Length of the grid in each dimension [lx, ly, lz]

    Returns:
    msh : Mesh
        Mesh object containing the grid points
    """
    msh = Mesh()
    
    msh.dim = 3
    dx = ln[0] / (n[0] - 1)
    dy = ln[1] / (n[1] - 1)
    dz = ln[2] / (n[2] - 1)
    msh.totnds = n[0] * n[1] * n[2]

    tmp = np.zeros((msh.totnds + 1, 3))
    tmp[0] = p

    l = 0
    for k in range(n[2]):
        for j in range(n[2]):
            for i in range(n[0]):
                tmp[l+1, 0] = tmp[l, 0] + dx
                tmp[l+1, 1] = tmp[l, 1]
                tmp[l+1, 2] = tmp[l, 2]
                l += 1
            tmp[l, 0] = tmp[0, 0]
            tmp[l, 1] = tmp[l, 1] + dy
            tmp[l, 2] = tmp[l, 2]
        tmp[l, 0] = p[0]
        tmp[l, 1] = p[1]
        tmp[l, 2] = tmp[l, 2] + dz

    msh.nds = tmp[:msh.totnds]

    print(f"totnds = {msh.totnds}")

    return msh

def plot_3d_grid(mesh):
    """
    Plot the 3D grid points
    
    Parameters:
    mesh : Mesh
        Mesh object containing the grid points
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x = mesh.nds[:, 0]
    y = mesh.nds[:, 1]
    z = mesh.nds[:, 2]
    
    ax.scatter(x, y, z, c='b', marker='o', s=10)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Grid Points')
    
    plt.tight_layout()
    plt.show()


# Exemplo de uso:
n = [10, 10, 10]  # número de pontos em cada dimensão
p = [0, 0, 0]     # ponto inicial
ln = [1, 1, 1]    # comprimento em cada dimensão

mesh = gen_gridpnts3d(n, p, ln)
print(f"Shape of the grid: {mesh.nds.shape}")
print("First 5 points:")
print(mesh.nds[:5])

# Plotar o gráfico 3D
plot_3d_grid(mesh)
print('O valor booleano de')

# # Função para converter a Ks do usuário em um valor booleano
# def str_to_bool(valor):
#     return valor.lower() in ('sim', 's', 'true', 't', '1', 'yes', 'y')

# # Exemplo de uso
# j = 0  # Supondo que j seja o índice da camada
# Bool = input(f"Digite 'sim' ou 'não' para casos com Skin {j+1} (True/False): ")

# # Convertendo a Ks_Bool para booleano
# Ks_Bool = str_to_bool(Bool)

# # Exibindo o resultado
# print(f"O valor booleano de Phi para a camada {j+1} é: {Ks_Bool}")