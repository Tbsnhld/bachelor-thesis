from api.data_generator import ExperimentRunConfig, run_monte_carlo_sweep
from src import attack_model, mechanism
from src.data_source import BernoulliSource
from models.enums_configuration_options import AttackModelOptions, MechanismOptions, QueryOptions, DatabaseOptions
from helper.helper import make_observers
from src.observer import DataGeneratorObserver

### RUN CONFIG ###
VARIED_VALUE = 'size'
VALUES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 450, 460, 470, 480, 490, 500]
#VALUES = [10, 50, 100, 200, 500, 1000]
RUN_COUNT = 100000 #Because for Bernoulli and TenSource the likelihood can be 0 these runs won't count
CSV_FILENAME = 'ten_source' #None if no CSV needed

### Experiment Config ###
datasource = DatabaseOptions.RANDOMONETEN
size = 10 #Database size
probability = 0.5 #Probability for the value in the database / Mean of 
probabilities = None #Probabilities for TenSource
query = QueryOptions.MEDIAN #Select Value from Enum QueryOptions
h0_value = 0
h1_value = 9 
attack_model = AttackModelOptions.MAX_LIKELIHOOD
mechanism = MechanismOptions.GAUSSIAN #Select Value from Enum MechanismOptions
mechanism_config = [0.5] #Scale / Std for Noise, Subsampling Rat for Subsampling, Prob for Poisson Sampling
alpha = 0.05 #Only necessary for when Using AttackModel = LIKELIHOOD_RATIO_ALPHA 
epsilon = 1  #Only necessary for (\epsilon,\delta-mechanism)
delta = 0.001 #Only necessary for (\epsilon,\delta-mechanism)
seed = None
mechanism_seed = None
mean = 5
std = 2



def main():
    base = ExperimentRunConfig(
        datasource=datasource,
        probability=probability,
        probabilities=probabilities,
        datasource_factory=datasource,
        size=size,
        query=query,
        h0_value=h0_value,
        h1_value=h1_value,
        attack_model=attack_model,
        mechanism=mechanism,
        mechanism_config=mechanism_config,
        alpha=alpha, 
        epsilon=epsilon,
        delta=delta,
        seed=seed,
        mechanism_seed=mechanism_seed,
        mean=mean,
        std=std
    )


    results = run_monte_carlo_sweep(
        base_config=base,
        varied_name=VARIED_VALUE,
        values=VALUES,
        run_count=RUN_COUNT,
        observer_filename=CSV_FILENAME,
    )

    for r in results:
        print(r.varied_value, r.success_rate, r.advantage)


if __name__ == "__main__":
    main()
