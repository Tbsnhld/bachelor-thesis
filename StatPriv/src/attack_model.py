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
        datasource = self.config.datasource
        query = self.config.query

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
