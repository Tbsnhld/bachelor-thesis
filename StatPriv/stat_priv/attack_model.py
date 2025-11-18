from abc import ABC, abstractmethod
from config import Config
class AttackModel(ABC):
   @abstractmethod
   def run(self)-> bool:
       pass


class MaximumLikelihood(AttackModel):
    def __init__(self, database_config: Config):
        self.database_config = database_config

    def run(self, mechanismed_data) -> bool:
        size = self.database_config.size
        probability = self.database_config.probability 
        return True
