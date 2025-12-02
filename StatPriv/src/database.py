import numpy as np
from numpy.random import normal
from src.config import Config
from src.mechanism import Mechanism

class Database:
    def __init__(self, config: Config) -> None:
        self.rng = np.random.default_rng(config.seed)
        self.config = config
        self.datasource = config.datasource
        self.data = self.datasource.load_data(self.rng, added_value=config.added_value, size=config.size)

#    def generate_data(self, n, p):
#        self.propability = p
#        self.data = self.rng.binomial(1, p, size=n);
#        self.data_size = n
#        self.data_p = p

#    def apply_mechanism(self, mechanism: Mechanism):
#        return mechanism.apply_mechanism(self.data)

#    def apply_gaussian_noise(self, psi):
#        noise = self.rng.normal(0, scale=psi, size=len(self.data))
#        return self.data + noise
#
#    def apply_laplace_noise(self, psi):
#        noise = self.rng.laplace(scale=psi, size=len(self.data));
#        return self.data + noise;
#
#    def apply_subsampling(self, m=None, p=None):
#        if m is None or m > (0.05 * self.data_size):
#            raise ValueError('You need to pass a samplesize, which should be m<=0.05n')
#        samples = self.rng.choice(a=self.data, size=m)
#        return samples
        

    def reseed(self, seed=None):
        self.rng = np.random.default_rng(seed=seed)

    def get_data(self):
        return self.data;

    def run_query(self):
        return self.config.query.execute(self.data)
