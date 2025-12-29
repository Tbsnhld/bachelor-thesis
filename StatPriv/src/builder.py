from abc import ABC, abstractmethod
from models.config import Config
from src.experiment import Experiment
from src.mechanism import GaussianNoise, LaplaceNoise, Subsampling
from src.attack_model import MaximumLikelihood
from src.query import AverageQuery, Query, SumQuery

class Builder(ABC):
    @abstractmethod
    def withDatabase(self, distribution, query, datasource, size, added_value, seed=None):
        pass

    @abstractmethod
    def withAttackModel(self, strategy):
        pass

    @abstractmethod
    def withMechanism(self, mechanism_name, seed=None):
        pass

    @abstractmethod
    def getExperiment(self):
        pass


class ExperimentBuilder(Builder):
    experiment: Experiment

    def __init__(self):
        self._database_config = Config(seed=None,datasource=None, size=None, probability=None, query=None, added_values = None, searched_database = None) 
        self.experiment = Experiment()

    def withDatabase(self, distribution, query, datasource, size, added_values, searched_database, seed=None):
        self._database_config.probability = distribution 
        self._database_config.datasource = datasource
        self._database_config.query = self.generate_Query(query) 
        self._database_config.size = size
        self._database_config.seed = seed
        self._database_config.added_values = added_values
        self._database_config.searched_database = searched_database 
        self.experiment.set_database_config(self._database_config)
        return self


    def withAttackModel(self, strategy):
        if self._database_config == None:
            raise RuntimeError("Database Config must be build before attack model.")
        if strategy == "maximum_likelihood":
            attack_model = MaximumLikelihood(self._database_config)
            self.experiment.set_attack_model(attack_model)
        else:
            raise ValueError(f"Unknown or not implemented attack model: {strategy}")
        return self

    def withMechanism(self, mechanism_name, seed=None):
        if mechanism_name == "gaussian":
            noise = GaussianNoise(seed)
            self.experiment.set_mechanism(noise)
        elif mechanism_name == "laplace":
            noise = LaplaceNoise(seed)
            self.experiment.set_mechanism(noise)
        elif mechanism_name == "subsampling":
            raise ValueError(f"Unknown or not implemented mechanism type: {mechanism_name}")
        else: 
            raise ValueError(f"Unknown or not implemented mechanism type: {mechanism_name}")
        return self

    def generate_Query(self, query_choice:str):
        if query_choice == "Average":
            query = AverageQuery()
        elif query_choice ==  "Sum":
            query = SumQuery()
        else:
            raise ValueError(f"Wrong query type: {query_choice}")
        return query 


    def getExperiment(self):
        return self.experiment

