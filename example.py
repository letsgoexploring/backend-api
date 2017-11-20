import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import linearsolve as ls
import scipy.linalg as la


# 1. Supplied by user
alpha  = .35
beta  = 0.99
delta   = 0.025
rhoa = .9
sigma = 1.5
A = 1

# 2. Simulation

# Set parameters
parameters = pd.Series()
parameters['alpha']  = .35
parameters['beta']  = 0.99
parameters['delta']   = 0.025
parameters['rhoa'] = .9
parameters['sigma'] = 1.5
parameters['A'] = 1

# Funtion that evaluates the equilibrium conditions
def equilibrium_equations(variables_forward,variables_current,parameters):
    
    # Parameters 
    p = parameters
    
    # Variables
    fwd = variables_forward
    cur = variables_current
    
    # Household Euler equation
    euler_eqn = p.beta*fwd.c**-p.sigma*(p.alpha*cur.a*fwd.k**(p.alpha-1)+1-p.delta) - cur.c**-p.sigma
    
    # Goods market clearing
    market_clearing = cur.c + fwd.k - (1-p.delta)*cur.k - cur.a*cur.k**p.alpha
        
    # Exogenous technology
    technology_proc = p.rhoa*np.log(cur.a) - np.log(fwd.a)
    
    # Stack equilibrium conditions into a numpy array
    return np.array([
            euler_eqn,
            market_clearing,
            technology_proc
        ])

# Initialize the model
model = ls.model(equations = equilibrium_equations,
                 nstates=2,
                 varNames=['a','k','c'],
                 shockNames=['eA','eK'],
                 parameters = parameters)

# Compute steady state, approximate, solve, and simulate
guess = [1,1,1]
model.compute_ss(guess)
model.approximate_and_solve()
model.impulse(T=41,t0=5,shock=None)

# Store output in variables
t = model.irs['eA']['eA'].index.tolist()
e = model.irs['eA']['eA'].tolist()
a = model.irs['eA']['a'].tolist()
k = model.irs['eA']['k'].tolist()
c = model.irs['eA']['c'].tolist()

print('t:',t,'\n')
print('e:',e,'\n')
print('a:',a,'\n')
print('k:',k,'\n')
print('c:',c,'\n')
