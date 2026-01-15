from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, turnout) -> None:
        pass


class SuccessRateObserver(Observer):
    def __init__(self):
        self.success_rate: float = 0
        self.nr_run: int = 0
        self.correctly_guessed: int = 0

    def probabilities(self,probabilities):
        self.probabilities = probabilities

    def update(self, turnout):
        self.nr_run = self.nr_run + 1
        print(turnout)
        if turnout == True:
            self.correctly_guessed = self.correctly_guessed + 1
        self.success_rate = self.correctly_guessed / self.nr_run

    def finalize(self):
        print(f"probabilities: {self.probabilities}")
        print(f"Nr runs: {self.nr_run}")
        print(f"Nr times h0 was guessed: {self.correctly_guessed}")
        print(f"Success_rate of h0: {self.success_rate}")


class ExperimentGraphicObserver(Observer):
    def update(self, turnout) -> None:
        pass

        

        

