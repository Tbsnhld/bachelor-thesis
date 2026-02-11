from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Callable, Iterable, List
import inspect

from helper import helper as h
from models.enums_configuration_options import AttackModelOptions, MechanismOptions, QueryOptions, DatabaseOptions
from models.enums_data_source import DataSourceType
from models.enums_mechanism import MechanismType
from models.enums_query import QueryType
from src.observer import DataGeneratorObserver, SuccessRateObserver


@dataclass(frozen=True)
class ExperimentRunConfig:
    datasource: Any | None
    datasource_factory: Callable[..., Any] | None
    size: int
    query: Any | None
    h0_value: Any
    h1_value: Any 
    attack_model: Any | None
    mechanism: Any | None
    mechanism_config: list[Any] | None
    alpha: float | None
    epsilon: float | None
    delta: float | None
    seed: int | None
    mechanism_seed: int | None
    datasource_type: str | None = None
    probability: float | None = None
    probabilities: list[float] | None = None
    mean: float | None = None
    std: float | None = None


@dataclass(frozen=True)
class SweepResult:
    varied_name: str
    varied_value: Any
    success_rate: float
    advantage: float


def _resolve_query(query: Any | None):
    if query is None:
        return h.make_query(QueryType.AVERAGE)
    if isinstance(query, QueryOptions):
        if query == QueryOptions.AVERAGE:
            query_gen = h.make_query(QueryType.AVERAGE) 
            return query_gen 
        if query == QueryOptions.MEDIAN:
            query_gen = h.make_query(QueryType.MEDIAN) 
            return query_gen 
        if query == QueryOptions.SUM:
            query_gen = h.make_query(QueryType.SUM) 
            return query_gen 
    if isinstance(query, QueryType):
        return h.make_query(query)
    return query


def _resolve_mechanism_type(mechanism: Any | None) -> MechanismType:
    if isinstance(mechanism, MechanismType):
        return mechanism
    if isinstance(mechanism, MechanismOptions):
        mapping = {
            MechanismOptions.GAUSSIAN: MechanismType.GAUSSIAN,
            MechanismOptions.GAUSSIAN_EPSILON: MechanismType.GAUSSIAN_EPSILON,
            MechanismOptions.LAPLACE: MechanismType.LAPLACE,
            MechanismOptions.LAPLACE_EPSILON: MechanismType.LAPLACE_EPSILON,
            MechanismOptions.SAMPLING_NO_REPLACEMENT: MechanismType.SUBSAMPLING,
            MechanismOptions.SAMPLING_REPLACEMENT: MechanismType.SUBSAMPLING_REPLACEMENT,
            MechanismOptions.POISSONSAMPLING: MechanismType.POISSON_SUBSAMPLING,
            MechanismOptions.PURE_STATISTICAL_PRIVACY: MechanismType.PURE_STATISTICAL_PRIVACY,
        }
        if mechanism in mapping:
            return mapping[mechanism]
    if isinstance(mechanism, str):
        by_value = {
            MechanismOptions.GAUSSIAN.value: MechanismType.GAUSSIAN,
            MechanismOptions.GAUSSIAN_EPSILON.value: MechanismType.GAUSSIAN_EPSILON,
            MechanismOptions.LAPLACE.value: MechanismType.LAPLACE,
            MechanismOptions.LAPLACE_EPSILON.value: MechanismType.LAPLACE_EPSILON,
            MechanismOptions.SAMPLING_NO_REPLACEMENT.value: MechanismType.SUBSAMPLING,
            MechanismOptions.SAMPLING_REPLACEMENT.value: MechanismType.SUBSAMPLING_REPLACEMENT,
            MechanismOptions.POISSONSAMPLING.value: MechanismType.POISSON_SUBSAMPLING,
            MechanismOptions.PURE_STATISTICAL_PRIVACY.value: MechanismType.PURE_STATISTICAL_PRIVACY,
        }
        if mechanism in by_value:
            return by_value[mechanism]
    raise ValueError(f"Unsupported mechanism type: {mechanism}")


def _build_datasource(cfg: ExperimentRunConfig):
    if cfg.datasource is not None:
        if isinstance(cfg.datasource, (DatabaseOptions, DataSourceType, str)):
            return h.make_datasource(
                source_type=cfg.datasource,
                size=cfg.size,
                probability=cfg.probability,
                probabilities=cfg.probabilities,
                mean=cfg.mean,
                std=cfg.std,
            )
        return cfg.datasource
    else :
        raise ValueError(f"No valid Datasource: {cfg.datasource}")


def build_experiment(run_config: ExperimentRunConfig):
    config = h.make_config(
        added_values=[run_config.h0_value, run_config.h1_value],
        size=run_config.size,
        probability=run_config.probability,
        probabilities=run_config.probabilities,
        mean=run_config.mean,
        std=run_config.std,
        seed=run_config.seed,
        attack_type=(
            run_config.attack_model.value
            if isinstance(run_config.attack_model, AttackModelOptions)
            else run_config.attack_model
        ),
        alpha=run_config.alpha,
    )

    datasource = _build_datasource(run_config)
    config = config.with_datasource(datasource)
    config = config.with_query(_resolve_query(run_config.query))

    mechanism_type = _resolve_mechanism_type(run_config.mechanism)
    mechanism_config = run_config.mechanism_config or []
    mechanism = h.make_mechanism(mechanism_config, mechanism_type, seed=run_config.mechanism_seed)
    config = config.with_mechanism(mechanism)

    attack_model = None
    if run_config.attack_model is not None:
        attack_model = h.make_attack_model(config, run_config.attack_model)
        if hasattr(attack_model, "set_alpha") and run_config.alpha is not None:
            attack_model.set_alpha(run_config.alpha)

    experiment = h.make_experiment(
        config=config,
        mechanism=mechanism,
        attack_model=attack_model,
        epsilon=run_config.epsilon,
        delta=run_config.delta,
    )
    return experiment


def _success_rate_from_observers(observers: Iterable[Any]) -> float:
    for observer in observers:
        if hasattr(observer, "success_rate"):
            return float(observer.success_rate)
    return float("nan")


def run_monte_carlo_sweep(
    base_config: ExperimentRunConfig,
    varied_name: str,
    values: Iterable[Any],
    run_count: int,
    observer_filename: str | None = None,
) -> list[SweepResult]:
    if not hasattr(base_config, varied_name):
        raise ValueError(f"ExperimentRunConfig has no field named '{varied_name}'")

    results: list[SweepResult] = []

    for value in values:
        run_cfg = replace(base_config, **{varied_name: value})
        experiment = build_experiment(run_cfg)


        observers = []
        observers.append(SuccessRateObserver())
        if observer_filename != None:
            observers.append(DataGeneratorObserver(f"{observer_filename}.csv"))


        simulator = h.make_simulator(run_count, experiment, observers=observers)
        simulator.run_simulation()

        success_rate = _success_rate_from_observers(observers)
        advantage = abs(success_rate - 0.5) if success_rate == success_rate else float("nan")
        results.append(
            SweepResult(
                varied_name=varied_name,
                varied_value=value,
                success_rate=success_rate,
                advantage=advantage,
            )
        )

    return results
