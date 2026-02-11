from dataclasses import dataclass, replace
from numpy._typing import _UnknownType
from models.enums_query import QueryType
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
    attack_type: str | None
    alpha: float | None
    sensitivity: float | None

    def with_added_values(self, values) -> "Config":
        return replace(self, added_values=values) 

    def with_seed(self, seed) -> "Config":
        return replace(self, seed=seed) 

    def with_datasource(self, datasource) -> "Config":
        sensitivity = self.calculate_sensitivity(self.query)
        config = replace(self, datasource=datasource, sensitivity=sensitivity) 
        return config

    def with_size(self, size) -> "Config":
        sensitivity = self.calculate_sensitivity(self.query)
        config = replace(self, size=size, sensitivity=sensitivity) 
        return config

    def with_query(self, query) -> "Config":
        sensitivity = self.calculate_sensitivity(query)
        config = replace(self, query=query, sensitivity=sensitivity) 
        return config

    def with_mechanism(self, mechanism) -> "Config":
        return replace(self, mechanism=mechanism) 

    def with_attack_model(self, attack_type) -> "Config":
        return replace(self, attack_type=attack_type)

    def with_alpha(self, alpha) -> "Config":
        return replace(self, alpha=alpha)

    def calculate_sensitivity(self, query: Query):
        if query != None and self.datasource != None and self.size != None:
            if type(query) == QueryType.SUM.value :
                sensitivity = self.datasource.max_diff
            elif type(query) == QueryType.MEDIAN.value:
                sensitivity = 1
            else:
                sensitivity = self.datasource.max_diff/self.size
            return sensitivity
        return None


