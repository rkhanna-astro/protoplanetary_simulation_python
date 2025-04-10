import numpy as np
import config as cfig
from datetime import datetime
import plot_me

def makedata(X, Y, ts, Menv0, tps, alpha, eta):
    K = cfig.K
    G = cfig.G
    gamma = cfig.gamma 
    Lambda0 = cfig.Lambda0
    s = cfig.s 
    Md = cfig.Md 
    sc_ind = cfig.sc_ind 
    Mdot_ps = cfig.Mdot_ps 
    Msc = cfig.Msc

    mdotfactor = ((K**1.5) * (G**((1 - 3*gamma)/2)) * (ts**(3 - 3*gamma)) / 1.989e+30) * 3.15569e+7
    mfactor = (K**1.5) * (G**((1 - 3*gamma)/2)) * (ts**(4 - 3*gamma)) / 1.989e+30

    print(f'Values of mfactor and mdotfactor are: {mfactor} and {mdotfactor}')

    GBfactor = (4.0 * np.pi)**((gamma - 1.0) / gamma) * gamma**(-1.0 / gamma)
    GammaBig = GBfactor * Y[1, :]**(2.0 * (1.0 - gamma) / gamma) * Lambda0 * X**s

    factor1 = ((4 * np.pi * gamma)**((gamma - 1.0) / (2 * gamma)) * Y[1, :]**((1.0 - gamma) / gamma)) / (gamma**0.5)
    vr_cs = np.abs(factor1 * Y[0, :])

    sfactor = (1 / (2 * np.pi)) * (K**0.5) * (G**(-0.5 * (1.0 + gamma))) * (ts**(-gamma)) * 0.1
    sigma = sfactor * Y[1, :]
    print(f'sigma_end: {sigma[-1]} gr/cm^2')
    disk_region = np.where(sigma > 0.1)[0]
    print(f'indice:: disk_region(end): {disk_region[-1]}')

    J = X * (Y[1, :] * (Y[0, :] - (2 - gamma) * X) / (3 * gamma - 4))**0.5

    dlnJ_dlnx = 0.5 + (3 * gamma - GammaBig - 4) * X / (2 * (Y[0, :] - (2.0 - gamma) * X))
    factor3 = ((4 * np.pi)**(0.5 * (1.0 - gamma) / gamma)) * (gamma**(0.5 / gamma)) * (Y[1, :]**(-1.0 / gamma))
    Qtoomre = factor3 * 2 * J * (2 * dlnJ_dlnx)**0.5 / (X**2)

    V_z = (Lambda0 * X**s) / Y[1, :]

    H_r = (4 * np.pi)**((1.0 - gamma) / gamma) * (gamma**(1.0 / gamma)) * (Y[1, :]**((gamma - 2.0) / gamma)) * (1.0 / X)

    P_rho = Y[1, :]**((2.0 * gamma - 2.0) / gamma)

    Mdot_acc = mdotfactor * X * Y[1, :] * Y[0, :] / (3 * gamma - 4)
    print(f'The value of Mdot_acc at the outer boundary is: {Mdot_acc[-1]} M_sun/yr')

    v_phi_cs = factor1 * J / X

    v_z_cs = factor1 * V_z

    J_M = np.sqrt(np.abs((3.0 * gamma - 4.0) / (Y[1, :] * (Y[0, :] - (2.0 - gamma) * X))))
    factor4 = ((4 * np.pi)**(0.5 * (1.0 - gamma) / gamma)) * (gamma**(0.5 / gamma)) * (Y[1, :]**(gamma - 1.0 / gamma))
    jmath = factor4 * J_M

    Mdot_w_Mdot_acc = mdotfactor * Y[2, :] / Mdot_acc
    print(f'Mw/Macc (i,f): {Mdot_w_Mdot_acc[0]} and {Mdot_w_Mdot_acc[-1]}')

    Mdisk = mfactor * (Y[0, :] - (2.0 - gamma) * X) * Y[1, :] * X / (3.0 * gamma - 4.0)
    Md = Mdisk[-1]

    Menv = Menv0 - Md
    Mdisk_Menv = Mdisk / Menv

    cs = ((4 * np.pi)**((1 - gamma) / (2 * gamma))) * (gamma**(0.5 / gamma)) * (K**0.5) * (G**((1 - gamma) / 2)) * (ts**(1 - gamma)) * (Y[1, :]**((gamma - 1) / gamma))
    cs = cs * 1.e-3

    r = X * (K**0.5) * (G**((1.0 - gamma) / 2.0)) * (ts**(2 - gamma)) / 1.49597870691e+11
    j = K * (G**(1 - gamma)) * (ts**(3 - 2 * gamma)) * J

    Ew = (K**1.5) * (G**((3.0 - 5.0 * gamma) / 2.0)) * (ts**(6.0 - 5.0 * gamma)) * Y[4, :]

    sinkind = np.where(r < 5)[0]
    sc_ind = sinkind[-1]
    Mdot_ps = Mdot_acc[sc_ind]
    Msc = Mdisk[sc_ind]

    r_cm = X * (K**0.5) * (G**((1.0 - gamma) / 2.0)) * (ts**(2 - gamma))
    H_cm = r_cm * H_r
    rho_midplane = sigma / (2 * H_cm)

    lambda_cj = 2 * ((cs * 1.e+3)**2) / (G * 10 * sigma * (1 + (1 - Qtoomre**2)**0.5))
    lambda_cj = lambda_cj / 1.49597870691e+11

    Rcj = lambda_cj / r[-1]

    plotmat = np.zeros((14, len(X)))
    plotmat[0, :] = r
    plotmat[1, :] = v_phi_cs
    plotmat[2, :] = cs
    plotmat[3, :] = vr_cs
    plotmat[4, :] = sigma
    plotmat[5, :] = Mdisk
    plotmat[6, :] = Ew
    plotmat[7, :] = Mdot_acc
    plotmat[8, :] = Qtoomre
    plotmat[9, :] = Mdisk_Menv
    plotmat[10, :] = Rcj
    plotmat[11, :] = dlnJ_dlnx
    plotmat[12, :] = J
    plotmat[13, :] = factor3

    # print(plotmat)

    # plot_me.plotme(plotmat)

    header = "r, v_phi_cs, cs, vr_cs, sigma, Mdisk, Ew, Mdot_acc, Qtoomre, Mdisk_Menv, Rcj, dlnJ_dlnx, J, factor3"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

    # Create filename with timestamp
    csv_filename = f"output_alpha_{alpha}_eta_{eta}_time_{int(tps)}.csv"

    # Transpose plotmat so each column becomes a row (CSV convention)
    np.savetxt(csv_filename, plotmat.T, delimiter=',', header=header, comments='')

    return plotmat

# Example usage
# X = np.linspace(0, 10, 100)
# Y = np.random.rand(5, 100)
# ts = 1.0
# Menv0 = 1.0

# plotmat = makedata(X, Y, ts, Menv0)
# print(plotmat)