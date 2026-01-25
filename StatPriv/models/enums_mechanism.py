from enum import Enum
import src.mechanism as mechanisms

class MechanismType(Enum):
    GAUSSIAN = type(mechanisms.GaussianNoise) 
    LAPLACE = type(mechanisms.LaplaceNoise) 
    SUBSAMPLING = type(mechanisms.SubsamplingWithoutReplacement) 
    SUBSAMPLING_REPLACEMENT = type(mechanisms.SubsamplingWithReplacement) 
    POISSON_SUBSAMPLING = type(mechanisms.PoissonSubsampling) 

