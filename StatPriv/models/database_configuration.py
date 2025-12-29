from dataclasses import dataclass
from numpy._typing import _UnknownType
from src.data_source import DataSource
from src.query import Query

@dataclass
class DatabaseConfig:
    seed: int | None
    query: Query | None
    datasource: DataSource
    added_value: _UnknownType 
    size: int | None
    


