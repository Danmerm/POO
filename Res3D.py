import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import Conversor_Unidades as con

class ReservoirSimulator:
    def __init__(self):
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.dx = None
        self.dy = None
        self.dz = None
        self.kx = None
        self.ky = None
        self.kz = None
        self.pres = None
        self.por_ref = None
        self.pref = 0.0
        self.visref = 0.0
        self.rhoref = 0.0
        self.compf = 0.0
        self.compr = 0.0
        self.vispr = 0.0
        self.wells = []
        self.time_step = 0.0
        self.total_time = 0.0
        self.current_time = 0.0
        self.pressure_history = []
        
    def read_input(self, input_file):
        # Implementar a leitura do arquivo de entrada
        # Esta função deve ler os dados de entrada conforme especificado
        pass
    
    def initialize(self, nx, ny, nz, dx, dy, dz, kx, ky, kz, pres, por, por_ref, 
                   pref, visref, rhoref, compf, compr, vispr):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.dx = np.array(dx)
        self.dy = np.array(dy)
        self.dz = np.array(dz)
        self.kx = np.array(kx).reshape((nx, ny, nz))
        self.ky = np.array(ky).reshape((nx, ny, nz))
        self.kz = np.array(kz).reshape((nx, ny, nz))
        self.pres = np.array(pres).reshape((nx, ny, nz))
        self.por = np.array(por).reshape((nx, ny, nz))
        self.pref = pref
        self.por_ref = por_ref
        self.visref = visref
        self.rhoref = rhoref
        self.compf = compf
        self.compr = compr
        self.vispr = vispr
        
    def add_well(self, well_type, radius, i, j, k, control_type, control_value):
        well = {
            'type': well_type,
            'radius': radius,
            'i': i-1,  # Convertendo para índice 0-based
            'j': j-1,
            'k': k-1,
            'control_type': control_type,
            'control_value': control_value,
            'flow_rate': 0.0
        }
        self.wells.append(well)
        
    def set_time_parameters(self, time_step, total_time):
        self.time_step = time_step
        self.total_time = total_time
        self.current_time = 0.0
        
    def calculate_transmissibilities(self):
        # Calcula as transmissibilidades entre células vizinhas
        tx = np.zeros((self.nx+1, self.ny, self.nz))
        ty = np.zeros((self.nx, self.ny+1, self.nz))
        tz = np.zeros((self.nx, self.ny, self.nz+1))
        
        # Transmissibilidades na direção x
        for i in range(1, self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    dx_avg = 0.5 * (self.dx[i-1] + self.dx[i])
                    kx_avg = 2 * self.kx[i-1,j,k] * self.kx[i,j,k] / (self.kx[i-1,j,k] + self.kx[i,j,k] + 0*1e-20)
                    area = self.dy[j] * self.dz[k]
                    tx[i,j,k] = kx_avg * area / dx_avg
                    
        # Transmissibilidades na direção y
        for i in range(self.nx):
            for j in range(1, self.ny):
                for k in range(self.nz):
                    dy_avg = 0.5 * (self.dy[j-1] + self.dy[j])
                    ky_avg = 2 * self.ky[i,j-1,k] * self.ky[i,j,k] / (self.ky[i,j-1,k] + self.ky[i,j,k] + 0*1e-20)
                    area = self.dx[i] * self.dz[k]
                    ty[i,j,k] = ky_avg * area / dy_avg
                    
        # Transmissibilidades na direção z
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(1, self.nz):
                    dz_avg = 0.5 * (self.dz[k-1] + self.dz[k])
                    kz_avg = 2 * self.kz[i,j,k-1] * self.kz[i,j,k] / (self.kz[i,j,k-1] + self.kz[i,j,k] + 0*1e-20)
                    area = self.dx[i] * self.dy[j]
                    tz[i,j,k] = kz_avg * area / dz_avg
                    
        return tx, ty, tz
        
    def calculate_well_index(self, well):
        # Calcula o índice de produtividade do poço (Peaceman)
        i = well['i']
        j = well['j']
        k = well['k']
        
        rw = well['radius']
        kx = self.kx[i,j,k]
        ky = self.ky[i,j,k]
        kz = self.kz[i,j,k]
        
        dx = self.dx[i]
        dy = self.dy[j]
        dz = self.dz[k]
        
        req = 0.28 * np.sqrt(np.sqrt(ky/kx)*dx**2 + np.sqrt(kx/ky)*dy**2) / ((ky/kx)**0.25 + (kx/ky)**0.25)
        skin = 0  # Assumindo skin factor zero
        wi = 2 * np.pi * np.sqrt(kx * ky) * dz / (np.log(req/rw) + skin)  # Skin = 0
        
        return wi
        
    def update_properties(self, pressure):
        # Atualiza propriedades dependentes da pressão
        porosity = self.por_ref * (1.0 + self.compr * (pressure - self.pref))
        viscosity = self.visref * (1.0 + self.vispr * (pressure - self.pref))
        density = self.rhoref * (1.0 + self.compf * (pressure - self.pref))
        
        return porosity, viscosity, density
        
    def assemble_system(self, pressure_old, dt):
        n_cells = self.nx * self.ny * self.nz
        A = lil_matrix((n_cells, n_cells))
        b = np.zeros(n_cells)
        
        tx, ty, tz = self.calculate_transmissibilities()
        
        # Pré-calcula propriedades nas células
        porosity_old, viscosity_old, density_old = self.update_properties(pressure_old)
        # porosity, viscosity, density = self.update_properties(pres)
        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    idx = i + j*self.nx + k*self.nx*self.ny
                    
                    # # Termo acumulativo
                    # # porosity, viscosity, density = self.update_properties(pres[i,j,k])
                    # vol = self.dx[i] * self.dy[j] * self.dz[k]
                    # # accum = vol * porosity[i,j,k] * density[i,j,k] / (viscosity[i,j,k])
                    # accum = vol * porosity[i,j,k] * density[i,j,k] / (viscosity[i,j,k])
                    # accum_old = vol * porosity_old[i,j,k] * density_old[i,j,k] / (viscosity_old[i,j,k])
                    
                    porosity, viscosity, density = self.update_properties(pres)
                    vol = self.dx[i] * self.dy[j] * self.dz[k]
                    accum = vol * porosity * density / (viscosity)
                    accum_old = vol * porosity_old[i,j,k] * density_old[i,j,k] / (viscosity_old[i,j,k])
                    
                    A[idx, idx] = 0*(accum[i,j,k] - accum_old) / dt
                    b[idx] = 0.0
                    
                    # # Geometria da célula
                    # vol = self.dx[i] * self.dy[j] * self.dz[k]
                    
                    # # Termo acumulativo (avaliado no tempo antigo para o vetor b)
                    # accum_old = vol * porosity_old[i,j,k] * density_old[i,j,k] / viscosity_old[i,j,k]
                    
                    # # O termo acumulativo no tempo presente será tratado implicitamente
                    # # através da derivada das propriedades em relação à pressão
                    
                    # # Coeficientes para a linearização do termo acumulativo
                    # p = pressure_old[i,j,k]  # Pressão de referência para linearização
                    
                    # # Derivadas das propriedades em relação à pressão
                    # dphi_dp = self.por_ref * self.compr
                    # drho_dp = self.rhoref * self.compf
                    # dmu_dp = self.visref * self.vispr
                    
                    # # Termos da expansão em série de Taylor
                    # phi = self.por_ref * (1.0 + self.compr * (p - self.pref))
                    # rho = self.rhoref * (1.0 + self.compf * (p - self.pref))
                    # mu = self.visref * (1.0 + self.vispr * (p - self.pref))
                    
                    # # Derivada do termo acumulativo em relação à pressão
                    # daccum_dp = vol * (
                    #     (dphi_dp * rho / mu) + 
                    #     (phi * drho_dp / mu) - 
                    #     (phi * rho * dmu_dp / (mu**2)))
                    
                    # # Termo acumulativo linearizado
                    # A[idx, idx] = daccum_dp / dt
                    # b[idx] = accum_old / dt  # Termo fonte do passo anterior

                    # Termos de fluxo
                    # Direção x
                    if i > 0:
                        idx_neighbor = (i-1) + j*self.nx + k*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i-1,j,k])
                        density_avg = 0.5 * (density[i,j,k] + density[i-1,j,k])
                        trans = tx[i,j,k] / viscosity_avg #tx[i,j,k] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira esquerda (i=0) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira
                        
                    if i < self.nx-1:
                        idx_neighbor = (i+1) + j*self.nx + k*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i+1,j,k])
                        density_avg = 0.5 * (density[i,j,k] + density[i+1,j,k])
                        trans = tx[i+1,j,k] / viscosity_avg#tx[i+1,j,k] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira direita (i=nx-1) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira

                    # Direção y
                    if j > 0:
                        idx_neighbor = i + (j-1)*self.nx + k*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i,j-1,k])
                        density_avg = 0.5 * (density[i,j,k] + density[i,j-1,k])
                        trans = ty[i,j,k] / viscosity_avg #ty[i,j,k] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira inferior (j=0) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira
                        
                    if j < self.ny-1:
                        idx_neighbor = i + (j+1)*self.nx + k*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i,j+1,k])
                        density_avg = 0.5 * (density[i,j,k] + density[i,j+1,k])
                        trans = ty[i,j+1,k] / viscosity_avg #ty[i,j+1,k] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira superior (j=ny-1) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira
                        
                    # Direção z
                    if k > 0:
                        idx_neighbor = i + j*self.nx + (k-1)*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i,j,k-1])
                        density_avg = 0.5 * (density[i,j,k] + density[i,j,k-1])
                        trans = tz[i,j,k] / viscosity_avg #tz[i,j,k] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira inferior (k=0) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira

                    if k < self.nz-1:
                        idx_neighbor = i + j*self.nx + (k+1)*self.nx*self.ny
                        viscosity_avg = 0.5 * (viscosity[i,j,k] + viscosity[i,j,k+1])
                        density_avg = 0.5 * (density[i,j,k] + density[i,j,k+1])
                        trans = tz[i,j,k+1] / viscosity_avg #tz[i,j,k+1] * density_avg / viscosity_avg
                        
                        A[idx, idx] += trans
                        A[idx, idx_neighbor] -= trans
                    # Fronteira superior (k=nz-1) - condição de fronteira fechada
                    # Nada a fazer, pois não há fluxo através desta fronteira

        # Adiciona termos dos poços (tratados implicitamente)
        for well in self.wells:
            i = well['i']
            j = well['j']
            k = well['k']
            idx = i + j*self.nx + k*self.nx*self.ny
            
            wi = self.calculate_well_index(well)
            
            # if well['control_type'] == 'pressure':
            #     pwf = well['control_value']
            #     # Linearizado em torno da pressão atual
            #     p = pressure_old[i,j,k]
            #     rho = self.rhoref * (1.0 + self.compf * (p - self.pref))
            #     mu = self.visref * (1.0 + self.vispr * (p - self.pref))
            #     drho_dp = self.rhoref * self.compf
            #     dmu_dp = self.visref * self.vispr
                
            #     # Termo do poço linearizado
            #     bhp_term = wi * (rho / mu + (drho_dp * mu - rho * dmu_dp) / (mu**2) * (p - p))
            #     A[idx, idx] += bhp_term
            #     b[idx] += bhp_term * pwf
                
            # elif well['control_type'] == 'rate':
            #     q = well['control_value']
            #     if well['type'] == 'injector':
            #         q = -q  # Taxa negativa para injeção
                
            #     # Converter vazão superficial para condições de reservatório
            #     p = pressure_old[i,j,k]
            #     mu = self.visref * (1.0 + self.vispr * (p - self.pref))
            #     rho = self.rhoref * (1.0 + self.compf * (p - self.pref))
            #     q_res = q * mu / (rho * 24.0 * 3600.0)  # m3/dia para m3/s
            #     b[idx] += q_res
        # Adiciona termos dos poços
        for well in self.wells:
            i = well['i']
            j = well['j']
            k = well['k']
            idx = i + j*self.nx + k*self.nx*self.ny
            
            wi = self.calculate_well_index(well)
            viscosit_w = viscosity[i,j,k]
            density_w = density[i,j,k]
            
            if well['control_type'] == 'pressure':
                pwf = well['control_value']
                bhp_term = wi * density_w / viscosit_w
                
                A[idx, idx] += bhp_term
                b[idx] += bhp_term * pwf
                
            elif well['control_type'] == 'rate':
                q = well['control_value']
                if well['type'] == 'injector':
                    q = -q  # Taxa negativa para injeção
                
                # Converter vazão superficial para condições de reservatório
                q_res = q * viscosit_w / (density_w * 1.0/24.0/3600.0)  # m3/dia para m3/s
                b[idx] += q_res
        
        return csr_matrix(A), b
        
    def solve_time_step(self, dt):
        pressure_old = self.pres.copy()
        
        # Monta e resolve o sistema linear
        A, b = self.assemble_system(pressure_old, dt)
        pressure_new_flat = spsolve(A, b)
        
        # Atualiza a pressão no reservatório
        pressure_new = pressure_new_flat.reshape((self.nx, self.ny, self.nz))
        self.pres = pressure_new
        
        # Calcula vazões dos poços com controle de pressão
        self.update_well_flows(pressure_old, dt)
        
        self.current_time += dt
        self.pressure_history.append(self.pres.copy())
        
        return pressure_new
        
    def update_well_flows(self, pressure_old, dt):
        _, viscosity, density = self.update_properties(self.pres)
        
        for well in self.wells:
            i = well['i']
            j = well['j']
            k = well['k']
            
            wi = self.calculate_well_index(well)
            visc = viscosity[i,j,k]
            rho = density[i,j,k]
            
            if well['control_type'] == 'pressure':
                pwf = well['control_value']
                p_cell = self.pres[i,j,k]
                
                q = wi * rho / visc * (p_cell - pwf)
                well['flow_rate'] = q * (rho / visc * 24.0 * 3600.0)  # Converter para m3/dia
                
            elif well['control_type'] == 'rate':
                # Vazão já está especificada
                pass
        
    def run_simulation(self):
        num_steps = int(np.ceil(self.total_time / self.time_step))
        
        for step in range(num_steps):
            if self.current_time + self.time_step > self.total_time:
                dt = self.total_time - self.current_time
            else:
                dt = self.time_step
                
            print(f"Time step {step+1}: t = {self.current_time + dt:.2f} days")
            self.solve_time_step(dt)
            
    def plot_pressure_slice(self, k_layer, time_step=-1):
        plt.figure(figsize=(10, 8))
        plt.imshow(self.pressure_history[time_step][:,:,k_layer].T, origin='lower')
        plt.colorbar(label='Pressure (kPa)')
        plt.xlabel('I index')
        plt.ylabel('J index')
        plt.title(f'Pressure map at layer {k_layer+1}, time = {self.current_time:.2f} days')
        plt.show()

# Exemplo de uso do simulador
if __name__ == "__main__":
    # Criar instância do simulador
    simulator = ReservoirSimulator()
    
    # Definir parâmetros do reservatório (exemplo)
    nx, ny, nz = 4, 4, 1
    dx = np.full(nx, 20.0)  # 100m em x
    dy = np.full(ny, 20.0)  # 100m em y
    dz = np.full(nz, 10.0)   # 20m em z

    # Adicionar poços
    # simulator.add_well('producer', 0.1, 1, 1, 1, 'rate', 100.0)  # Produtor com BHP de 15000 kPa
    simulator.add_well('producer', 0.1, 4, 4, 1,'pressure', 12000.0) # Produtor com BHP de 15000 kPa
    simulator.add_well('injector', 0.1, 1, 1, 1, 'rate', 10.0)        # Injtor com 100 m3/dia

    #Conversão de unidades para o SI
    por_ref = 0.2
    pref = 20000.0    # kPa
    pref = con.Convert_kPa_to_Pa(pref)
    visref = 1.02      # cP
    visref= con.ConvertBtoI.viscosity(visref)   #De cP => Pa.s
    rhoref = 1000.0   # kg/m3
    compf = 1e-9      # 1e-6 1/kPa => 1/Pa
    compr = 1e-9      # 1e-6 1/kPa => 1/Pa
    vispr = 1e-7*1e-6      # 1e-7 cp/kPa

    #Dos poços
    for r in range(len(simulator.wells[:])):
        if simulator.wells[r]['control_type']=='rate':
            simulator.wells[r]['control_value']=con.ConvertBtoI.flow_rate(simulator.wells[r]['control_value']) 
        elif simulator.wells[r]['control_type']=='pressure':
            simulator.wells[r]['control_value']=con.Convert_kPa_to_Pa(simulator.wells[r]['control_value'])
        else:
            exit('Warning: Estratégia de controle do poço número ', r, 'não detetada')
        #Outras variáveis
    Permeabx = 250
    Perm_X=con.ConvertBtoI.permeability(Permeabx)    #De mD => m2
    Perm_Y=con.ConvertBtoI.permeability(Permeabx)
    Perm_Z=con.ConvertBtoI.permeability(Permeabx)
    #A densidade já está em SI e não é utilizada

    kx = ky = kz = np.full((nx, ny, nz), Perm_X)  # 100 mD em todas as direções
    pres = np.full((nx, ny, nz), pref)  # 20000 kPa inicial
    por = np.full((nx, ny, nz), por_ref)   # Porosidade de 20%
    
    # Inicializar simulador
    simulator.initialize(nx, ny, nz, dx, dy, dz, kx, ky, kz, pres, por, por_ref,
                        pref, visref, rhoref, compf, compr, vispr)
    
    # # Adicionar poços
    # simulator.add_well('producer', 0.1, 1, 1, 1, 'rate', 100.0)  # Produtor com BHP de 15000 kPa
    # simulator.add_well('injector', 0.1, 100, 100, 1, 'rate', 100.0)        # Injtor com 100 m3/dia
    
    # Configurar tempo de simulação
    simulator.set_time_parameters(time_step=1, total_time=10)  # 1 dia por passo, 10 dias total
    
    # Executar simulação
    simulator.run_simulation()
    
    # Plotar resultados
    simulator.plot_pressure_slice(0)  # Mostrar camada 3 (k=2 em 0-based)
    print('fim')