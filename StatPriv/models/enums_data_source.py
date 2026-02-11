from enum import Enum
import src.query as queries
import src.data_source as sources

class DataSourceType(Enum):
    BERNOULLI = sources.BernoulliSource
    GAUSSIAN = sources.GaussianSource
    TEN = sources.TenSource

