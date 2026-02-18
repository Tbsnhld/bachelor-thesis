from dataclasses import dataclass 
from typing import Any, Callable 

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
    data: list[dict[str, Any]]
