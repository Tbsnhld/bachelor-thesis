import numpy as np
from abc import ABC, abstractmethod
from models.config import Config
from models.database_configuration import DatabaseConfig
from src import mechanism
from src.data_source import BernoulliSource
from src.query import AverageQuery, Query, SumQuery
class AttackModel(ABC):
   @abstractmethod
   def run(self, observed_answer, databases) -> int:
       pass

class MaximumLikelihood(AttackModel):
    def __init__(self, config: Config):
        self.config = config 

    def run(self, observed_answer, databases) -> int:
        h0_database = databases[0]
        h1_database = databases[1]
        
        h0_li = self.likelihood(h0_database, observed_answer)
        h1_li = self.likelihood(h1_database, observed_answer)

        if self.likelihood_ratio(h0_li, h1_li) >= 1:
            return int(0)
        elif self.likelihood_ratio(h0_li, h1_li) < 1:
            return int(1)

    def likelihood(self, database, observed_value):
        return self.config.datasource.likelihood(database.db_config, database.db_config.query, observed_value)
                       
    def likelihood_ratio(self, h0_li, h1_li):
        ratio = h0_li/h1_li
        return ratio

class LikelihoodRatioAlpha(AttackModel):
    def __init__(self, config: Config):
        self.config = config 
        self.alpha = 0  

    def run(self, observed_answer, databases) -> int:
        h0_database = databases[0]
        h1_database = databases[1]
        
        h0_li = self.likelihood(h0_database, observed_answer)
        h1_li = self.likelihood(h1_database, observed_answer)
        likelihood_ratio = self.likelihood_ratio(h0_li, h1_li)
        threshold = self.calculate_threshold(h0_database, self.alpha)
        h0_threshold_li = self.likelihood(h0_database, threshold)
        h1_threshold_li = self.likelihood(h1_database, threshold)
        threshold_ratio = self.likelihood_ratio(h0_threshold_li, h1_threshold_li)

        if likelihood_ratio >= threshold_ratio:
            return int(0)
        elif likelihood_ratio < threshold_ratio:
            return int(1)

    def likelihood(self, database, observed_value):
        if database.db_config.query == type(SumQuery):
            observed_value = (observed_value * self.config.size)/ self.config.mechanism.sample_size
        return self.config.datasource.likelihood(database.db_config, database.db_config.query, observed_value)
                       
    def likelihood_ratio(self, h0_li, h1_li):
        ratio = h0_li/h1_li
        return ratio

    def calculate_threshold(self, database, alpha):
        threshold = self.config.datasource.threshold(database.db_config, database.db_config.query, alpha)
        return threshold 

    def set_alpha(self, value):
        self.alpha = value
