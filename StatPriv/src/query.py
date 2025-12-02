from abc import ABC, abstractmethod
class Query(ABC):
    @abstractmethod
    def execute(self,data):
        pass

class AverageQuery(Query):
    def execute(self, data):
        return sum(data) / len(data)

class SumQuery(Query):
    def execute(self, data):
        return sum(data)

