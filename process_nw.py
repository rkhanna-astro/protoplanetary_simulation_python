import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.optimize import root_scalar
from scipy.integrate import solve_ivp
import fun_bvps_c as funbvps
import funsys_c as funsys
import makedata_c as makedata
import config as globals

# Define global variables
# class GlobalVars:
#     K = 4e5
#     G = 6.67384e-11
#     ts = None
#     eta = None
#     gamma = None
#     Lambda0 = 0.0
#     lm = 1.5
#     s = 0.7
#     dSigma_dx = -1e3
#     class_type = 'disk'
#     Mdot_out = None
#     mdotfactor = None
#     xb = None
#     v0 = -1e-5
#     w0 = None
#     G0 = None
#     E0 = None
#     Md = None
#     Menv_at_time = None
#     sc_ind = None
#     Mdot_ps = None
#     Msc = None
#     Mps = 1e-3

# globals = GlobalVars()

def process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable, lambda0 = None):
    # Clear previous variables (not needed in Python)
    # clc equivalent in Python is not needed

    # Set global variables
    globals.gamma = gamma_eff
    globals.Lambda0 = 0.0
    globals.eta = etaprime if etaprime != -999 else 1e-2
    ty = tps
    globals.ts = ty * 3.15569e7  # Convert years to seconds

    x_shock = x_sh_test
    if x_sh_test == 0:
        x_shock = (25.) * (globals.K**-0.5) * (globals.G**((globals.gamma-1)/2)) * (globals.ts**(globals.gamma-2)) * 1.49597870691e11  # in AU
        print(f'x_shock = {x_shock}')

    x0 = 1e-5
    xf = x_shock
    globals.xb = [x0, xf]

    if Mdot_stable == -999:
        Mdot_stable = 1.0079e-5
    globals.Mdot_out = Mdot_stable * (alpha_0**-1.5)

    if Mdot_stable == -1:
        globals.Mdot_out = 0.6

    s0_i = 1e4
    s0_f = 1e12

    globals.mdotfactor = ((globals.K**1.5) * (globals.G**((1 - 3*globals.gamma)/2)) * (globals.ts**(3 - 3*globals.gamma)) / 1.989e30) * 3.15569e7

    s0_root = root_scalar(
        funbvps.funbvps,
        bracket=[s0_i, s0_f],  # Interval where sign changes
        method='toms748'        # Brent's method (default, most reliable)
    )
    print(f's0_root = {s0_root} | f(s0_root) = {funbvps.funbvps(s0_root.root)}')

    # x = np.linspace(x0, xf, 100)
    sol = solve_ivp(funsys.funsys, [x0, xf], [globals.v0, s0_root.root, 0, 0, 0])
    Yv = sol.y
    x = sol.t
    print(f'w0, G0 = {globals.w0}, {globals.G0}')

    Aa = x_shock * (4.0 * np.pi)**((globals.gamma-1.0)/(2*globals.gamma)) * globals.gamma**(-1.0/(2*globals.gamma)) * Yv[-1, 1]**((1.0-globals.gamma)/globals.gamma)
    print(f'Aa = {Aa}')
    Cs_end = ((4 * np.pi)**((1-globals.gamma)/(2*globals.gamma))) * (globals.gamma**(0.5/globals.gamma)) * (globals.K**0.5) * (globals.G**((1-globals.gamma)/2)) * (globals.ts**(1-globals.gamma)) * (Yv[-1, 1]**((globals.gamma-1)/globals.gamma))
    print(f'Cs_end = {Cs_end}')

    # Calculate mass of the envelope
    Menv0 = {0.1: 5.2486, 0.2: 2.6243, 0.3: 1.7495, 0.5: 1.0497, 0.8: 0.6561, 1.0: 0.5249}.get(alpha_0, None)
    plotmat = makedata.makedata(x, Yv, globals.ts, Menv0, tps, alpha_0, etaprime)
    print(f'Mdisk = {globals.Md}')

    return plotmat

# def funbvps(s):
#     # Define the function for boundary value problem solver
#     # Placeholder implementation
#     return s - 1e8

# def funsys(Y, x):
#     # Define the system of ODEs
#     # Placeholder implementation
#     return [Y[0], Y[1], Y[2], Y[3], Y[4]]

# def makedata(x, Yv, ts, Menv0):
#     # Placeholder implementation for makedata function
#     return np.array([x, Yv, ts, Menv0])

# Example usage
# plotmat = process(1.0, 0, 1.1, 0.1, 1e-2, 1.0079e-5)
