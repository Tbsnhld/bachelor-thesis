from enum import Enum
import src.mechanism as mechanisms

class MechanismType(Enum):
    GAUSSIAN =mechanisms.GaussianNoise 
    GAUSSIAN_EPSILON = mechanisms.GaussianNoiseEpsilonDelta
    LAPLACE = mechanisms.LaplaceNoise 
    LAPLACE_EPSILON = mechanisms.GaussianNoiseEpsilonDelta
    SUBSAMPLING = mechanisms.SubsamplingWithoutReplacement 
    SUBSAMPLING_REPLACEMENT = mechanisms.SubsamplingWithReplacement
    POISSON_SUBSAMPLING = mechanisms.PoissonSubsampling 
    PURE_STATISTICAL_PRIVACY = mechanisms.PureStatisticalPrivacy

