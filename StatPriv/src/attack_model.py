from abc import ABC, abstractmethod
from models.config import Config
from src.data_source import BernoulliSource
from src.query import AverageQuery
class AttackModel(ABC):
   @abstractmethod
   def run(self, observed_answer)-> int:
       pass

class MaximumLikelihood(AttackModel):
    def __init__(self, database_config: Config):
        self.database_config = database_config

    def run(self, observed_answer, databases) -> int:
        probability = self.database_config.probability 
        datasource = self.database_config.datasource
        query = self.database_config.query
        if type(query) == AverageQuery and type(datasource) == BernoulliSource:
            print(f"observed answer: {observed_answer}")
            if observed_answer >= probability:
                return 1
            elif observed_answer < probability:
                return 0
        else:
            raise ValueError(f"Currently not able to calculate anything but Average for Bernoulli")
        

    def likelihood(self, observed_answer):
    #   domain = self.database_config.datasource.domain
    #   size = self.database_config.size
        pass
                       
