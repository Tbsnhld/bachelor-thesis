from abc import ABC, abstractmethod
from models.config import Config
from src.experiment import Experiment
from src.mechanism import GaussianNoise, LaplaceNoise, Subsampling
from src.attack_model import MaximumLikelihood
from src.query import AverageQuery, MedianQuery, Query, SumQuery

class Builder(ABC):
    @abstractmethod
    def with_database(self, distribution, query, datasource, size, added_value, seed=None):
        pass

    @abstractmethod
    def with_attack_model(self, strategy):
        pass

    @abstractmethod
    def with_mechanism(self, mechanism_name, seed=None):
        pass

    @abstractmethod
    def get_experiment(self):
        pass


class ExperimentBuilder(Builder):
    experiment: Experiment

    def __init__(self):
        self.experiment_config = Config(seed=None,datasource=None, size=None, probability=None, query=None, added_values = None, mechanism=None) 
        self.experiment = Experiment()

    def with_database(self, distribution, query, datasource, size, added_values, seed=None):
        self.experiment_config = (
            self.experiment_config.with_probability(distribution)
                .with_datasource(datasource)
                .with_query(self.generate_query(query)) 
                .with_size(size)
                .with_seed(seed)
                .with_added_values(added_values)
             )
        self.experiment.set_experiment_config(self.experiment_config)
        return self


    def with_attack_model(self, strategy):
        if self.experiment_config == None:
            raise RuntimeError("Database must be configured before attack model.")
        if strategy == "maximum_likelihood":
            attack_model = MaximumLikelihood(self.experiment_config)
            self.experiment.set_attack_model(attack_model)
        else:
            raise ValueError(f"Unknown or not implemented attack model: {strategy}")
        return self

    def with_mechanism(self, mechanism_name, seed=None):
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

    def generate_query(self, query_choice:str):
        if query_choice == "Average":
            query = AverageQuery()
        elif query_choice == "Median":
            query = MedianQuery()
        elif query_choice ==  "Sum":
            query = SumQuery()
        else:
            raise ValueError(f"Wrong query type: {query_choice}")
        return query 

    def get_experiment(self):
        return self.experiment

