from abc import ABC, abstractmethod
class Builder(ABC):
    @property
    def experiment(self):
        pass

    @experiment.setter
    @abstractmethod
    def experiment(self, experiment_info):
        pass

    @abstractmethod
    def buildDatabaseConfig(self, distribution, size):
        pass

    @abstractmethod
    def buildAttackModel(self, strategy):
        pass

    @abstractmethod
    def buildMechanism(self, name, sigma):
        pass

    @abstractmethod
    def getExperiment(self):
        pass


class ExperimentBuilder(Builder):
    def buildDatabaseConfig(self, distribution, size):
        return super().buildDatabaseConfig(distribution, size)

    def buildAttackModel(self, strategy):
        return super().buildAttackModel(strategy)

    def buildMechanism(self, name, sigma):
        return super().buildMechanism(name, sigma)

    def getExperiment(self):
        pass

