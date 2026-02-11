from abc import ABC, abstractmethod
from scipy import stats
import numpy as np
import pandas as pd
from scipy.signal import fftconvolve
from models.enums_query import QueryType
import src.query as query_types
import pdb

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
        self.max_diff = 1

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
            scaled_observed = self.snap_observed(observed_value, self.size)
            snapped_scaled_observed = self.limit_observed(scaled_observed, 0, self.size)
        if type(query) == query_types.SumQuery:
            observed_value = self.limit_observed(observed_value, 0, self.size)
            snapped_scaled_observed = self.snap_observed(observed_value, 1)
        var = self.generate_updated_var(database_conf, query)
        return var.pmf(snapped_scaled_observed)

    def generate_updated_var(self, database_conf, query):
        distribution_rv = self.random_variable(1, self.p)
        var = query.discrete_likelihood(database_conf, distribution_rv)
        return var

    def threshold(self, database_conf, query, alpha):
        var = self.generate_updated_var(database_conf, query)
        if type(query) == query_types.AverageQuery or type(query) == query_types.MedianQuery:
            return var.ppf(1-alpha) / self.size
        if type(query) == query_types.SumQuery:
            return var.ppf(1-alpha) 

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
        self.p = self.normalize(p)
        self.size = size
        self.domain = list(range(10))
        self.value_type = int
        self.new_probs: None
        self.max_diff = 9

    def load_data(self, rng: np.random.Generator):
        if self.p != None:
            data = rng.choice(a=self.domain, replace=True, p=self.p, size=self.size)
        else:
            self.p = [1/len(self.domain)] * len(self.domain)
            data = rng.choice(a=self.domain, replace=True, p=self.p, size=self.size)
        return data

    def normalize(self, probabilities: list[float]):
        if probabilities != None:
            total = sum(probabilities)
            #round necessariy because of float issues
            if round(total,3) < 0:
                raise ValueError("Sum of probabilities must be atleast 1 ")

            # Normalize so they sum to 1
            probabilities = [p / total for p in probabilities]
        return probabilities 


    def select_value(self, data, added_value):
        new_data = data.copy()
        new_data[-1] = added_value
        return new_data

    def random_variable(self, size, probability):
        distribution_rv = stats.rv_discrete(values=(size, probability))
        return distribution_rv

    def query_distribution(self, probability, query_type, variance=None) :
        probability = self.new_probs
        return self.random_variable(self.domain, probability);

    def calculate_new_probabilities(self, added_value):
        p_sized = [p * self.size for p in self.p]
        p_sized[added_value] += 1
        return [p / (self.size + 1) for p in p_sized]

    def likelihood(self, database_conf, query, observed_value, sample_size=None):
        snapped_scaled_observed = observed_value
        self.new_probs = self.calculate_new_probabilities(int(database_conf.added_value))
        if type(query) == query_types.AverageQuery or type(query) == query_types.MedianQuery:
            scaled_observed = self.snap_observed(observed_value, 1)
            snapped_scaled_observed = self.limit_observed(scaled_observed, 0, max(self.domain))
            var = self.generate_updated_var(database_conf, query)
        if type(query) == query_types.SumQuery:
            observed_value = self.limit_observed(observed_value, 0, max(self.domain) * self.size)
            snapped_scaled_observed = self.snap_observed(observed_value, 1)
            single_var = self.generate_updated_var(database_conf, query)
            var = self.convolve(database_conf, single_var)

        return var.pmf(snapped_scaled_observed)

    def convolve(self, database_conf, distribution_rv):
        n = database_conf.size

        pk = np.asarray(distribution_rv.pk, dtype=float)
        pk = pk / pk.sum()

        # Compute pk convolved with itself n times (pk^{*n})
        pmf = np.array([1.0], dtype=float)  # sum of 0 variables
        base = pk.copy()
        m = n
        while m > 0:
            if m & 1:
                pmf = fftconvolve(pmf, base)
                pmf = np.clip(pmf, 0, None)   # kill tiny negative FFT noise
                pmf /= pmf.sum()
            m >>= 1
            if m:
                base = fftconvolve(base, base)
                base = np.clip(base, 0, None)
                base /= base.sum()

        support = np.arange(pmf.size)  # 0..9n
        return self.random_variable(support, pmf)

    def generate_updated_var(self, database_conf, query, sample_size=None):
        distribution_rv = self.random_variable(self.domain, self.p)
        var = query.discrete_likelihood(database_conf, distribution_rv)
        return var

    def threshold(self, database_conf, query, alpha):
        var = self.generate_updated_var(database_conf, query)
        return var.ppf(1-alpha)

    def snap_observed(self, observed_value, scale):
        snapped_scaled_observed = (round(observed_value / scale))
        return snapped_scaled_observed

    def limit_observed(self, observed_value, limit_min, limit_max):
        if observed_value > limit_max:
            observed_value = limit_max 
        if observed_value < limit_min:
            observed_value = limit_min 
        return observed_value

class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float, size: int):
        self.mean = mean
        self.std = std
        self.size = size
        self.value_type = float
        self.k_sigma_bound = 4 
        self.max_diff = 2*(self.std * self.k_sigma_bound)  

    def load_data(self, rng: np.random.Generator):
        data = np.round(rng.normal(loc=self.mean, scale=self.std, size=self.size), 3)
        a, b = self.mean - self.k_sigma_bound * self.std, self.mean + self.k_sigma_bound * self.std
        return np.clip(data, a, b)

    def random_variable(self, loc, std):
        distribution_rv = stats.norm(loc=loc, scale=std)
        return distribution_rv

    def likelihood(self, database_conf, query, observed_value):
        var = self.generate_updated_var(database_conf, query)
        return var.pdf(observed_value)
        #return query.likelihood(database_conf, distribution_rv, observed_value)

    def select_value(self, data, added_value):
        new_data = data.copy()
        new_data[-1] = added_value
        return new_data

    def query_distribution(self, loc, query_type, variance) :
        std = np.sqrt(variance)
        if query_type == QueryType.AVERAGE:
            return self.random_variable(loc, std);
        elif query_type == QueryType.MEDIAN:
            return self.random_variable(loc, std);
        elif query_type == QueryType.SUM:
            return self.random_variable(self.size*loc, self.size*std);

    def generate_updated_var(self, database_conf, query):
        distribution_rv = self.random_variable(self.mean, self.std)
        var = query.likelihood(database_conf, distribution_rv)
        return var

    def threshold(self, database_conf, query, alpha):
        var = self.generate_updated_var(database_conf, query)
        return var.ppf(1-alpha)

