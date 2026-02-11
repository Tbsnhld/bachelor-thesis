from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np
import math
#import helper.graphic_assist as ga

class Mechanism(ABC):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
       pass 

class Subsampling(Mechanism):
    @abstractmethod
    def __init__(self, mechanism_config, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        pass

class AdditiveNoise(Mechanism):
    @abstractmethod
    def __init__(self, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        pass

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        pass

class PureStatisticalPrivacy(Mechanism):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        return data

class PoissonSubsampling(Subsampling):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed)
        self.mechanism_config = mechanism_config
        self.var = None
        self.sample_size = None

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 
            #throw error

        bernoulli_decisions = self.rng.binomial(n=1, p=self.mechanism_config[0], size=datasize)
        self.var = np.var(data)
        subsampled_data = []
        for i in range(datasize): 
            if bernoulli_decisions[i] == 1:
                subsampled_data.append(data[i])
        self.sample_size = len(subsampled_data)

        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
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

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        return data

class SubsamplingWithReplacement(Subsampling):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed)
        self.sample_size = mechanism_config[0] 
        self.util_loss = 1

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        if data.all()==None:
            raise ValueError('data is empty') 

        subsampled_data = self.rng.choice(a=data, size=self.sample_size, replace=True, shuffle=False) 
        return subsampled_data

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        return data


class AdditiveNoiseEpsilonDelta(Mechanism):
    @abstractmethod
    def __init__(self, mechanism_config, seed=None):
        pass

    @abstractmethod
    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data

    @abstractmethod
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        return data

class GaussianNoise(AdditiveNoise):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed);
        self.scale = mechanism_config[0]
        self.util_loss = self.scale*self.scale

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data
    
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        noise = self.rng.normal(0, scale=self.scale)
        return data + noise 

class GaussianNoiseEpsilonDelta(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);
        self.util_loss = None

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data
    
    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        scale = self.calculate_scale(epsilon, datasize, delta, sensitivity)
        noise = self.rng.normal(0, scale=scale)
        return data + noise 

    def calculate_scale(self, epsilon, size, delta, sensitivity):
        scale = (2*(math.log(1.25/delta))*(math.pow(sensitivity,2)))/math.pow(epsilon,2)
        self.util_loss = scale*scale
        return scale


class LaplaceNoise(AdditiveNoise):
    def __init__(self, mechanism_config, seed=None):
        self.rng = np.random.default_rng(seed);
        self.scale = mechanism_config[0]
        self.util_loss = None 

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data 

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        noise = self.rng.laplace(scale=self.scale);
        return data + noise 

class LaplaceNoiseEpsilonDelta(AdditiveNoise):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed);
        self.util_loss = None 

    def pre_query_mechanism(self, data, datasize) -> ndarray:
        return data 

    def post_query_mechanism(self, data, datasize, epsilon=None, delta=None, sensitivity=None) -> ndarray:
        scale = self.calculate_scale(epsilon, sensitivity)
        noise = self.rng.laplace(scale=scale);
        return data + noise 

    def calculate_scale(self, epsilon, sensitivity):
        scale = sensitivity / epsilon
        self.util_loss = 2*pow(scale, 2)
        return scale
