import numpy as np
from abc import ABC, abstractmethod
from models.config import Config
from models.database_configuration import DatabaseConfig
from src.data_source import BernoulliSource
from src.query import AverageQuery
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
        threshold = self.calculate_threshold(likelihood_ratio)

        if likelihood_ratio >= threshold:
            return int(0)
        elif likelihood_ratio < threshold:
            return int(1)

    def likelihood(self, database, observed_value):
        return self.config.datasource.likelihood(database.db_config, database.db_config.query, observed_value)
                       
    def likelihood_ratio(self, h0_li, h1_li):
        ratio = h0_li/h1_li
        return ratio

    def calculate_threshold(self, likelihood_ratio):
        return np.quantile(likelihood_ratio, 1 - self.alpha)

    def set_alpha(self, value):
        self.alpha = value
