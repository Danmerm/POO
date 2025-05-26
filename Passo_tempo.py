import numpy as np
import matplotlib.pyplot as plt

# Input data
well_flowrate = [0.,3000,1500,0.,3000,0.,3000,0.,3000,0.] #[100, 200, 150]  # m³/d
Period_Q = [8,5,5,5,10,15,0.1,0.1,0.2,0.1] #[15, 15, 5]  # days
Dt_max = 10 * 24 * 3600  # seconds (maximum time step)
transition_duration = 0.05 * 24 * 3600  # 2 days transition in seconds

# Calculate cumulative days
Days = np.cumsum(Period_Q)
total_simulation_time = Days[-1] * 24 * 3600  # Total time in seconds

# Parameters for time step generation
numpoints_per_period = 10000  # Points per period
total_points = numpoints_per_period * len(Period_Q)

def generate_time_steps(period_days, num_points, max_dt):
    """Generate time steps for a period that sum to exactly the period duration"""
    # Create base time points (0 to 1)
    t_normalized = np.linspace(0, 1, num_points)
    
    # Create weights with smaller steps at period boundaries
    weights = 0.5 + 0.5 * np.sin(np.pi * t_normalized - np.pi/2)
    weights = weights / np.sum(weights)  # Normalize to sum=1
    
    # Scale to period duration
    period_seconds = period_days * 24 * 3600
    dt_values = weights * period_seconds
    
    # Ensure no step exceeds max_dt
    while np.any(dt_values > max_dt):
        # Reduce peaks and renormalize
        dt_values = np.minimum(dt_values, max_dt)
        remaining_time = period_seconds - np.sum(dt_values)
        if remaining_time > 0:
            # Distribute remaining time
            dt_values += remaining_time / num_points
    
    return dt_values

def smooth_transition(t, t0, duration):
    """Smooth transition function using logistic sigmoid"""
    return 1 / (1 + np.exp(-8*(t - t0)/duration))

# Initialize combined arrays
Dt_combined = np.zeros(total_points)
Q_m3_d_combined = np.zeros(total_points)

# Generate time steps and flow rates
current_flow = 0.0  # Initial flow rate
time_accumulated = 0.0
start_idx = 0

for period_idx, (period_days, target_flow) in enumerate(zip(Period_Q, well_flowrate)):
    # Generate time steps for this period
    end_idx = start_idx + numpoints_per_period
    period_seconds = period_days * 24 * 3600
    
    # Generate Dt values that sum exactly to period duration
    Dt_period = generate_time_steps(period_days, numpoints_per_period, Dt_max)
    Dt_combined[start_idx:end_idx] = Dt_period
    
    # Calculate flow rate with smooth transitions
    transition_start = time_accumulated if period_idx > 0 else 0.0
    
    for i in range(start_idx, end_idx):
        current_time = time_accumulated
        progress = smooth_transition(current_time, transition_start, transition_duration)
        
        # For first period, transition from initial flow (0) to target
        if period_idx == 0:
            Q_m3_d_combined[i] = current_flow + (target_flow - current_flow) * progress
        else:
            # Transition from previous target to current target
            prev_target = well_flowrate[period_idx-1]
            Q_m3_d_combined[i] = prev_target + (target_flow - prev_target) * progress
        
        time_accumulated += Dt_combined[i]
    
    start_idx = end_idx

# Trim arrays to actual simulation time
simulation_end_idx = np.argmax(np.cumsum(Dt_combined) >= total_simulation_time)
if simulation_end_idx == 0:
    simulation_end_idx = len(Dt_combined)

Dt_combined = Dt_combined[:simulation_end_idx]
Q_m3_d_combined = Q_m3_d_combined[:simulation_end_idx]

# Verify total time matches
total_time = np.sum(Dt_combined)
print(f"Total simulation time: {total_time/(24*3600):.2f} days (target: {Days[-1]} days)")
print(f"Time steps: {len(Dt_combined)}")
print(f"Final flow rate: {Q_m3_d_combined[-1]:.2f} m³/d")

# Plot results
cumulative_time = np.cumsum(Dt_combined) / (24 * 3600)  # Convert to days

plt.figure(figsize=(12, 6))
plt.plot(cumulative_time, Q_m3_d_combined, label='Flow Rate')
for day in Days:
    plt.axvline(x=day, color='r', linestyle='--', alpha=0.3)
plt.xlabel('Time (days)')
plt.ylabel('Flow Rate (m³/d)')
plt.title('Smooth Flow Rate Transition Between Periods')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from typing import List, Tuple

# class SmoothFlowController:
#     def __init__(self, Q_m3_d: List[float], Period_Q: List[float], 
#                  transition_days: float = 2.0, max_time_expansion: float = 1.1):
#         """
#         Initialize the flow controller with target flow rates and periods.
        
#         Args:
#             Q_m3_d: List of target flow rates (m³/day)
#             Period_Q: List of period durations (days)
#             transition_days: Duration of smooth transitions between flow rates (days)
#             max_time_expansion: Multiplier for simulation time beyond last period
#         """
#         self.Q_m3_d = Q_m3_d
#         self.Period_Q = Period_Q
#         self.Days = [sum(Period_Q[:i+1]) for i in range(len(Period_Q))]
#         self.transition_time = transition_days * 24 * 3600  # Convert to seconds
#         self.max_time_expansion = max_time_expansion
        
#         # Simulation state
#         self.Time = [0.0]  # seconds
#         self.q_well = [0.0]  # m³/day
#         self.current_period = 0
#         self.simulation_complete = False
        
#         # Time step configuration
#         self.Dt_max = 10 * 24 * 3600  # seconds
#         self._init_time_steps()
        
#     def _init_time_steps(self):
#         """Initialize adaptive time steps for simulation"""
#         numpoints = 10001
#         xtime = np.linspace(0, 10000, num=numpoints)
#         # Sigmoid function for smooth time step variation
#         ytime = 1 / (1 + np.exp(-2*(xtime - 5000)/1000))  
#         self.Dt_list = self.Dt_max * ytime
    
#     def _smooth_heaviside(self, t: float, t0: float) -> float:
#         """
#         Smooth approximation of Heaviside function.
        
#         Args:
#             t: Current time (days)
#             t0: Transition start time (days)
            
#         Returns:
#             Transition progress (0 to 1)
#         """
#         # Normalize by transition time duration
#         k = self.transition_time / (24 * 3600)  # Convert back to days for scaling
#         return 1 / (1 + np.exp(-2*(t - t0)/k))
    
#     def _get_target_flow(self, t_days: float) -> Tuple[float, float]:
#         """
#         Calculate target flow rate and transition progress.
        
#         Args:
#             t_days: Current time in days
            
#         Returns:
#             (target_flow, transition_progress)
#         """
#         # If beyond last period, maintain final flow rate
#         if t_days >= self.Days[-1]:
#             return self.Q_m3_d[-1], 1.0
        
#         # Find current period
#         for i, day in enumerate(self.Days):
#             if t_days < day:
#                 target_flow = self.Q_m3_d[i]
#                 transition_start = self.Days[i-1] if i > 0 else 0.0
#                 progress = self._smooth_heaviside(t_days, transition_start)
#                 return target_flow, progress
                
#         return self.Q_m3_d[-1], 1.0
    
#     def step(self) -> bool:
#         """
#         Advance the simulation by one time step.
        
#         Returns:
#             True if simulation should continue, False if complete
#         """
#         if self.simulation_complete:
#             return False
            
#         j = len(self.Time) - 1
#         t_days = self.Time[j] / (3600 * 24)
        
#         # Check if simulation should end
#         if t_days >= self.Days[-1] * self.max_time_expansion:
#             self.simulation_complete = True
#             return False
        
#         # Get appropriate time step
#         Dt = self.Dt_list[j] if j < len(self.Dt_list) else self.Dt_max
        
#         # Calculate smooth flow transition
#         target_flow, progress = self._get_target_flow(t_days)
#         current_flow = self.q_well[-1]
#         new_flow = current_flow + (target_flow - current_flow) * min(progress * 1.5, 1.0)
        
#         # Update simulation state
#         self.Time.append(self.Time[j] + Dt)
#         self.q_well.append(new_flow)
        
#         return True
    
#     def run_simulation(self):
#         """Run complete simulation until all periods are processed"""
#         while self.step():
#             pass
    
#     def plot_results(self):
#         """Plot the flow rate over time"""
#         time_days = np.array(self.Time) / (3600 * 24)
        
#         plt.figure(figsize=(12, 6))
#         plt.plot(time_days, self.q_well, label='Well Flow Rate', linewidth=2)
        
#         # Add period markers and target flow lines
#         for i, day in enumerate(self.Days):
#             plt.axvline(x=day, color='r', linestyle='--', alpha=0.3)
#             plt.axhline(y=self.Q_m3_d[i], color='g', linestyle=':', alpha=0.3)
        
#         plt.xlabel('Time (days)', fontsize=12)
#         plt.ylabel('Flow Rate (m³/day)', fontsize=12)
#         plt.title('Smooth Well Flow Rate Transition', fontsize=14)
#         plt.grid(True, which='both', linestyle='--', alpha=0.6)
#         plt.legend(fontsize=12)
#         plt.tight_layout()
#         plt.show()

# # Example usage
# if __name__ == "__main__":
#     # Configuration
#     Q_m3_d = [2500.,0.,2000, 1000., 0.]  # Target flow rates (m³/day)
#     Period_Q = [10, 12, 7, 2, 5]  # Duration of each period (days)
#     transition_days = 3.0  # Days for smooth transitions
    
#     # Create and run controller
#     controller = SmoothFlowController(Q_m3_d, Period_Q, transition_days)
#     controller.run_simulation()
    
#     # Display results
#     print(f"Simulation completed in {len(controller.Time)} steps")
#     print(f"Final flow rate: {controller.q_well[-1]:.2f} m³/day")
    
#     # Plot results
#     controller.plot_results()
#     print(f"fim")
# # import numpy as np
# # from numpy import linspace

# # # Função de transição suave (aproximação da função Heaviside)
# # def smooth_heaviside(t, t0, k=0.1):
# #     """Aproximação suave da função Heaviside
# #     t: tempo atual
# #     t0: tempo de transição
# #     k: coeficiente de suavização (quanto menor, mais abrupta a transição)
# #     """
# #     return 1 / (1 + np.exp(-2*(t - t0)/k))

# # # Dados de entrada
# # Q_m3_d = [2500., 1000., 0.]  # m3/day
# # Period_Q = [15, 15, 5]  # day
# # Days = [sum(Period_Q[:i+1]) for i in range(len(Period_Q))]  # [15, 30, 35]

# # # Configurações de tempo
# # Time = [0.0]  # seconds
# # Dt_max = 10*24*3600  # seconds
# # Dt_initial = 1  # seconds

# # # Parâmetros de controle (não utilizados na versão simplificada)
# # alpha_static = 0.01
# # alpha_flow = 0.01

# # # Listas para armazenamento
# # q_well = [0.0]  # Vazão atual do poço

# # # Configuração da escala de tempo (opcional)
# # limpoints = [1, 10000]
# # numpoints = 10001
# # limtimeaxu = [1e-4, 9995]
# # xtime = linspace(limpoints[0], limpoints[1], num=numpoints)
# # ytime = 1 / (1 + np.exp(-2*(xtime - limpoints[1]/2)/(limpoints[1]*0.1)))  # Função sigmoide
# # Dt_list = Dt_max * ytime

# # def get_smooth_flow(j, Time, Days, Q_m3_d, transition_time=1.0):
# #     """Calcula a vazão com transição suave entre os períodos"""
# #     t = Time[j] / (3600 * 24)  # Converte para dias
    
# #     # Determina o período atual e o próximo valor de vazão
# #     current_q = q_well[-1]
# #     next_q = Q_m3_d[0]  # Valor padrão inicial
    
# #     for i, day in enumerate(Days):
# #         if t < day:
# #             next_q = Q_m3_d[i]
# #             transition_start = Days[i-1] if i > 0 else 0.0
# #             break
    
# #     # Se estamos no último período, mantemos a última vazão
# #     if t >= Days[-1]:
# #         return Q_m3_d[-1]
    
# #     # Calcula o progresso da transição (0 a 1)
# #     transition_progress = smooth_heaviside(t, transition_start, transition_time)
    
# #     # Interpola suavemente entre a vazão atual e a próxima
# #     smooth_q = current_q + (next_q - current_q) * transition_progress
    
# #     return smooth_q

# # def testing_control(j, Time, Days, Q_m3_d, Dt_max):
# #     """Função de controle modificada para transições suaves"""
# #     if Time[j] <= Days[-1] * 3600 * 24:
# #         # Usa Dt da lista ou um valor padrão
# #         Dt = Dt_list[j] if j < len(Dt_list) else Dt_max
        
# #         # Obtém a vazão com transição suave
# #         current_q = get_smooth_flow(j, Time, Days, Q_m3_d, transition_time=2.0)  # 2 dias de transição
        
# #         q_well.append(current_q)
# #         return Dt, current_q
# #     else:
# #         return Dt_max, Q_m3_d[-1]

# # # Simulação principal
# # j = 0
# # while Time[j] <= Days[-1] * 3600 * 24 * 1.1:  # 10% a mais para garantir estabilização
# #     Dt, q = testing_control(j, Time, Days, Q_m3_d, Dt_max)
# #     Time.append(Time[j] + Dt)
# #     j += 1

# # # Resultados
# # print("Tempo total simulado:", Time[-1]/(3600*24), "dias")
# # print("Número de passos:", len(Time))
# # print("Última vazão:", q_well[-1], "m3/d")

# # # Opcional: Plotar os resultados
# # import matplotlib.pyplot as plt
# # plt.figure(figsize=(10, 5))
# # plt.plot(np.array(Time)/(3600*24), q_well, label='Vazão do poço')
# # plt.xlabel('Tempo (dias)')
# # plt.ylabel('Vazão (m³/dia)')
# # plt.title('Transição suave de vazão do poço')
# # plt.grid(True)
# # for day in Days:
# #     plt.axvline(x=day, color='r', linestyle='--', alpha=0.3)
# # plt.legend()
# # plt.show()

# # # import numpy as np
# # # from skfuzzy import smf

# # # # Dados de entrada
# # # Period_Q = [15, 15, 5]  # dias
# # # Dt_max = 10 * 24 * 3600  # segundos
# # # limpoints = [1, 10000]
# # # numpoints = 10000
# # # limtimeaxu = [1e-4, 9995]

# # # # Gerar xtime e ytime
# # # xtime = np.linspace(limpoints[0], limpoints[1], num=numpoints)
# # # ytime = smf(xtime, limtimeaxu[0], limtimeaxu[1])  # Assumindo que smf está definida

# # # # # Função para criar Dt sem normalizar ytime
# # # # def create_Dt_no_norm(period_days, Dt_max, ytime):
# # # #     total_seconds = period_days * 24 * 3600
# # # #     Dt_initial = Dt_max * ytime  # Dt sem ajuste
# # # #     sum_Dt_initial = np.sum(Dt_initial)
    
# # # #     # Fator de correção para atingir o total desejado
# # # #     correction_factor = total_seconds / sum_Dt_initial
# # # #     Dt_corrected = Dt_initial * correction_factor
    
# # # #     # Verifica se algum elemento excede Dt_max após correção
# # # #     if np.any(Dt_corrected > Dt_max):
# # # #         print(f"Aviso: Correção ultrapassa Dt_max no período de {period_days} dias.")
# # # #         # Opção 1: Limitar e aceitar que a soma não será exata
# # # #         Dt_corrected = np.minimum(Dt_corrected, Dt_max)
# # # #         # Opção 2: Redistribuir diferença (mais complexo)
    
# # # #     return Dt_corrected

# # # # # Criar Dt para cada período em Period_Q
# # # # Dt_list = []
# # # # for period in Period_Q:
# # # #     Dt = create_Dt_no_norm(period, Dt_max, ytime)
# # # #     Dt_list.append(Dt)
# # # #     print(f"Período: {period} dias | Soma de Dt: {np.sum(Dt) / (24 * 3600):.2f} dias")

# # # # # Dt_list[0] = Dt para Period_Q[0], etc.

# # # # Função para criar Dt para um período específico
# # # def create_Dt(period_days, Dt_max, ytime):
# # #     total_seconds = period_days * 24 * 3600
# # #     ytime_normalized = ytime / np.sum(ytime)  # Normaliza para soma = 1
# # #     Dt = total_seconds * ytime_normalized  # Escala para o total desejado
    
# # #     # Verifica se algum elemento excede Dt_max
# # #     if np.any(Dt > Dt_max):
# # #         print("Aviso: Alguns elementos de Dt excedem Dt_max. Ajustando...")
# # #         Dt = np.minimum(Dt, Dt_max)  # Limita pelo Dt_max
# # #         # Reajusta a soma para o total desejado (opcional)
# # #         # Isso pode ser feito redistribuindo a diferença, mas pode ser complexo
# # #     return Dt

# # # # # Criar Dt para cada período em Period_Q
# # # # Dt_list = []
# # # # for period in Period_Q:
# # # #     Dt = create_Dt(period, Dt_max, ytime)
# # # #     Dt_list.append(Dt)
# # # #     # Dt_list.append(Dt)
# # # #     print(f"Período: {period} dias, Soma de Dt: {np.sum(Dt) / (24 * 3600)} dias")

# # # # --- Modificação principal: Criar um único vetor Dt sem lista ---
# # # # Calcula o tamanho total necessário (numpoints * número de períodos)
# # # total_length = numpoints * len(Period_Q)
# # # Dt_combined = np.empty(total_length)  # Array vazio pré-alocado

# # # start_idx = 0
# # # for period in Period_Q:
# # #     Dt = create_Dt(period, Dt_max, ytime)
# # #     end_idx = start_idx + numpoints
# # #     Dt_combined[start_idx:end_idx] = Dt  # Preenche o segmento atual
# # #     print(f"Período: {period} dias, Soma de Dt: {np.sum(Dt) / (24 * 3600)} dias")
# # #     start_idx = end_idx

# # # print(f"fim")