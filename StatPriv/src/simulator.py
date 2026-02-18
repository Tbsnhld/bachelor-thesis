from abc import ABC, abstractmethod
class Simulator(ABC):
    @abstractmethod
    def run_simulation(self):
       pass 

    @abstractmethod
    def add_observers(self, observers):
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

    # returns the approximated value 
    def run_simulation(self):
        self.notify(self.experiment.config)

        for i in range(self.n):
            turnout = self.experiment.run()
            self.notify(turnout)
        return self.finalize()

    def add_observers(self, observers):
        for observer in observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, info):
        for observer in self.observers:
            observer.update(info)

    def finalize(self):
        answer = None
        for observer in self.observers:
            data = observer.finalize()
            if data is not None:
                answer = data
        return answer


