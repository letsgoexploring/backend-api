import linearsolve as ls
import numpy as np
import pandas as pd


# 1. Supplied by user
# A=1
# alpha=0.33
# delta=0.025
# beta=0.98
# sigma = 1
# eta = 1
# phi = 1.5
# rho = 0.9
# sige = 0.01
# parameters = 41

# Function that evaluates the equilibrium conditions
def equilibrium_equations(variables_forward, variables_current, parameters):
    # Parameters
    p = parameters

    # Variables
    fwd = variables_forward
    cur = variables_current

    # Household Euler equation
    euler_eqn = (p.beta * fwd.c ** -p.sigma *
                 (p.alpha * fwd.a * fwd.k ** (p.alpha - 1) *
                  fwd.l ** (1 - p.alpha) + 1 - p.delta) -
                 cur.c ** -p.sigma)

    # Labor supply
    labor_supply = ((1 - p.alpha) * cur.c ** -p.sigma * cur.a * cur.k ** p.alpha *
                    cur.l ** -p.alpha - p.phi * (1 - cur.l) ** -p.eta)

    # Goods market clearing
    market_clearing = cur.c + cur.i - cur.y

    # Production function
    production_fun = cur.a * cur.k ** p.alpha * cur.l ** (1 - p.alpha) - cur.y

    # Capital evolution
    capital_evolution = fwd.k - (1-p.delta)*cur.k - cur.i

    # Exogenous technology
    technology_proc = p.rhoa * np.log(cur.a) - np.log(fwd.a)

    # Stack equilibrium conditions into a numpy array
    return np.array([
        euler_eqn,
        labor_supply,
        market_clearing,
        production_fun,
        capital_evolution,
        technology_proc
    ])


def centralized_rbc_with_labor_simulation(parameters):
    # Initialize the model
    parameters = pd.Series(parameters)
    model = ls.model(equations=equilibrium_equations,
                     nstates=2,
                     varNames=['a', 'k', 'c', 'i', 'y', 'l'],
                     shockNames=['eA', 'eK'],
                     parameters=parameters)

    # Compute steady state, approximate, solve, and simulate
    guess = [1, 2, 1, 1, 1, 0.3]
    model.compute_ss(guess)
    model.approximate_and_solve()
    model.impulse(T=parameters['periods'], t0=5, shock=[parameters['sige'], 0])

    return {
        't': model.irs['eA']['eA'].index.tolist(),
        'e': model.irs['eA']['eA'].tolist(),
        'a': model.irs['eA']['a'].tolist(),
        'k': model.irs['eA']['k'].tolist(),
        'c': model.irs['eA']['c'].tolist(),
        'i': model.irs['eA']['i'].tolist(),
        'y': model.irs['eA']['y'].tolist(),
        'l': model.irs['eA']['l'].tolist(),
    }
