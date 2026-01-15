from models.config import Config
from models.database_configuration import DatabaseConfig
from src.data_source import BernoulliSource, GaussianSource, TenSource
from src.database_generator import DatabaseGenerator
from src.query import AverageQuery, MedianQuery, SumQuery
from models.enums_query import QueryType
from models.enums_data_source import DataSourceType


# ------------------------
# Query factory
# ------------------------

def make_query(query_type: QueryType = QueryType.AVERAGE): 
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
    source_type: str = "Gaussian",
    size: int = 50,
    probability: float | None = 0.5,
    mean: float | None = 150,
    std: float | None = 13,
):
    if source_type == "Bernoulli":
        return BernoulliSource(probability, size)
    elif source_type == "TenSource":
        return TenSource(probability, size)
    elif source_type == "Gaussian":
        return GaussianSource(mean, std, size)
    else:
        raise ValueError(f"Unknown datasource type: {source_type}")


# ------------------------
# Config factory
# ------------------------

def make_config(
    added_values = [0, 50],
    size: int = 50,
    probability: float | None = 0.5,
    mean: float | None = 150,
    std: float | None = 13,
    seed: int | None = 1234,
):
    return (
        Config(
            seed=seed, 
            added_values=added_values, 
            datasource=None, 
            size=size, 
            probability=probability,
            query=None)
        .with_datasource(
            make_datasource(
                size=size,
                probability=probability,
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
    added_value=[0,50],
    size: int = 50,
    seed: int | None = 1234
):
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


