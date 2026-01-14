from enum import Enum

class DataSourceType(Enum):
    BERNOULLI = "Bernoulli"
    GAUSSIAN = "Gaussian"
    TEN = "TenSource"

class QueryType(Enum):
    AVERAGE = "Average"
    MEDIAN = "Median"
    SUM = "Sum"

