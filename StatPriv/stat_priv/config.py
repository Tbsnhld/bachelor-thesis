from dataclasses import dataclass
from data_source import DataSource
from query import Query

@dataclass
class Config:
    seed: int | None
    datasource: DataSource | None
    size: int | None
    probability: float | None
    query: Query | None
    


