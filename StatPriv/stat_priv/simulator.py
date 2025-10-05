from abc import ABC, abstractmethod
class Simulator(ABC):
    @property
    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def run_simulation(self, attack_model) -> float:
       pass 

    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass
    
class MonteCarlo(Simulator):
    def __init__(self, experiment):
       self.n = n 
       self._experiment = experiment

    @property
    def experiment(self):
        return self._experiment

    # returns the approximated value 
    def run_simulation(self, attack_model):
        sum = 0
        for _ in range(self.n):
            sum = sum + attack_model.run();
        return sum / self.n

    def add_observer(self, observer):
        return super().add_observer(observer)

    def remove_observer(self, observer):
        return super().remove_observer(observer)

    def notify(self):
        return super().notify()
