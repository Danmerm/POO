class ConvertBtoI:
    '''
    Converte as unidades do Sistema Brasileiro
    para o sistema Internacional
    '''
    def permeability(x): # milidarcy -> m^2
        return x*(9.86923e-16)

    def viscosity(x): #cp -> Pa*s
        return x*(1e-3)

    def flow_rate(x): #m^3/dia to m^3/s
        return x/86400.0

    
class ConvertItoB:

    '''
    Converte as unidades do Sistema Internacional
    para o sistema Basilero
    '''

    def permeability(x):  # m^2 -> milidarcy
        return x/(9.86923e-16)

    def viscosity(x): #Pa*s -> cp
        return x/(1e-3)

    def flow_rate(x): #m^3/s to m^3/dia
        return x*86400.0

    
def Convert_kPa_to_Pa(x):
    return 1000.0*x
def Convert_Pa_to_kPa(x):
    return x/1000.0