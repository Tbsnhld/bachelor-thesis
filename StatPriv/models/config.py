from dataclasses import dataclass, replace
from numpy._typing import _UnknownType
from src.data_source import DataSource
from src.query import Query

@dataclass(frozen=True)
class Config:
    seed: int | None
    datasource: DataSource | None
    size: int | None
    probability: float | None
    query: Query | None
    added_values: _UnknownType | None

    def with_added_values(self, values) -> "Config":
       return replace(self, added_values=values) 

    def with_seed(self, seed) -> "Config":
       return replace(self, seed=seed) 

    def with_datasource(self, datasource) -> "Config":
       return replace(self, datasource=datasource) 

    def with_size(self, size) -> "Config":
       return replace(self, size=size) 

    def with_probability(self, probability) -> "Config":
       return replace(self, probability=probability) 

    def with_query(self, query) -> "Config":
       return replace(self, query=query) 

