import numpy as np
import matplotlib.pyplot as plt

def decay(M0_env, Mend, time):
    global Menv_at_time
    G = 6.67384e-11
    rho = (1.4e-19) * 1000  # kg/m^3 >> observations
    tff = np.sqrt(3 * np.pi / (32 * G * rho)) / 3.15569e+7  # yr
    tau = tff / 3  # yr
    tau_bontemps = 9.e+4  # yr

    # M0_env in M_sun
    Mend = 1.0
    Mdot_max = (10**(-4.78)) * (Mend**0.65)  # see Dib et al. (2010)
    print(f'Mdot_max, tff: {Mdot_max}, {tff}')

    t = np.linspace(1.e+0, 3.e+5, int(1.e+5))
    Macc = (M0_env / tau_bontemps) * np.exp(-t / tau_bontemps)  # Bontemps(1996)
    Menvp = M0_env * np.exp(-t / tau_bontemps)
    Mdot = 10**(((7 + np.log10(Mdot_max)) * (np.exp(1) * t / tau) * np.exp(-t / tau)) - 7)  # Schmeja & Klessen (2004)

    nelement = t.size
    Menv = np.zeros(nelement)
    Menv[0] = M0_env
    for i in range(1, nelement):
        dt = t[i] - t[i - 1]
        Menv[i] = Menv[i - 1] - Mdot[i - 1] * dt  # true!

    Class0_ind = np.where(Menvp > 0.5 * M0_env)[0]
    psf_ind = np.where(Menvp > 0.99 * M0_env)[0]
    t_0to1 = t[Class0_ind[-1]]
    t_psf = t[psf_ind[-1]]
    print(f't_0to1: {t_0to1}')
    print(f't_psf: {t_psf}')

    div = 1  # or tau
    plt.semilogy(t / div, Macc)
    plt.grid()
    plt.hold(True)
    plt.semilogy(t / div, Mdot)
    mp = plt.semilogy(t / div, Menvp)
    plt.setp(mp, linestyle=':', color='green', linewidth=2)

    vert1 = plt.axvline(x=t_0to1 / div, color='red', linestyle='-', linewidth=1)
    vert2 = plt.axvline(x=t_psf / div, color='red', linestyle='-', linewidth=1)
    plt.hold(False)

    myind = np.where(t < time)[0]
    Menv_at_time = Menvp[myind[-1]]
    Minfall = (M0_env / tau_bontemps) * np.exp(-time / tau_bontemps)  # Bontemps(1996)
    out = Minfall

    return out

# Example usage
M0_env = 1.0
Mend = 1.0
time = 1.e+5

result = decay(M0_env, Mend, time)
print(result)