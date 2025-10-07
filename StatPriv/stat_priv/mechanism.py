from abc import ABC, abstractmethod, abstractproperty, property
class Mechanism(ABC):
    @abstractmethod
    def apply_mechanism(self, data=None, result=None):
        pass

class Subsampling(Mechanism):
    def apply_mechanism(self, data, result=None) -> ndarray:
        if data==None:
            pass
            #throw error
        #Do Subsampling
        return None

class AdditiveNoise(Mechanism):
    @property
    @abstractmethod
    def loc(self):
        pass

    @property
    @abstractmethod
    def scale(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

class GaussianNoise(AdditiveNoise):
    def apply_mechanism(self, data=None, result):
        if result==None:
            pass
        #throw error
        #Gaussian GaussianNoise
        return None


class LaplaceNoise(AdditiveNoise):
    def apply_mechanism(self, data=None, result):
        if result==None:
            pass
        #throw error
        #Laplace Noise
        return None




