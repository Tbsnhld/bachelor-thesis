from enum import Enum
import src.query as queries

class QueryType(Enum):
    AVERAGE =type(queries.AverageQuery) 
    MEDIAN = type(queries.MedianQuery) 
    SUM = type(queries.SumQuery) 

