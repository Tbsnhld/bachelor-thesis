from math import dist
from InquirerPy import inquirer 
from builder import ExperimentBuilder
from data_source import BernoulliSource, DataSource, GaussianSource, TenSource
from simulator import MonteCarlo
from observer import SuccessRateObserver 

def main():
    builder = ExperimentBuilder()
    while True:
        solution = checkFinished(builder)
        if solution == True:
            run_count = inquirer.number(
                message="How often do you wish to run the experiment?",
                float_allowed=False,
                min_allowed=1,
                max_allowed=10000,
                default=500 
            ).execute()
            experiment = builder.getExperiment()
            observer = SuccessRateObserver()
            observer.probabilities(experiment.config.probability)
            simulator = MonteCarlo(int(run_count), experiment)
            simulator.add_observer(observer)
            simulator.run_simulation()
            exit()

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
            choices=["Binary/Bernoulli", "Binomial 1-10", "Gaussian", "CSV"],
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
            choices=["Average", "Sum"],
            default="Average",
            ).execute()


    seedy_n = inquirer.select(
            message="Do you wish to use a seed?",
            choices=["Yes","No"],
            default="Exit"
    ).execute()


    if seedy_n == "Yes":
        seed = int(inquirer.number(
            message="Seed: ",
        ).execute())
        datasource = datasource_generator(data_source, size, distribution, seed)
        return builder.withDatabase(distribution, query, datasource, size, seed)

    datasource = datasource_generator(data_source, size, distribution)
    searched_value = select_value(datasource)
    return builder.withDatabase(distribution=distribution, query=query, size=size, datasource=datasource, added_value=searched_value)

def attackModel(builder: ExperimentBuilder):
    if builder._database_config == None:
        builder = database(builder)

    attackModel = inquirer.select(
            message="Which strategy does the attacker use?",
            choices=["maximum_likelihood", "other"],
            default="maximum_likelihood"
            ).execute()
    builder.withAttackModel(attackModel)
    return builder

def mechanism(builder: ExperimentBuilder):
    attackModel = inquirer.select(
            message="Which mechanism does the database use?",
            choices=["gaussian", "laplace", "poission"],
            default="gaussian"
            ).execute()

    seedy_n = inquirer.select(
            message="Do you wish to use a seed?",
            choices=["Yes","No"],
            default="Exit"
    ).execute()

    if seedy_n == "Yes":
        seed = int(inquirer.number(
            message="Seed: ",
        ).execute())
        return builder.withMechanism(attackModel, seed)
    builder.withMechanism(attackModel)
    return builder

def datasource_generator(datasource_str : str, size: int, distribution: float, seed=None):
    datasource=None
    if datasource_str == "Binary/Bernoulli":
        datasource = BernoulliSource(p=distribution)
    elif datasource_str == "Binomial 1-10":
        datasource = TenSource(p=distribution)
    elif datasource_str == "Gaussian":
        mean = float(inquirer.number(
            message="Mean: ",
            float_allowed=True,
        ).execute())
        std = float(inquirer.number(
            message="Standard deviation: ",
            float_allowed=True,
        ).execute())
        datasource = GaussianSource(mean, std)
    elif datasource_str == "CSV":
        raise ValueError(f"Data source not implemented: {datasource_str}")
    else :
        raise ValueError(f"Data source could not be generated: {datasource_str}")
    return datasource

def select_value(datasource: DataSource):
        domain = datasource.domain
        domain_list_str = [str(value) for value in domain]
        selected_value = inquirer.select(
                message="Which value is searched?",
                choices=domain_list_str,
                default=domain_list_str[0]
                ).execute()
        return selected_value

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
            return False
        if fin == "Yes":
            return True

if __name__ == "__main__":
    main()

