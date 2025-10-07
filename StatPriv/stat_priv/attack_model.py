from abc import ABC, abstractmethod
class AttackModel(ABC):
   @property
   @abstractmethod
   def density_function(self):
       pass

   @density_function.setter
   @abstractmethod
   def density_function(self, mu):
       pass

   @abstractmethod
   def run(self):
       pass


class MaximumLikelihood(AttackModel):
    @property
    def density_function(self):
        return super().density_function
    
    @density_function.setter
    def density_function(self, mu):
        return super().density_function

    def run(self):
        pass
