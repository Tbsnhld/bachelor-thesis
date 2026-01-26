from abc import ABC, abstractmethod
from models.config import Config
from models.enums_configuration_options import AttackModelOptions, DatabaseOptions, MechanismOptions, MenuOptions, QueryOptions
from src.experiment import Experiment
from src.mechanism import GaussianNoise, LaplaceNoise, PoissonSubsampling, SubsamplingWithReplacement, SubsamplingWithoutReplacement
from src.attack_model import MaximumLikelihood, LikelihoodRatioAlpha
from src.query import AverageQuery, MedianQuery, Query, SumQuery

class Builder(ABC):
    @abstractmethod
    def with_database(self, query, datasource, size, added_values, selected_database, seed=None):
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
        self.experiment_config = Config(seed=None,datasource=None, size=None, query=None, added_values = None, mechanism=None, selected_database=None) 
        self.experiment = Experiment()

    def with_database(self, query, datasource, size, added_values, selected_database, seed=None):
        self.experiment_config = (
            self.experiment_config
                .with_datasource(datasource)
                .with_query(self.generate_query(query)) 
                .with_size(size)
                .with_seed(seed)
                .with_added_values(added_values)
                .with_selected_database(selected_database)
             )
        self.experiment.set_experiment_config(self.experiment_config)
        self._rebuild_dependents()
        return self

    def with_alpha(self, alpha):
        if self.experiment.attack_model != None:
            self.experiment.attack_model.set_alpha(alpha)
        return self

    def with_attack_model(self, strategy):
        if self.experiment_config == None:
            raise RuntimeError("Database must be configured before attack model.")
        if strategy == AttackModelOptions.MAX_LIKELIHOOD.value:
            attack_model = MaximumLikelihood(self.experiment_config)
            self.experiment.set_attack_model(attack_model)
        elif strategy == AttackModelOptions.LIKELIHOOD_RATIO_ALPHA.value:
            attack_model = LikelihoodRatioAlpha(self.experiment_config)
            self.experiment.set_attack_model(attack_model)
        else:
            raise ValueError(f"Unknown or not implemented attack model: {strategy}")
        return self

    def with_mechanism(self, mechanism_name, sampling_size = None, seed=None):
        if mechanism_name == MechanismOptions.GAUSSIAN.value:
            noise = GaussianNoise(seed)
            self.experiment.set_mechanism(noise)
        elif mechanism_name == MechanismOptions.LAPLACE.value:
            noise = LaplaceNoise(seed)
            self.experiment.set_mechanism(noise)
        elif mechanism_name == MechanismOptions.SAMPLING_NO_REPLACEMENT.value:
            mechanism = SubsamplingWithoutReplacement(seed, sampling_size)
            self.experiment.set_mechanism(mechanism)
        elif mechanism_name == MechanismOptions.SAMPLING_REPLACEMENT.value:
            mechanism = SubsamplingWithReplacement(seed, sampling_size)
            self.experiment.set_mechanism(mechanism)
        elif mechanism_name == MechanismOptions.POISSONSAMPLING.value:
            mechanism = PoissonSubsampling(seed)
            self.experiment.set_mechanism(mechanism)
        else: 
            raise ValueError(f"Unknown or not implemented mechanism type: {mechanism_name}")
        return self

    def generate_query(self, query_choice:str):
        if query_choice == QueryOptions.AVERAGE.value:
            query = AverageQuery()
        elif query_choice == QueryOptions.MEDIAN.value:
            query = MedianQuery()
        elif query_choice == QueryOptions.SUM.value:
            query = SumQuery()
        else:
            raise ValueError(f"Wrong query type: {query_choice}")
        return query 

    def get_experiment(self):
        return self.experiment

    def _rebuild_dependents(self):
        self._rebuild_attack_model()

    def _rebuild_attack_model(self):
        if not self.experiment_config: 
            return

        if type(self.experiment.attack_model)  == MaximumLikelihood:
            attack_model = MaximumLikelihood(self.experiment_config)
            self.experiment.set_attack_model(attack_model)
        if type(self.experiment.attack_model)  == LikelihoodRatioAlpha:
            attack_model = LikelihoodRatioAlpha(self.experiment_config)
            self.experiment.set_attack_model(attack_model)


