import numpy as np
import cmath as math

j_counts = 6
l = 6
delta = np.sqrt(.1)


L = 2 * l + 1
gamma = 1 / (np.cos((1/L) * math.acos(1/delta)))
alphas = []
betas = np.zeros(j_counts)
print(gamma)

for j in range(1, j_counts + 1):
    alphas.append((2 * ((np.pi / 2) -  math.atan(math.tan(2 * np.pi * j / L) * math.sqrt(1 - gamma**2)))).real)
    betas[l - j] = -1 * alphas[j-1]
print(betas)