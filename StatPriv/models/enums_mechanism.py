from enum import Enum
import src.mechanism as mechanisms

class MechanismType(Enum):
    GAUSSIAN =mechanisms.GaussianNoise 
    LAPLACE = mechanisms.LaplaceNoise 
    LAPLACE_EPSILON = mechanisms.LaplaceNoiseEpsilonDelta
    SUBSAMPLING = mechanisms.SubsamplingWithoutReplacement 
    SUBSAMPLING_REPLACEMENT = mechanisms.SubsamplingWithReplacement
    POISSON_SUBSAMPLING = mechanisms.PoissonSubsampling 
    PURE_STATISTICAL_PRIVACY = mechanisms.PureStatisticalPrivacy

