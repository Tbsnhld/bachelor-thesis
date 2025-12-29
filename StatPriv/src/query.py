from abc import ABC, abstractmethod
from scipy import stats

class Query(ABC):
    @abstractmethod
    def execute(self,data):
        pass

    @abstractmethod
    def adversary(self,data):
        pass

class AverageQuery(Query):
    #data: Generated numpy data
    def execute(self, data):
        return sum(data) / len(data)

    #data: scipy stats generated data
    def adversary(self, data, db_config):
        mean = data.mean()
        size = db_config.size
        adversary_avg = ((size - 1) * mean + db_config.added_value) / size
        return adversary_avg

class MedianQuery(Query):
    def execute(self, data):
        return data[len(data)/2]

    def adversary(self, data):
        return data.median()
    
class SumQuery(Query):
    def __init__(self):
        self.size 
    
    def execute(self, data):
        self.size = len(data)
        return sum(data)

    def adversary(self, data):
        return self.size * data.mean()

