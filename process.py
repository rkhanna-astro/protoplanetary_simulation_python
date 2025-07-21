import numpy as np
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from scipy.optimize import root_scalar
import fun_bvps_c as funbvps
import funsys_c as funsys
import makedata_c as makedata
import config as globals

def process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable, lambda0 = None):
    # Clear previous variables (not needed in Python)
    # clc equivalent in Python is not needed

    # Set global variables
    globals.gamma = gamma_eff

    globals.Lambda0 = 0.1

    if lambda0 is not None:
        globals.Lambda0 = lambda0
    
    globals.eta = etaprime if etaprime != -999 else 1e-2
    ty = tps
    globals.ts = ty * 3.15569e7  # Convert years to seconds

    print("Properties1", alpha_0, etaprime, gamma_eff, Mdot_stable)
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
        method='toms748'       # Brent's method (default, most reliable)
    )
    print(f's0_root = {s0_root} | f(s0_root) = {funbvps.funbvps(s0_root.root)}')

    print("this is the root", s0_root.root)

    # x_scaled = np.linspace(1, 1e5, 100)
    # x = safe_logspace(x0, xf, 100)
    # print(x)
    
    sol = solve_ivp(funsys.funsys, [x0, xf], [globals.v0, s0_root.root, 0, 0, 0])
    x = sol.t
    Yv = sol.y
    print(Yv)
    print(f'w0, G0 = {globals.w0}, {globals.G0}')

    Aa = x_shock * (4.0 * np.pi)**((globals.gamma-1.0)/(2*globals.gamma)) * globals.gamma**(-1.0/(2*globals.gamma)) * Yv[-1, 1]**((1.0-globals.gamma)/globals.gamma)
    print(f'Aa = {Aa}')
    Cs_end = ((4 * np.pi)**((1-globals.gamma)/(2*globals.gamma))) * (globals.gamma**(0.5/globals.gamma)) * (globals.K**0.5) * (globals.G**((1-globals.gamma)/2)) * (globals.ts**(1-globals.gamma)) * (Yv[-1, 1]**((globals.gamma-1)/globals.gamma))
    print(f'Cs_end = {Cs_end}')

    # Calculate mass of the envelope
    hardcoded_vals = {0.1: 5.2486, 0.2: 2.6243, 0.3: 1.7495, 0.5: 1.0497, 0.8: 0.6561, 1.0: 0.5249}
    Menv0 = hardcoded_vals.get(alpha_0, None)

    if not Menv0:
        multi = alpha_0 * 10
        Menv0 = np.round(hardcoded_vals[0.1] / multi, 4)
    
    plotmat = makedata.makedata(x, Yv, globals.ts, Menv0, tps, alpha_0, etaprime)
    print(f'Mdisk = {globals.Md}')

    return plotmat


def safe_logspace(x0, xf, num=100):
    """
    Generates a strictly increasing logspace array with validation.
    
    Args:
        x0: Start value (must be > 0)
        xf: End value (must be > x0)
        num: Number of points
        
    Returns:
        Monotonically increasing array with num points from x0 to xf
    """
    # Input validation
    if None in (x0, xf):
        raise ValueError("x0 and xf cannot be None")
    if x0 <= 0 or xf <= 0:
        raise ValueError("x0 and xf must be positive")
    if xf <= x0:
        raise ValueError("xf must be greater than x0")
    
    # Generate logspace with extra points
    x = np.logspace(-5, 1, num, dtype = np.float32)
    
    # Remove duplicates (floating-point artifacts)
    x = np.unique(x)  # Automatically sorts too
    
    # # Ensure we have enough points
    # if len(x) < num:
    #     # If we lost too many points, use linspace in log domain
    #     x = np.exp(np.linspace(np.log(x0), np.log(xf), num))
    # else:
    #     # Select evenly spaced indices to get desired number
    #     idx = np.linspace(0, len(x)-1, num, dtype=int)
    #     x = x[idx]
    
    # Final validation
    assert np.all(np.diff(x) > 0), "Output is not strictly increasing"
    return x

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