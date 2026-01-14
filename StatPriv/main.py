from math import dist
from InquirerPy import inquirer 
from src.builder import ExperimentBuilder
from src.data_source import BernoulliSource, DataSource, GaussianSource, TenSource
from src.simulator import MonteCarlo
from src.observer import SuccessRateObserver 

def main():
    builder = ExperimentBuilder()
    run_loop(builder)

def run_loop(builder: ExperimentBuilder):
    while True:
        checkFinished(builder)

        options = inquirer.select(
                message="What do you wish to configure?",
                choices=["Database", "AttackModel", "Mechanism", "Privacy Bounds","Exit"],
                default="Database",
                ).execute()

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
    epsilon = inquirer.number(
            message="Epsilon value: ", float_allowed=True, min_allowed=0
            ).execute()
    builder.experiment.epsilon = float(epsilon)

    delta = inquirer.number(
            message="Delta value: ", float_allowed=True, min_allowed=0
            ).execute()
    builder.experiment.delta = float(delta)

    return builder

def database(builder: ExperimentBuilder) -> ExperimentBuilder:
    data_source = inquirer.select(
            message="Database Type",
            choices=["Binary/Bernoulli", "Random 1-10", "Gaussian", "CSV"],
            default="Binary/Bernoulli",
            ).execute()

    distribution = float(inquirer.number(
        message="Distribution: ", float_allowed=True, max_allowed=1, min_allowed=0
    ).execute())


    size = int(inquirer.number(
            message="Database size: ", float_allowed=False, max_allowed=10000, min_allowed=0
    ).execute())

    query = inquirer.select(
            message="Which query? ",
            choices=["Average","Median", "Sum"],
            default="Average",
            ).execute()


    seed = None
    if ask_for_seed():
        seed = enter_seed('Seed') 

    datasource = datasource_generator(data_source, size, distribution, seed)
    searched_values = select_values(datasource)
    return builder.with_database(distribution=distribution, query=query, size=size, datasource=datasource, added_values=searched_values, seed=seed)

def attackModel(builder: ExperimentBuilder):
    if builder._database_config == None:
        builder = database(builder)

    attackModel = inquirer.select(
            message="Which strategy does the attacker use?",
            choices=["maximum_likelihood", "other"],
            default="maximum_likelihood"
            ).execute()
    builder.with_attack_model(attackModel)
    return builder

def mechanism(builder: ExperimentBuilder):
    attackModel = inquirer.select(
            message="Which mechanism does the database use?",
            choices=["gaussian", "laplace", "poission"],
            default="gaussian"
            ).execute()

    if ask_for_seed():
        seed = enter_seed("Mechanism seed")
        return builder.with_mechanism(attackModel, seed)
    builder.with_mechanism(attackModel)
    return builder

def datasource_generator(datasource_str : str, size: int, distribution: float, seeds=None):
    datasource=None
    if datasource_str == "Binary/Bernoulli":
        datasource = BernoulliSource(p=distribution, size=size)
    elif datasource_str == "Random 1-10":
        datasource = TenSource(p=distribution, size=size)
    elif datasource_str == "Gaussian":
        mean = float(inquirer.number(
            message="Mean: ",
            float_allowed=True,
        ).execute())
        std = float(inquirer.number(
            message="Standard deviation: ",
            float_allowed=True,
        ).execute())
        datasource = GaussianSource(mean, std, size=size)
    elif datasource_str == "CSV":
        raise ValueError(f"Data source not implemented: {datasource_str}")
    else :
        raise ValueError(f"Data source could not be generated: {datasource_str}")
    return datasource


def select_values(datasource: DataSource):
        domain = datasource.domain
        domain_list_str = [str(value) for value in domain]
        selected_value = inquirer.select(
                message="Critical Entry value in searched dataset",#TODO change message
                choices=domain_list_str,
                default=domain_list_str[0]
                ).execute()

        selected_value2 = inquirer.select(
                message="Critical Entry value in the other dataset",
                choices=domain_list_str,
                default=domain_list_str[0]
                ).execute()

        selected_values = [selected_value, selected_value2]
        return selected_values

def checkFinished(builder: ExperimentBuilder):
    if (builder.experiment.attack_model is not None and
        builder.experiment.mechanism is not None and 
        builder.experiment.config is not None and 
        builder.experiment.delta is not None):
        fin = inquirer.select(
                message="Run the experiment",
                choices=["Yes", "No"],
                default="No",
                ).execute()

        if fin == "No":
            return 
        if fin == "Yes":
            run_experiment(builder)

def run_experiment(builder: ExperimentBuilder):
        run_count = inquirer.number(
            message="How often do you wish to run the experiment?",
            float_allowed=False,
            min_allowed=1,
            max_allowed=10000,
            default=500 
        ).execute()
        experiment = builder.get_experiment()
        observer = SuccessRateObserver()
        observer.probabilities(experiment.config.probability)
        simulator = MonteCarlo(int(run_count), experiment)
        simulator.add_observer(observer)
        simulator.run_simulation()
        run_loop(builder)

def ask_for_seed() -> bool:
    seed = inquirer.select(
            message="Do you wish to use a seed?",
            choices=["Yes", "No"],
            default=["No"]
            ).execute()

    if seed == "Yes":
        return True 
    return False 

def enter_seed(message: str | None) -> int:
    if message == None:
        return int(inquirer.number(message=f"Seed: ").execute())
    return int(inquirer.number(message=f"Enter seed for {message}").execute())

if __name__ == "__main__":
    main()

