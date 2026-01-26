from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np
import math
class Mechanism(ABC):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        pass

class Subsampling(Mechanism):
    @abstractmethod
    def __init__(self, seed=None, sample_size=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class PoissonSubsampling(Subsampling):
    def __init__(self, seed=None, sample_size=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = sample_size

    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 
            #throw error

        bernoulli_decisions = self.rng.binomial(n=1, p=probabilities, size=datasize)
        subsampled_data = []
        for i in range(datasize): 
            if bernoulli_decisions[i] == 1:
                subsampled_data.append(data[i])

        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class SubsamplingWithoutReplacement(Subsampling):
    def __init__(self, seed=None, sample_size=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = sample_size

    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 
            #throw error

        subsampled_data = self.rng.choice(a=data, size=sample_size, replace=False, shuffle=False) 
        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class SubsamplingWithReplacement(Subsampling):
    def __init__(self, seed=None, sample_size=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = sample_size

    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 

        subsampled_data = self.rng.choice(a=data, size=sample_size, replace=True, shuffle=False) 
        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class AdditiveNoise(Mechanism):
    @abstractmethod
    def __init__(self, seed=None):
        pass

class GaussianNoise(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        return data
    
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        scale = self.calculate_scale(epsilon, datasize, delta)
        noise = self.rng.normal(0, scale=scale)
        return data + noise 

    def calculate_scale(self, epsilon, size, delta):
        sensitivity = 1/size
        scale = (2*(math.log(1.25/delta))*(math.pow(sensitivity,2)))/math.pow(epsilon,2)
        return scale


class LaplaceNoise(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def pre_query_mechanism(self, data, datasize, sample_size=None, probabilities=None) -> ndarray:
        return data 

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        scale = self.calculate_scale(epsilon, datasize)
        noise = self.rng.laplace(scale=scale);
        #throw error
        #Laplace Noise
        return data + noise 

    def calculate_scale(self, epsilon, size):
        sensitivity = 1/size
        scale = sensitivity / epsilon
        return scale



