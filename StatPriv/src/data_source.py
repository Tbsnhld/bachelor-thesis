from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from scipy import stats
import numpy as np
import pandas as pd
from models.enums_query import QueryType
import src.query as query_types

class DataSource(ABC):
    @abstractmethod
    def load_data(self, rng: np.random.Generator):
        pass

    @abstractmethod
    def select_value(self, data, added_value):
        pass

    @abstractmethod
    def query_distribution(self, probability, variance):
        pass

class BernoulliSource(DataSource):
    def __init__(self,  size: int, p: float):
        self.p = p
        self.size = size
        self.domain = list(range(2))
        self.value_type= int

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
        snapped_scaled_observed = observed_value
        if type(query) == query_types.AverageQuery or type(query) == query_types.MedianQuery:
            observed_value = self.limit_observed(observed_value, 0, 1)
            snapped_scaled_observed = self.snap_observed(observed_value, self.size)
        if type(query) == query_types.SumQuery:
            observed_value = self.limit_observed(observed_value, 0, self.size)
            snapped_scaled_observed = self.snap_observed(observed_value, 1)
        distribution_rv = self.random_variable(1, self.p)
        return query.discrete_likelihood(database_conf, distribution_rv, snapped_scaled_observed)

    #Because noised observed value isn't necessarily within the support which would make the pmf return 0
    #theoretically what we're doing here is going from our bernoulli mean to the a binom mean,
    #reason being there are n bernoulli trials done, which when summed up is a binomial distribution
    def snap_observed(self, observed_value, scale):
        snapped_scaled_observed = (round(observed_value * scale))
        return snapped_scaled_observed

    def limit_observed(self, observed_value, limit_min, limit_max):
        if observed_value > limit_max:
            observed_value = limit_max 
        if observed_value < limit_min:
            observed_value = limit_min 
        return observed_value

    def query_distribution(self, probability, query_type, variance=None) :
        if query_type == QueryType.AVERAGE:
            return self.random_variable(self.size, probability)
        elif query_type == QueryType.MEDIAN:
            return self.random_variable(self.size, probability)
        elif query_type == QueryType.SUM:
            return self.random_variable(self.size, probability)


class TenSource(DataSource):
    def __init__(self, size: int, p: list[float] | None=None):
        self.p = p
        self.size = size
        self.domain = list(range(10))
        self.value_type = int
        self.new_probs: None

    def load_data(self, rng: np.random.Generator):
        if self.p != None:
            data = rng.choice(a=self.domain, replace=True, p=self.p, size=self.size)
        else:
            self.p = [1/self.size] * self.size
            data = rng.choice(a=self.domain, replace=True, p=self.p, size=self.size)
        return data

    def select_value(self, data, added_value):
        new_data = data.copy()
        #TODO: Is this needed, or even corect? 
        #removed_value = new_data[-1]
        new_data[-1] = added_value
        return new_data

    def random_variable(self, size, probability):
        distribution_rv = stats.rv_discrete(values=(size, probability))
        return distribution_rv

    def query_distribution(self, probability, query_type, variance=None) :
        probability = self.new_probs
        return self.random_variable(self.domain,probability);

    def calculate_new_probabilities(self, added_value):
        p_sized = [p * self.size for p in self.p]
        p_sized[added_value] += 1
        return [p / (self.size + 1) for p in p_sized]

    def likelihood(self, database_conf, query, observed_value):
        distribution_rv = self.random_variable(self.domain, self.p)
        self.new_probs = self.calculate_new_probabilities(database_conf.added_value)
        return query.discrete_likelihood(database_conf, distribution_rv, observed_value)


class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float, size: int):
        self.mean = mean
        self.std = std
        self.size = size
        self.domain = None
        self.value_type = float

    def load_data(self, rng: np.random.Generator):
        data = np.round(rng.normal(loc=self.mean, scale=self.std, size=self.size), 3)
        return data

    def random_variable(self, probability, std):
        distribution_rv = stats.norm(loc=probability, scale=std)
        return distribution_rv

    def likelihood(self, database_conf, query, observed_value):
        distribution_rv = self.random_variable(self.mean, self.std)
        return query.likelihood(database_conf, distribution_rv, observed_value)

    def select_value(self, data, added_value):
        new_data = data.copy()
        new_data[-1] = added_value
        return new_data

    def query_distribution(self, probability, query_type, variance) :
        std = np.sqrt(variance)
        if query_type == QueryType.AVERAGE:
            return self.random_variable(probability, std);
        elif query_type == QueryType.MEDIAN:
            return self.random_variable(probability, std);
        elif query_type == QueryType.SUM:
            return self.random_variable(probability, std);

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
