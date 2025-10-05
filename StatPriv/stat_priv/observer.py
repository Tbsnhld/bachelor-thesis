from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, bool) -> None:
        pass


class SuccessRateObserver(Observer):
    success_rate: float
    nr_run: int
    correctly_guessed: int
    def update(self, bool):
        self.nr_run =+ 1
        if bool == True:
            self.correctly_guessed =+ 1
        self.success_rate = self.correctly_guessed / self.nr_run


class ExperimentGraphicObserver(Observer):
    def update(self, bool) -> None:
        pass

        

        

