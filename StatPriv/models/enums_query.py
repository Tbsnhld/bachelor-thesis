from enum import Enum
import src.query as queries

class QueryType(Enum):
    AVERAGE = queries.AverageQuery
    MEDIAN = queries.MedianQuery
    SUM = queries.SumQuery

