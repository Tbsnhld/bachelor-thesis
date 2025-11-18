from abc import ABC, abstractmethod
class Simulator(ABC):
    @abstractmethod
    def run_simulation(self) -> float:
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
    def __init__(self, count, experiment):
       self.n = count 
       self.experiment = experiment
       self.observers = []

    # returns the approximated value 
    def run_simulation(self):
        sum = 0
        for _ in range(self.n):
            sum = sum + self.experiment.run();
            self.notify()
        return sum / self.n

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()
