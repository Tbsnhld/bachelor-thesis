from InquirerPy import inquirer
import helper.validators as validators
from src.data_source import DataSource 

def ask_attack_model():
    return inquirer.select(
            message="Which strategy does the attacker use?",
            choices=["maximum_likelihood", "other"],
            default="maximum_likelihood"
            ).execute()

def ask_database():
    return inquirer.select(
            message="Database Type",
            choices=["Binary/Bernoulli", "Random 1-10", "Gaussian", "CSV"],
            default="Binary/Bernoulli",
            ).execute()

def ask_delta():
    return inquirer.number(
            message="Delta value: ", float_allowed=True, min_allowed=0
            ).execute()
def ask_distribution():
    return inquirer.number(
        message="Distribution: ", float_allowed=True, max_allowed=1, min_allowed=0
    ).execute()


def ask_epsilon():
    return inquirer.number(
            message="Epsilon value: ", float_allowed=True, min_allowed=0
            ).execute()


def ask_mean():
    return inquirer.number(
                message="Mean: ",
                float_allowed=True,
            ).execute()

def ask_std():
    return inquirer.number(
            message="Standard deviation: ",
            float_allowed=True,
        ).execute()

def ask_mechanism():
    return inquirer.select(
            message="Which mechanism does the database use?",
            choices=["gaussian", "laplace", "poission"],
            default="gaussian"
            ).execute()

def ask_start():
    return inquirer.select(
                message="Run the experiment",
                choices=["Yes", "No"],
                default="No",
                ).execute()

def ask_query():
    return inquirer.select(
            message="Which query? ",
            choices=["Average","Median", "Sum"],
            default="Average",
            ).execute()

def ask_run_count():
    return inquirer.number(
            message="How often do you wish to run the experiment?",
            float_allowed=False,
            min_allowed=1,
            max_allowed=10000,
            default=500 
        ).execute()

def ask_seed() -> bool:
    seed = inquirer.select(
            message="Do you wish to use a seed?",
            choices=["Yes", "No"],
            default=["No"]
            ).execute()

    if seed == "Yes":
        return True 
    return False 

def ask_size():
    return int(inquirer.number(
            message="Database size: ", float_allowed=False, max_allowed=10000, min_allowed=0
    ).execute())

def enter_seed(message: str | None) -> int:
    if message == None:
        return int(inquirer.number(message=f"Seed: ").execute())
    return int(inquirer.number(message=f"Enter seed for {message}").execute())

def menu():
    return inquirer.select(
                message="Menu",
                choices=["Database", "AttackModel", "Mechanism", "Privacy Bounds","Exit"],
                default="Database",
                ).execute()


def pick_value(datasource: DataSource, message: str):
    if datasource.domain:
        domain_list = [str(value) for value in datasource.domain]
        return inquirer.select(
                message=message,#TODO change message
                choices=domain_list,
                default=domain_list[0]
                ).execute()

    value = inquirer.text(
            message=message,
            validate=lambda value: validators._validate_type(value, datasource.value_type),
            ).execute()

    return datasource.value_type(value)

