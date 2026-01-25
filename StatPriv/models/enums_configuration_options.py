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
    LAPLACE = "Laplace Noise"
    SAMPLING_REPLACEMENT = "Subsampling with Replacement"
    SAMPLING_NO_REPLACEMENT = "Sampling without Replacement"
    POISSONSAMPLING = "Poission Sampling"

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


