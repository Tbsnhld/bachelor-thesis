from enum import Enum
import src.mechanism as mechanisms
import src.data_source as sources

class MechanismType(Enum):
    GAUSSIAN = type(mechanisms.GaussianNoise) 
    LAPLACE = type(mechanisms.LaplaceNoise) 
    SUBSAMPLING = type(mechanisms.Subsampling) 

