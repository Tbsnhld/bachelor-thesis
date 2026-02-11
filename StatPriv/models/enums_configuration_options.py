from enum import Enum

class AttackModelOptions(Enum):
    MAX_LIKELIHOOD = "Maximum Likelihood fixed Threshold (1)"
    LIKELIHOOD_RATIO_ALPHA = "Maximum Likelihood"

class DatabaseOptions(Enum):
    BINARY = "Binary Values"
    RANDOMONETEN = "Random 1-10"
    GAUSSIAN = "Gaussian Distribution"
    CSV = "CSV"

class MechanismOptions(Enum):
    SAMPLING = "Sampling"
    NOISE = "Noise"
    GAUSSIAN = "Gaussian Noise"
    GAUSSIAN_EPSILON = "Gaussian Noise epsilon-delta"
    LAPLACE = "Laplace Noise"
    LAPLACE_EPSILON = "Laplace Noise epsilon-delta"
    SAMPLING_REPLACEMENT = "Subsampling with Replacement"
    SAMPLING_NO_REPLACEMENT = "Sampling without Replacement"
    POISSONSAMPLING = "Poisson Sampling"
    PURE_STATISTICAL_PRIVACY = "Pure Statistical Privacy"

class MenuOptions(Enum):
    DATABASE = "Database"
    ATTACKMODEL = "Attack Model"
    MECHANISM = "Mechanism"
    PRIVACY_BOUNDS = "Privacy Bounds"
    EXIT = "Exit"


class QueryOptions(Enum):
    AVERAGE = "Average"
    MEDIAN = "Median"
    SUM = "Sum"


