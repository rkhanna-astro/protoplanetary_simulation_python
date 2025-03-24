import numpy as np
import matplotlib.pyplot as plt

# Define the function f(x, y) = x^3 - 2y^2 - 3x over x=[-2, 2], y=[-1, 1]
x = np.arange(-2, 2.1, 0.1)
y = np.arange(-1, 1.1, 0.1)
X, Y = np.meshgrid(x, y)
Z = X**3 - 2*Y**2 - 3*X

# Gradient of f
dX, dY = np.gradient(Z, 0.1, 0.1)

# Plot the vector field and contour levels
plt.figure()
plt.quiver(X, Y, dX, dY)
plt.contour(X, Y, Z, 10)
plt.axis('equal')
plt.axis([-2, 2, -1, 1])
plt.title('Vector Field and Contour Levels')
plt.show()

# Plot surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.contour(X, Y, Z, 10, offset=np.min(Z), cmap='viridis')
ax.view_init(30, 120)
plt.title('Surface Plot')
plt.show()
