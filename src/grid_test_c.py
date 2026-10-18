
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
        plotmat = process(2.e+3, 1.0, gamma, alpha_0, -999)
        Qmax = np.mean(plotmat[8, :])
        Qmatrix1[i // n, i % n] = Qmax
        i += 1

a0, gm = np.meshgrid(A, B)

fig, ax = plt.subplots(figsize=(10, 8))

# Plot 1
c = ax.pcolor(a0, gm, Qmatrix1, shading='auto')
cb = fig.colorbar(c, ax=ax)
cb.set_label('Q_{max}')
cb.set_position([.8314, .11, .0581, .8150])

FontSize = 18
FontName = 'MyriadPro-Regular'  # or choose any other font
ax.set_xlabel(r'$\alpha$ (t=1kyr)', fontsize=FontSize, fontname=FontName)
ax.set_ylabel(r'$\gamma$', fontsize=FontSize, fontname=FontName)

ax.contour(a0, gm, Qmatrix1, levels=np.arange(0, np.max(Qmatrix1), 0.5), colors='white')

plt.tight_layout()
plt.show()

fig.savefig('grid1.eps', format='eps')