from InquirerPy import inquirer 
from builder import ExperimentBuilder
from data_source import BinomialSource

def main():
    builder = ExperimentBuilder()
    while True:
        solution = checkFinished(builder)
        if solution == True:
            end_message = inquirer.select(
                    message="Do you wish to run the experiment?",
                    choices=["Yes", "No"],
                    default="No"
                    ).execute()
            if end_message == False:
                continue

            if end_message == True:
                run_count = inquirer.number(
                    message="How often do you wish to run the experiment?",
                    float_allowed=False,
                    min_allowed=1,
                    max_allowed=10000,
                    default=500 
                )
                experiment = builder.getExperiment()
                simulator = MonteCarlo(run_count, experiment)
        options = inquirer.select(
                message="What do you wish to configure?",
                choices=["Database", "AttackModel", "Mechanism", "Exit"],
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



                


def database(builder: ExperimentBuilder) -> ExperimentBuilder:
    query = inquirer.select(
            message="Database Type",
            choices=["Binary", "1-10"],
            default="Binary",
            )

    distribution = inquirer.number(
        message="Distribution: ", float_allowed=True, max_allowed=1, min_allowed=0
    ).execute()


    size = inquirer.number(
            message="Database size: ", float_allowed=False, max_allowed=10000, min_allowed=0
    ).execute()

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

    

    datasource = BinomialSource(p=distribution)

    if seedy_n == "Yes":
        seed = inquirer.number(
            message="Seed: ",
        ).execute
        return builder.withDatabase(distribution, size, query, seed)

    return builder.withDatabase(distribution=distribution, size=size, datasource=datasource)

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
        seed = inquirer.number(
            message="Seed: ",
        ).execute()
        return builder.withMechanism(attackModel, seed)
    builder.withMechanism(attackModel)
    return builder

def checkFinished(builder: ExperimentBuilder):
    if (builder.experiment.attack_model is not None and
        builder.experiment.mechanism is not None and 
        builder.experiment.config is not None and 
        builder.experiment.delta is not None and 
        builder.experiment.sample_size is not None):
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

