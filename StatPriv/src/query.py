from abc import ABC, abstractmethod
from scipy import stats
from models.enums import DataSourceType
from src.data_source import BernoulliSource
import numpy as np

class Query(ABC):
    @abstractmethod
    def execute(self, data):
        pass

    @abstractmethod
    def likelihood(self, database, distribution_rv, observed_value):
        pass

    def calculate_expected_gaussian(self, mean, var, size): 
        std = np.sqrt(var)
        std_expected_answer = std/np.sqrt(size)
        return stats.norm(loc=mean, scale=np.sqrt(var))

class AverageQuery(Query):
    #data: Generated numpy data
    def execute(self, data):
        return sum(data) / len(data)

    #data: scipy stats generated data
    def likelihood(self, database_conf, distribution_rv, observed_value):
        size = database_conf.size
        rv_mean = distribution_rv.mean()
        adversary_mean = (round((size - 1) * rv_mean) + int(database_conf.added_value)) / size
        adversary_variance = self.variance(database_conf, distribution_rv) 

        clt_mean_rv = self.calculate_expected_value(adversary_mean, adversary_variance)
        return clt_mean_rv.pdf(observed_value) 

    def discrete_likelihood(self, database_conf, distribution_rv, observed_value):
        size = database_conf.size
        rv_mean = distribution_rv.mean() 
        adversary_mean = (round((size - 1) * rv_mean) + int(database_conf.added_value)) / size

        var = database_conf.datasource.query_distribution(adversary_mean)
        return var.pmf(observed_value) 
    
    def mean(self, database_conf, distribution_rv):
        rv_mean = distribution_rv.mean()
        adversary_mean = ((database_conf.size - 1) * rv_mean + int(database_conf.added_value)) / database_conf.size
        return adversary_mean

    def variance(self, database_conf, distribution_rv):
        rv_mean = distribution_rv.mean()
        adversary_mean = self.mean(database_conf, distribution_rv)
        var = distribution_rv.var()
        original_contrib = (database_conf.size - 1) * (var + (rv_mean - adversary_mean)**2)
        outlier_contrib = (database_conf.added_value - adversary_mean)**2
        adversary_variance = (original_contrib + outlier_contrib) / database_conf.size
        return adversary_variance

    def calculate_expected_gaussian(self, mean, var, size): 
        return super().calculate_expected_gaussian(mean, var, size)

class MedianQuery(Query):
    def execute(self, data):
        return data[len(data)/2]

    def likelihood(self, database_conf, distribution_rv, observed_value):
        median = distribution_rv.ppf(0.5)
        size = database_conf.size
        adversary_median = ((size - 1) * median + int(database_conf.added_value)) / size 
        clt_rv = self.central_limit_theorem_variable(adversary_median)
        return clt_rv.pdf(observed_value) 

    def mean(self, database_conf, distribution_rv):
        rv_mean = distribution_rv.mean()
        adversary_mean = ((database_conf.size - 1) * rv_mean + int(database_conf.added_value)) / database_conf.size
        return adversary_mean

    def variance(self, database_conf, distribution_rv):
        rv_mean = distribution_rv.mean()
        adversary_mean = self.mean(database_conf, distribution_rv)
        var = distribution_rv.var()
        original_contrib = (database_conf.size - 1) * (var + (rv_mean - adversary_mean)**2)
        outlier_contrib = (database_conf.added_value - adversary_mean)**2
        adversary_variance = (original_contrib + outlier_contrib) / database_conf.size
        return adversary_variance

    def central_limit_theorem_variable(self, mean): 
        return super().central_limit_theorem_variable(mean)
    
class SumQuery(Query):
    def __init__(self):
        self.size 
    
    def execute(self, data):
        self.size = len(data)
        return sum(data)

    def likelihood(self, database_conf, distribution_rv, observed_value):
        mean = distribution_rv.mean()
        size = database_conf.size
        guessed_sum = ((size - 1) * mean + int(database_conf.added_value))
        clt_rv = self.central_limit_theorem_variable(guessed_sum)
        return clt_rv.pdf(observed_value) 

    def central_limit_theorem_variable(self, mean): 
        return super().central_limit_theorem_variable(mean)

