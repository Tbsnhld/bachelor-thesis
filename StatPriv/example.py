import numpy as np

rng = np.random.default_rng()
n, p, size = 1, .5, 15
s = rng.binomial(n, p, size)

print(s)

