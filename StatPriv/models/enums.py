from enum import Enum
from src.data_source import BernoulliSource, GaussianSource, TenSource

class DataSourceType(Enum):
    BERNOULLI = "Bernoulli"
    GAUSSIAN = "Gaussian"
    TEN = "TenSource"

class QueryType(Enum):
    AVERAGE = "Average"
    MEDIAN = "Median"
    SUM = "Sum"

