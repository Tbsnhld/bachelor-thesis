from math import dist
from InquirerPy import inquirer
from src.builder import ExperimentBuilder
from src.data_source import BernoulliSource, DataSource, GaussianSource, TenSource
from src.database import Database
from src.experiment import Experiment
from src.simulator import MonteCarlo
from src.observer import DataGeneratorObserver, SuccessRateObserver 
from models.enums_configuration_options import AttackModelOptions, DatabaseOptions, MechanismOptions, MenuOptions, QueryOptions
import helper.configuration_helper as co_helper

def main():
    builder = ExperimentBuilder()
    run_loop(builder)

def run_loop(builder: ExperimentBuilder):
    while True:
        checkFinished(builder)

        options = co_helper.menu()

        if options == MenuOptions.EXIT.value:
            print(f"You choose {options}")
            exit()
        elif options == MenuOptions.DATABASE.value:
            builder = database(builder)
        elif options == MenuOptions.ATTACKMODEL.value:
            builder = attack_model(builder)
        elif options == MenuOptions.MECHANISM.value:
            builder = mechanism(builder)
        elif options == MenuOptions.PRIVACY_BOUNDS.value:
            builder = bounds(builder)

def bounds(builder: ExperimentBuilder) -> ExperimentBuilder:
    epsilon = float(co_helper.ask_epsilon())
    delta = float(co_helper.ask_delta())
    builder = builder.with_bounds(epsilon=epsilon, delta=delta)

    return builder

def database(builder: ExperimentBuilder) -> ExperimentBuilder:
    database_type = co_helper.ask_database()

    size = co_helper.ask_size()
    query = co_helper.ask_query()

    seed = None
    if co_helper.ask_seed():
        seed = co_helper.enter_seed('Seed') 

    datasource = generate_datasource(database_type, size, seed)
    searched_values = select_values(datasource)
    return builder.with_database(query=query, size=size, datasource=datasource, added_values=searched_values, seed=seed)

def attack_model(builder: ExperimentBuilder):
    if builder.experiment_config == None:
        builder = database(builder)

    attack_model = co_helper.ask_attack_model()
    builder.with_attack_model(attack_model)
    if attack_model == AttackModelOptions.LIKELIHOOD_RATIO_ALPHA.value:
        alpha = co_helper.ask_alpha()
        builder.with_alpha(alpha)
    return builder

def mechanism(builder: ExperimentBuilder):
    mechanism = co_helper.ask_mechanism()
    seed = None

    if co_helper.ask_seed():
        seed = co_helper.enter_seed("Mechanism seed")

    if co_helper.needs_sample_size(mechanism):
        mechanism_config = [co_helper.ask_sample_size(builder.experiment_config.size)]
    else :
        mechanism_config = co_helper.mechanism_config(mechanism)

    builder.with_mechanism(mechanism, mechanism_config, seed)
    return builder


def generate_datasource(datasource_str : str, size: int, seeds=None):
    datasource=None
    if datasource_str == DatabaseOptions.BINARY.value:
        distribution = float(co_helper.ask_distribution())
        datasource = BernoulliSource(p=distribution, size=size)
    elif datasource_str == DatabaseOptions.RANDOMONETEN.value:
        distributions = co_helper.ask_distribution_each_entry(9)
        datasource = TenSource(p=distributions, size=size)
    elif datasource_str == DatabaseOptions.GAUSSIAN.value:
        mean = float(co_helper.ask_mean())
        std = float(co_helper.ask_std())
        datasource = GaussianSource(mean, std, size=size)
    elif datasource_str == DatabaseOptions.CSV.value:
        raise ValueError(f"Data source not implemented: {datasource_str}")
    else :
        raise ValueError(f"Data source can't be generated: {datasource_str}")
    return datasource


def select_values(datasource: DataSource):
    selected_value = co_helper.pick_value(datasource, "Pick critical entry value for the null hypothesis database.")
    selected_value2 = co_helper.pick_value(datasource, "Pick critical entry value for the alternativ hypothesis database.")
    selected_values = [selected_value, selected_value2]
    return selected_values

def checkFinished(builder: ExperimentBuilder):
    if (builder.experiment.attack_model is not None and
        builder.experiment.mechanism is not None and 
        builder.experiment.config is not None and 
        builder.experiment.delta is not None):

        fin = co_helper.ask_start()
        if fin == "No":
            return 
        if fin == "Yes":
            run_experiment(builder)

def run_experiment(builder: ExperimentBuilder):
        run_count = co_helper.ask_run_count()
        experiment = builder.get_experiment()
        
        observers = configure_observers()

        simulator = MonteCarlo(int(run_count), experiment)
        simulator.add_observers(observers)
        simulator.run_simulation()
        run_loop(builder)

def configure_observers():
        observer_choices=co_helper.ask_observers()
        observers = []

        for observer in observer_choices:
            if observer == 'CSV File Run':
                file_name = co_helper.ask_filename() + '.csv'
                observer = DataGeneratorObserver(file_name)
                observers.append(observer)

            if observer == 'CLI Attacker SuccessRate':
                observer = SuccessRateObserver()
                observers.append(observer)

        return observers

if __name__ == "__main__":
    main()

