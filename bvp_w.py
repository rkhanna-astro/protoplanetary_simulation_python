import numpy as np
from scipy.integrate import solve_bvp

#
# this code is a function to solve e.g. d^2ydx^2+y = 0. >> the exact solution is y=sin(x)
# first we reduce the second-order equation to a system of first-order equations
#
# dy/dx = z
# dz/dx = -y
#
# boundary conditions:
#
# z(x=0)  = 1  ! first boundary
# y(x=pi) = 0  ! second boundary


def bvp():

    # In the matlab code, there was a sentence, clear all
    global K, G, t, Mb0, Lambda0, gamma, eta, l, lm, s, mdotfactor

    K = 200**2 # m2/s2
    G = 6.67384e-11 # % m^3 kg^-1 s^-2 -OR- N (m/kg)^2

    eta = 0.01  # % viscosity parameter 1


    l = 1.0 # % viscosity parameter 2
    Lambda0 = 0.0 # % strength of wind
    lm = 1.0 # % angular momentum loss efficiency factor
    s = 0.7 # % wind power-low exponent
    gamma = 1.1  # % adiabatic index
    t = 1.e+4
    dt = 1.e+4 # % yr

    tmax = 1.0e+6
    nelement = int((tmax - t) / dt) + 1
    tt = np.zeros(nelement)
    Mb = np.zeros(nelement)
    Mdisk_tot = np.zeros(nelement)
    Mps = np.zeros(nelement)
    Menv = np.zeros(nelement)
    Menv_new = np.zeros(nelement)
    Mdiskps_new = np.zeros(nelement)

    Mps[0] = 1.e-3 #% solar unit
    M_cloud = 1.0  #% solar unit
    tau_acc = 1.e+6 # %Yr
    i = 1
    tt[0] = t

    ts = t * 3.15569e+7 #% convert years to seconds
    # % LogMdot=logMdot_max*(t/tau_acc)*exp(-t/tau_acc)
    # %Mb(i-1)= Mdot_max*exp(-t/tau_acc);
    mdotfactor = ((K**1.5) * (G**((1 - 3 * gamma) / 2)) * (ts**(3 - 3 * gamma)) / 1.989e+30) * 3.15569e+7

    mfactor = (K**1.5) * (G**((1 - 3 * gamma) / 2)) * (ts**(4 - 3 * gamma)) / 1.989e+30
    Mb0 = 1.e-6 #%(M_cloud/tau_acc)*exp(-t/tau_acc);
    x = np.array([1.0e-3, 1.0])
    y = np.array([-1.0e-1, 1.0e+7])
    sol = solve_bvp(deriv, bcs, x, y)
    X = sol.x
    Y = sol.y

    r = X * (K**0.5) * (G**((1 - gamma) / 2)) * (ts**(2 - gamma)) / 1.49597870691e+11 # In AU
    # %gamma_smooth = ( (X-1)*(1.1-1.0)/(0.01-1.0) ) + 1 ;
    print('The value of factor2X is', mdotfactor)
    # %	.*---------- Mass accretion rate
    Mdot_acc = mdotfactor * X * Y[1, :] * Y[0, :] / (3 * gamma - 4)
    # %	.*---------- Mass of disk
    Mdisk = mfactor * (Y[0, :] - (2 - gamma) * X) * Y[1, :] * X / (3 * gamma - 4) #% solar unit
    Mdisk_tot = Mdisk[-1]

    makedata(sol.x, sol.y, t - dt)

def deriv(x, y):
    global eta, l, Lambda0, lm, s, gamma

    gamma = ((x - 1) * (1.1 - 1.0) / (0.01 - 1.0)) + 1

    GBfactor = 0 # %(4.0*pi)^((gamma-1.0)/gamma) * gamma^(-1.0/gamma);
    GammaBig = 0 # %GBfactor * y(2)^(2.0*(1.0-gamma)/gamma) * Lambda0*x^s;

    if True:
        dGammaBig_dx = 0 # %s*Lambda0*x^(s-1);
    else:
        dGammaBig_dx = 0 # %(2.0*(1.0-gamma)/gamma) * dydx(2,1) * y(2)^((2.0-3.0*gamma)/gamma) * Lambda0*x^s + y(2)^(2.0*(1.0-gamma)/gamma) * s*Lambda0*x^(s-1);

    dGammaBig_dx = GBfactor * dGammaBig_dx

    #%coefficients

    A = ((y[0] - (2 - gamma) * x)**4) * (y[0] + (2 * lm**2 - 1) * x * GammaBig) / x**2
    B = x * dGammaBig_dx - 3 * GammaBig + 12 * gamma - 18
    C = (gamma - 2) * x * dGammaBig_dx - 2 * (GammaBig**2) + (5 * gamma - 2) * GammaBig - 10 * gamma + 12
    J = ((y[1] * y[0] / (3 * gamma - 4))**0.5) * x
    nu = eta * (y[1]**2) * (x**2) / (J**3)

    # % d{Vr}/dx

    dydx = np.zeros(2)
    dydx[0] = ((A / nu) + B * y[0] + C * x + 6 * (y[0]**2) / x) / (9 * y[0] - (3 * gamma + 2) * x - 4 * x * GammaBig)
    # % d{Sigma}/dx
    dydx[1] = -(y[1] / x) - y[1] * (dydx[0] - (2.0 - gamma)) / (y[0] - (2.0 - gamma) * x) + y[1] * (3.0 * gamma - GammaBig - 4.0) / (y[0] - (2.0 - gamma) * x)
    return dydx

# % d{Mdot_w}/dx
# %dydx(3) = y(2) * x * GammaBig;

# % boundary conditions y'(a)=1, y(b)=0.

def bcs(ya, yb):
    global Mb0, mdotfactor, gamma
    Xa = 1.e-2
    Xb = 1.0
    Mdot_acc = mdotfactor * Xb * yb[1] * yb[0] / (3 * gamma - 4) #  % solar mass per year
    Va = -1.e-4 # %(- ( (4.*l+6.)-(2.*l+6.)*gamma ) / (3.-2.*l) ) * ( Xa - (9.*(4.-3.*gamma)*Xa^3.) / (2.*l-3.)*(6.*l^2-2.*l-15.)*eta*Xa^l );
    # %Mb = 1.e-9;
    return np.array([ya[0] - Va, Mdot_acc - Mb0]) # %yb(2) - 5.0];
    #%yb(3)]; x.*yb(2).*yb(1)./(3.*gamma-4.)-1.0

