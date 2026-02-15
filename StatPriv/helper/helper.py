from models.config import Config
from models.database_configuration import DatabaseConfig
from models.enums_configuration_options import AttackModelOptions, DatabaseOptions
from models.enums_data_source import DataSourceType
from models.enums_mechanism import MechanismType
from models.enums_query import QueryType
from src.attack_model import LikelihoodRatioAlpha, MaximumLikelihood
from src.builder import ExperimentBuilder
from src.data_source import BernoulliSource, GaussianSource, TenSource
from src.database_generator import DatabaseGenerator
from src.experiment import Experiment
from src.mechanism import (
    GaussianNoise,
    LaplaceNoise,
    LaplaceNoiseEpsilonDelta,
    PoissonSubsampling,
    PureStatisticalPrivacy,
    SubsamplingWithoutReplacement,
    SubsamplingWithReplacement,
)
from src.observer import DataGeneratorObserver, SuccessRateObserver
from src.query import AverageQuery, MedianQuery, SumQuery
from src.simulator import MonteCarlo


# ------------------------
# Query factory
# ------------------------

def make_query(query_type: QueryType | None = QueryType.AVERAGE): 
    if query_type == QueryType.AVERAGE:
        return AverageQuery()
    elif query_type == QueryType.MEDIAN:
        return MedianQuery()
    elif query_type == QueryType.SUM:
        return SumQuery()
    else:
        raise ValueError(f"Unknown query type: {query_type}")


# ------------------------
# Datasource factory
# ------------------------

def make_datasource(
    source_type: str | DataSourceType | DatabaseOptions = "Gaussian",
    size: int = 50,
    probability: float | None = 0.5,
    probabilities: list[float] | None = None,
    mean: float | None = 150,
    std: float | None = 13,
):
    if isinstance(source_type, DataSourceType):
        source_type = source_type.name
    if isinstance(source_type, DatabaseOptions):
        source_type = source_type.name

    if source_type in ("Bernoulli", "BINARY"):
        return BernoulliSource(size, probability)
    if source_type in ("TenSource", "RANDOMONETEN"):
        if probabilities is None:
            probabilities = [1 / 10] * 10
        return TenSource(size=size, p=probabilities)
    if source_type in ("Gaussian", "GAUSSIAN"):
        return GaussianSource(mean=mean, std=std, size=size)
    raise ValueError(f"Unknown datasource type: {source_type}")


# ------------------------
# Config factory
# ------------------------

def make_config(
    added_values=None,
    size: int = 50,
    probability: float | None = 0.5,
    probabilities: list[float] | None = None,
    mean: float | None = 150,
    std: float | None = 13,
    seed: int | None = 1234,
    attack_type: str | None=AttackModelOptions.MAX_LIKELIHOOD.value,
    alpha: float | None=0.5
):
    if added_values is None:
        added_values = [0, 50]
    return (
        Config(
            seed=seed, 
            added_values=added_values, 
            datasource=None, 
            size=size, 
            mechanism=None,
            query=None,
            attack_type=attack_type,
            alpha=alpha,
            sensitivity=None)
        .with_datasource(
            make_datasource(
                size=size,
                probability=probability,
                probabilities=probabilities,
                mean=mean,
                std=std,
            )
        )
        .with_query(make_query())
    )


# ------------------------
# DatabaseConfig factory
# ------------------------

def make_database_config(
    added_value=None,
    size: int = 50,
    seed: int | None = 1234
):
    if added_value is None:
        added_value = [0, 50]
    return DatabaseConfig(
        seed=seed,
        query=make_query(),
        datasource=make_datasource(size=size),
        added_value=added_value,
        size=size,
    )


# ------------------------
# Generator factory
# ------------------------

def make_database_generator(config: Config):
    return DatabaseGenerator(config)


# ------------------------
# Mechanism factory
# ------------------------

def make_mechanism(mechanism_config, mechanism_type=MechanismType.GAUSSIAN, seed=None):
    if mechanism_type == MechanismType.GAUSSIAN:
        return GaussianNoise(mechanism_config, seed)
    if mechanism_type == MechanismType.LAPLACE:
        return LaplaceNoise(mechanism_config, seed)
    if mechanism_type == MechanismType.SUBSAMPLING:
        return SubsamplingWithoutReplacement(mechanism_config, seed)
    if mechanism_type == MechanismType.LAPLACE_EPSILON:
       return LaplaceNoiseEpsilonDelta(seed)
    if mechanism_type == MechanismType.SUBSAMPLING_REPLACEMENT:
        return SubsamplingWithReplacement(mechanism_config, seed)
    if mechanism_type == MechanismType.POISSON_SUBSAMPLING:
        return PoissonSubsampling(mechanism_config, seed)
    if mechanism_type == MechanismType.PURE_STATISTICAL_PRIVACY:
        return PureStatisticalPrivacy(seed)
    else:
        raise ValueError(f"Unknown query type: {mechanism_type}")


# ------------------------
# Attack model factory
# ------------------------

def make_attack_model(config: Config, attack_type: str | AttackModelOptions):
    if isinstance(attack_type, AttackModelOptions):
        attack_type = attack_type.value
    if attack_type == AttackModelOptions.MAX_LIKELIHOOD.value:
        return MaximumLikelihood(config)
    if attack_type == AttackModelOptions.LIKELIHOOD_RATIO_ALPHA.value:
        return LikelihoodRatioAlpha(config)
    raise ValueError(f"Unknown attack model type: {attack_type}")


# ------------------------
# Experiment factory
# ------------------------

def make_experiment(
    config: Config,
    mechanism,
    attack_model=None,
    epsilon=None,
    delta=None,
):
    experiment = Experiment()
    experiment.set_experiment_config(config)
    experiment.set_mechanism(mechanism)
    if attack_model is not None:
        experiment.set_attack_model(attack_model)
    if epsilon is not None:
        experiment.set_epsilon(epsilon)
    if delta is not None:
        experiment.set_delta(delta)
    return experiment


# ------------------------
# Builder factory
# ------------------------

def make_builder():
    return ExperimentBuilder()


# ------------------------
# Simulator factory
# ------------------------

def make_simulator(count: int, experiment: Experiment, observers=None):
    simulator = MonteCarlo(count, experiment)
    if observers:
        simulator.add_observers(observers)
    return simulator


# ------------------------
# Observer factory
# ------------------------

def make_observers(csv_filename: str | None = None):
    observers = [] 
    observer = SuccessRateObserver()
    observers.append(observer)
    if csv_filename:
        observers.append(DataGeneratorObserver(csv_filename))
    return observers
