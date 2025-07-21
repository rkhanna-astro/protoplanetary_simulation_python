import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 11)
y = np.sin(x / 10 * 2 * np.pi)

fig, ax = plt.subplots()
h, = ax.plot(x, y)

# Adding labels to the plot
for i, txt in enumerate(y):
    ax.annotate(f'{txt:.2f}', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.show()

