from math import dist
from InquirerPy import inquirer 
from src.builder import ExperimentBuilder
from src.data_source import BernoulliSource, DataSource, GaussianSource, TenSource
from src.simulator import MonteCarlo
from src.observer import SuccessRateObserver 
import helper.configuration_helper as co_helper

def main():
    builder = ExperimentBuilder()
    run_loop(builder)

def run_loop(builder: ExperimentBuilder):
    while True:
        checkFinished(builder)

        options = co_helper.menu()

        if options == "Exit":
            print(f"You choose {options}")
            exit()
        elif options == "Database":
            builder = database(builder)
        elif options == "AttackModel":
            builder = attackModel(builder)
        elif options == "Mechanism":
            builder = mechanism(builder)
        elif options == "Privacy Bounds":
            builder = bounds(builder)

def bounds(builder: ExperimentBuilder) -> ExperimentBuilder:
    epsilon = co_helper.ask_epsilon()
    builder.experiment.epsilon = float(epsilon)
    delta = co_helper.ask_delta()
    builder.experiment.delta = float(delta)

    return builder

def database(builder: ExperimentBuilder) -> ExperimentBuilder:
    database_type = co_helper.ask_database()

    distribution = float(co_helper.ask_distribution())
    size = co_helper.ask_size()
    query = co_helper.ask_query()

    seed = None
    if co_helper.ask_seed():
        seed = co_helper.enter_seed('Seed') 

    datasource = generate_datasource(database_type, size, distribution, seed)
    searched_values = select_values(datasource)
    return builder.with_database(distribution=distribution, query=query, size=size, datasource=datasource, added_values=searched_values, seed=seed)

def attackModel(builder: ExperimentBuilder):
    if builder.experiment_config == None:
        builder = database(builder)

    attackModel = co_helper.ask_attack_model()
    builder.with_attack_model(attackModel)
    return builder

def mechanism(builder: ExperimentBuilder):
    attackModel = co_helper.ask_mechanism()

    if co_helper.ask_seed():
        seed = co_helper.enter_seed("Mechanism seed")
        return builder.with_mechanism(attackModel, seed)
    builder.with_mechanism(attackModel)
    return builder

def generate_datasource(datasource_str : str, size: int, distribution: float, seeds=None):
    datasource=None
    if datasource_str == "Binary/Bernoulli":
        datasource = BernoulliSource(p=distribution, size=size)
    elif datasource_str == "Random 1-10":
        datasource = TenSource(p=distribution, size=size)
    elif datasource_str == "Gaussian":
        mean = float(co_helper.ask_mean())
        std = float(co_helper.ask_std())
        datasource = GaussianSource(mean, std, size=size)
    elif datasource_str == "CSV":
        raise ValueError(f"Data source not implemented: {datasource_str}")
    else :
        raise ValueError(f"Data source can't be generated: {datasource_str}")
    return datasource


def select_values(datasource: DataSource):
    selected_value = co_helper.pick_value(datasource, "Pick critical entry value for the first database.")
    selected_value2 = co_helper.pick_value(datasource, "Pick critical entry value for the second database.")
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
        observer = SuccessRateObserver()
        observer.probabilities(experiment.config.probability)
        simulator = MonteCarlo(int(run_count), experiment)
        simulator.add_observer(observer)
        simulator.run_simulation()
        run_loop(builder)


if __name__ == "__main__":
    main()

