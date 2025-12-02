from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np
import math
class Mechanism(ABC):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def apply_mechanism(self, data, datasize, epsilon=None, delta=None, sample_size=None, probabilities=None ) -> ndarray:
        pass

class Subsampling(Mechanism):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def apply_mechanism(self, data, datasize, epsilon=None, delta=None, sample_size=None, probabilities=None ) -> ndarray:
        if data==None:
            pass
            #throw error
        #Do Subsampling
        pass

class AdditiveNoise(Mechanism):
    @abstractmethod
    def __init__(self, seed=None):
        pass

class GaussianNoise(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def apply_mechanism(self, data, datasize, epsilon=None, delta=None, sample_size=None, probabilities=None ) -> ndarray:
        scale = calculate_scale(epsilon, datasize, delta)
        noise = self.rng.normal(0, scale=scale)
        return data + noise 


class LaplaceNoise(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def apply_mechanism(self, data, datasize, epsilon=None, delta=None, sample_size=None, probabilities=None ) -> ndarray:
        scale = calculate_scale(epsilon, datasize)
        noise = self.rng.laplace(scale=scale);
        #throw error
        #Laplace Noise
        return data + noise 

def calculate_scale(epsilon, size, delta=None) -> float:
    if delta == None or delta == 0.0:
        sensitivity = 1/size
        scale = sensitivity / epsilon
        return scale
    else:
        sensitivity = 1/size
        scale = (2*(math.log(1.25/delta))*(math.pow(sensitivity,2)))/math.pow(epsilon,2)
        return scale


