import numpy as np
import matplotlib.pyplot as plt

# Grid size
m = 20
n = 20

A = np.linspace(0.3, 0.8, m)
B = np.linspace(1.0, 1.1, n)

def process(tps, x_sh_test, gamma_eff, alpha_0, Mdot_stable):
    # Placeholder function for process
    # You need to implement this based on your specific requirements
    return np.random.rand(10, 10)  # Example output

Qmatrix1 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | gamma = {gamma}')
        plotmat = process(1.e+3, 1.0, gamma, alpha_0, -999)
        Qmax = np.max(plotmat[8, :])
        Qmatrix1[i // n, i % n] = Qmax
        i += 1

Qmatrix2 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | gamma = {gamma}')
        plotmat = process(2.e+3, 1.0, gamma, alpha_0, -999)
        Qmax = np.max(plotmat[8, :])
        Qmatrix2[i // n, i % n] = Qmax
        i += 1

Qmatrix3 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | gamma = {gamma}')
        plotmat = process(3.e+3, 1.0, gamma, alpha_0, -999)
        Qmax = np.max(plotmat[8, :])
        Qmatrix3[i // n, i % n] = Qmax
        i += 1

Qmatrix4 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | gamma = {gamma}')
        plotmat = process(4.e+3, 1.0, gamma, alpha_0, -999)
        Qmax = np.max(plotmat[8, :])
        Qmatrix4[i // n, i % n] = Qmax
        i += 1

a0, gm = np.meshgrid(A, B)

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Plot 1
ax = axs[0, 0]
c = ax.pcolor(a0, gm, Qmatrix1, shading='auto')
fig.colorbar(c, ax=ax, label='Q_{max}')
ax.set_title('Numerical Differentiation Example')
ax.set_xlabel(r'$\alpha_0$ (t=1kyr)')
ax.set_ylabel(r'$\gamma$')
ax.set_xticklabels([])
ax.xaxis.set_ticks_position('top')
ax.tick_params(length=6)
ax.contour(a0, gm, Qmatrix1, levels=np.arange(0, np.max(Qmatrix1), 0.5), colors='white')

# Plot 2
ax = axs[0, 1]
c = ax.pcolor(a0, gm, Qmatrix2, shading='auto')
fig.colorbar(c, ax=ax, label='Q_{max}')
ax.set_xlabel(r'$\alpha_0$ (t=2kyr)')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.xaxis.set_ticks_position('top')
ax.tick_params(length=6)
ax.contour(a0, gm, Qmatrix2, levels=np.arange(0, np.max(Qmatrix2), 0.5), colors='white')

# Plot 3
ax = axs[1, 0]
c = ax.pcolor(a0, gm, Qmatrix3, shading='auto')
fig.colorbar(c, ax=ax, label='Q_{max}')
ax.set_xlabel(r'$\alpha_0$ (t=3kyr)')
ax.set_ylabel(r'$\gamma$')
ax.tick_params(length=6)
ax.contour(a0, gm, Qmatrix3, levels=np.arange(0, np.max(Qmatrix3), 0.5), colors='white')

# Plot 4
ax = axs[1, 1]
c = ax.pcolor(a0, gm, Qmatrix4, shading='auto')
fig.colorbar(c, ax=ax, label='Q_{max}')
ax.set_xlabel(r'$\alpha_0$ (t=4kyr)')
ax.set_yticklabels([])
ax.tick_params(length=6)
ax.contour(a0, gm, Qmatrix4, levels=np.arange(0, np.max(Qmatrix4), 0.5), colors='white')

plt.tight_layout()
plt.show()