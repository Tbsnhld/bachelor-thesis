import numpy as np
import matplotlib.pyplot as plt

def distribution(distribution):
    plt.figure()
    plt.hist(distribution, bins=50, density=True, alpha=0.7)

    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.title("Created Distribution")
    plt.show()

