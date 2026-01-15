from dataclasses import dataclass, replace
from numpy._typing import _UnknownType
from src.data_source import DataSource
from src.query import Query
from src.mechanism import Mechanism

@dataclass(frozen=True)
class Config:
    seed: int | None
    datasource: DataSource | None
    size: int | None
    query: Query | None
    added_values: _UnknownType | None
    mechanism: Mechanism | None

    def with_added_values(self, values) -> "Config":
       return replace(self, added_values=values) 

    def with_seed(self, seed) -> "Config":
       return replace(self, seed=seed) 

    def with_datasource(self, datasource) -> "Config":
       return replace(self, datasource=datasource) 

    def with_size(self, size) -> "Config":
       return replace(self, size=size) 

    def with_query(self, query) -> "Config":
       return replace(self, query=query) 

    def with_mechanism(self, mechanism) -> "Config":
       return replace(self, mechanism=mechanism) 
