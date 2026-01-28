from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np
import math
class Mechanism(ABC):
    @abstractmethod
    def __init__(self, seed=None):
        pass

class Subsampling(Mechanism):
    @abstractmethod
    def __init__(self, mechanism_config, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class PoissonSubsampling(Subsampling):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed)
        self.mechanism_config = mechanism_config

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 
            #throw error

        bernoulli_decisions = self.rng.binomial(n=1, p=self.mechanism_config[0], size=datasize)
        subsampled_data = []
        for i in range(datasize): 
            if bernoulli_decisions[i] == 1:
                subsampled_data.append(data[i])
        self.sample_size = len(subsampled_data)

        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        if self.sample_size == 0:
            self.sample_size = 1
        return data

class SubsamplingWithoutReplacement(Subsampling):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = mechanism_config[0]

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 
            #throw error

        subsampled_data = self.rng.choice(a=data, size=self.sample_size, replace=False, shuffle=False) 
        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class SubsamplingWithReplacement(Subsampling):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = mechanism_config[0] 

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 

        subsampled_data = self.rng.choice(a=data, size=self.sample_size, replace=True, shuffle=False) 
        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class AdditiveNoise(Mechanism):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class AdditiveNoiseEpsilonDelta(Mechanism):
    @abstractmethod
    def __init__(self, mechanism_config, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        return data

class GaussianNoise(AdditiveNoise):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed);
        self.mechanism_config = mechanism_config

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data
    
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, probabilities=None) -> ndarray:
        noise = self.rng.normal(self.mechanism_config[0], scale=self.mechanism_config[1])
        return data + noise 

class GaussianNoiseEpsilonDelta(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def pre_query_mechanism(self, data, datasize) -> ndarray:
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
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed);
        self.mechanism_config = mechanism_config

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data 

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None) -> ndarray:
        noise = self.rng.laplace(scale=self.mechanism_config[0]);
        return data + noise 

class LaplaceNoiseEpsilonDelta(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data 

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None) -> ndarray:
        scale = self.calculate_scale(epsilon, datasize)
        noise = self.rng.laplace(scale=scale);
        return data + noise 

    def calculate_scale(self, epsilon, size):
        sensitivity = 1/size
        scale = sensitivity / epsilon
        return scale




