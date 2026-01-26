from dataclasses import dataclass, replace
from numpy._typing import _UnknownType
from src.data_source import DataSource
from src.query import Query

@dataclass(frozen=True)
class DatabaseConfig:
    seed: int | None
    query: Query | None
    datasource: DataSource | None
    added_value: _UnknownType | None
    size: int | None
    
    def with_added_value(self, value) -> "DatabaseConfig":
        return replace(self, added_value=value) 

    def with_seed(self, seed) -> "DatabaseConfig":
       return replace(self, seed=seed) 

    def with_datasource(self, datasource) -> "DatabaseConfig":
       return replace(self, datasource=datasource) 

    def with_size(self, size) -> "DatabaseConfig":
       return replace(self, size=size) 

    def with_query(self, query) -> "DatabaseConfig":
       return replace(self, query=query) 
