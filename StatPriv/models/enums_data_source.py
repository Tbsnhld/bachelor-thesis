from enum import Enum
import src.query as queries
import src.data_source as sources

class DataSourceType(Enum):
    BERNOULLI = type(sources.BernoulliSource) 
    GAUSSIAN = type(sources.GaussianSource) 
    TEN = type(sources.TenSource) 

