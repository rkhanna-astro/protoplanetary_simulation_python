import numpy as np
import matplotlib.pyplot as plt
import process

# Grid size
m = 20  # 20x20
n = 20
gamma = 1.05  # change to 1.1 if needed

A = np.arange(0.3, 0.8 + 0.025, 0.025)
print("alpha", A)
m = len(A)
B = np.arange(1.0, 1.1 + 0.005, 0.005)
print("timespace", B)
n = len(B)
eta = 0.01

Qmatrix1 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | eta = {eta}')
        plotmat = process.process(1.e+3, 1.0, gamma, alpha_0, eta, -999)
        Qmean = np.mean(plotmat[8, :])
        Qmatrix1[i // n, i % n] = Qmean
        i += 1

Qmatrix2 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | eta = {eta}')
        plotmat = process.process(2.e+3, 1.0, gamma, alpha_0, eta, -999)
        Qmean = np.mean(plotmat[8, :])
        Qmatrix2[i // n, i % n] = Qmean
        i += 1

Qmatrix3 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | eta = {eta}')
        plotmat = process.process(3.e+3, 1.0, gamma, alpha_0, eta, -999)
        Qmean = np.mean(plotmat[8, :])
        Qmatrix3[i // n, i % n] = Qmean
        i += 1

Qmatrix4 = np.zeros((m, n))
i = 0
for alpha_0 in A:
    for gamma in B:
        print(f'i = {i + 1} | alpha_0 = {alpha_0} | eta = {eta}')
        plotmat = process.process(4.e+3, 1.0, gamma, alpha_0, eta, -999)
        Qmean = np.mean(plotmat[8, :])
        Qmatrix4[i // n, i % n] = Qmean
        i += 1


print("lengths", A.shape, B.shape)
print("Qmatrix", Qmatrix1.shape)

a0, gm = np.meshgrid(A, B, indexing='ij')

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Plot 1
ax = axs[0, 0]
c = ax.pcolormesh(a0, gm, Qmatrix1, shading='auto')
fig.colorbar(c, ax=ax, label='Q_mean')
ax.set_xlabel(r'$\alpha_0$ (t=1kyr)')
ax.set_ylabel(r'$\gamma$')
ax.set_xticklabels([])
ax.xaxis.set_ticks_position('top')
ax.tick_params(length=6)
contour = ax.contour(a0, gm, Qmatrix1, levels=np.arange(0, np.max(Qmatrix1), 0.5), colors='white')
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')  # Label all contours

# Plot 2
ax = axs[0, 1]
c = ax.pcolor(a0, gm, Qmatrix2, shading='auto')
fig.colorbar(c, ax=ax, label='Q_mean')
ax.set_xlabel(r'$\alpha_0$ (t=2kyr)')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.xaxis.set_ticks_position('top')
ax.tick_params(length=6)
contour = ax.contour(a0, gm, Qmatrix2, levels=np.arange(0, np.max(Qmatrix2), 0.5), colors='white')
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')  # Label all contours



# Plot 3
ax = axs[1, 0]
c = ax.pcolor(a0, gm, Qmatrix3, shading='auto')
fig.colorbar(c, ax=ax, label='Q_mean')
ax.set_xlabel(r'$\alpha_0$ (t=3kyr)')
ax.set_ylabel(r'$\gamma$')
ax.tick_params(length=6)
contour = ax.contour(a0, gm, Qmatrix3, levels=np.arange(0, np.max(Qmatrix3), 0.5), colors='white')
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')  # Label all contours


# Plot 4
ax = axs[1, 1]
c = ax.pcolor(a0, gm, Qmatrix4, shading='auto')
fig.colorbar(c, ax=ax, label='Q_mean')
ax.set_xlabel(r'$\alpha_0$ (t=4kyr)')
ax.set_yticklabels([])
ax.tick_params(length=6)
contour = ax.contour(a0, gm, Qmatrix4, levels=np.arange(0, np.max(Qmatrix4), 0.5), colors='white')
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')  # Label all contours


plt.tight_layout()
plt.show()

fig.savefig('gridalpha0eta.pdf', format='pdf')
