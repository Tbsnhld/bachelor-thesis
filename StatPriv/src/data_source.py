from abc import ABC, abstractmethod
from scipy import stats
import numpy as np
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def load_data(self, rng: np.random.Generator):
        pass

    @abstractmethod
    def select_value(self, data, added_value):
        pass

class BernoulliSource(DataSource):
    def __init__(self,  size: int, p: float):
        self.p = p
        self.size = size
        self.domain = list(range(2))

    def load_data(self, rng: np.random.Generator):
        data = rng.binomial(n=1, p=self.p, size=self.size)
        return data

    def select_value(self, data, added_value):
        new_data = data.copy()
        new_data[-1] = added_value
        return new_data

    def random_variable(self, size, probability):
        distribution_rv = stats.binom(n=size, p=probability)
        return distribution_rv

    def likelihood(self, database_conf, query, observed_value):
        snapped_observed = self.snap_observed(observed_value)
        distribution_rv = self.random_variable(1, self.p)
        return query.discrete_likelihood(database_conf, distribution_rv, snapped_observed)

    #Because noised observed value isn't necessarily within the support which would make the pmf return 0
    #theoretically what we're doing here is going from our bernoulli mean to the a binom mean,
    #reason being there are n bernoulli trials done, which when summed up is a binomial distribution
    def snap_observed(self, observed_value):
        snapped_observed = (round(observed_value * self.size))
        return snapped_observed

    def query_distribution(self, probability):
        return self.random_variable(self.size, probability);


class TenSource(DataSource):
    def __init__(self, size: int, p: (float)|None=None):
        self.p = p
        self.size = size
        self.domain = list(range(10))

    def variance(self):
        # Compute the mean
        mean = np.sum(self.p * self.domain)
        # Compute the variance
        var = np.sum(self.p * (self.domain - mean)**2)
        return var

    def load_data(self, rng: np.random.Generator):
        if self.p != None:
            data = rng.choice(a=self.domain, replace=True, p=self.p)
        else:
            data = rng.choice(a=self.domain, replace=True)
        return data

    def select_value(self, data, added_value):
        size = data.size
        new_data = data.copy()
        new_data = np.put(new_data, [size - 1], added_value)
        return new_data

class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float, size: int):
        self.mean = mean
        self.std = std
        self.size = size
        self.domain = None

    def load_data(self, rng: np.random.Generator):
        data = np.round(rng.normal(loc=self.mean, scale=self.std, size=self.size), 3)
        return data

    def random_variable(self):
        distribution_rv = stats.norm(loc=self.mean, scale=self.std)
        return distribution_rv

    def likelihood(self, database_conf, query, observed_value):
        distribution_rv = self.random_variable()
        return query.likelihood(database_conf, distribution_rv, observed_value)

    def select_value(self, data, added_value):
        new_data = data.copy()
        new_data[-1] = added_value
        return new_data

class CSVSource(DataSource):
    def __init__(self, filepath: str, column: str | None = None):
        self.filepath = filepath
        self.column = column

    def load_data(self, rng: np.random.Generator, size: int | None = None):
        ds = pd.read_csv(self.filepath)
        if self.column:
            self.data = ds[self.column]
        else:
            self.data = ds.select_dtypes(include='number').to_numpy()

        if size and len(self.data) > size:
            self.data = self.data[:size]
        return self.data
