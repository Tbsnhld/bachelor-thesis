from abc import ABC, abstractmethod
class Simulator(ABC):
    @abstractmethod
    def run_simulation(self):
       pass 

    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify(self, info):
        pass
    
class MonteCarlo(Simulator):
    def __init__(self, count, experiment):
       self.n = count 
       self.experiment = experiment
       self.observers = []
       self.probabilities = experiment.config.probability

    # returns the approximated value 
    def run_simulation(self):

        for i in range(self.n):
            turnout = self.experiment.run()
            self.notify(turnout)
        self.finalize()
        

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, info):
        for observer in self.observers:
            observer.update(info)

    def finalize(self):
        for observer in self.observers:
            observer.finalize()

