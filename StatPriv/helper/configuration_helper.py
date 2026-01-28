from InquirerPy import inquirer
import helper.validators as validators
from src import mechanism
from src.data_source import DataSource 
from models.enums_configuration_options import AttackModelOptions, DatabaseOptions, MechanismOptions, MenuOptions, QueryOptions

def ask_alpha():
    return float(inquirer.number(
            message="Alpha value: ", float_allowed=True, min_allowed=0, max_allowed=1
            ).execute())

def ask_attack_model():
    return inquirer.select(
            message="Which strategy does the attacker use?",
            choices=[AttackModelOptions.MAX_LIKELIHOOD.value, AttackModelOptions.LIKELIHOOD_RATIO_ALPHA.value],
            default=AttackModelOptions.MAX_LIKELIHOOD.value
            ).execute()

def ask_database():
    return inquirer.select(
            message="Database Type",
            choices=[DatabaseOptions.BINARY.value, DatabaseOptions.RANDOMONETEN.value,DatabaseOptions.GAUSSIAN.value, DatabaseOptions.CSV.value],
            default=DatabaseOptions.BINARY.value,
            ).execute()

def ask_delta():
    return inquirer.number(
            message="Delta value: ", float_allowed=True, min_allowed=0.0000000001, max_allowed=1
            ).execute()

def ask_distribution():
    return inquirer.number(
        message="Distribution: ", float_allowed=True, max_allowed=1, min_allowed=0
    ).execute()

def ask_probability():
    return inquirer.number(
        message="Probability: ", float_allowed=True, max_allowed=1, min_allowed=0
    ).execute()

def ask_distribution_each_entry(size):
    if size <= 0:
        raise ValueError("Size must be a positive integer")

    use_custom = inquirer.confirm(
        message="Do you want to manually set probabilities for each entry?",
        default=False,
    ).execute()

    # Uniform distribution
    if not use_custom:
        return None

    probabilities = []

    for i in range(size):
        prob = inquirer.text(
            message=f"Enter probability for entry {i}",
            validate=lambda x: validators._validate_probability(x),
        ).execute()

        probabilities.append(float(prob))

    total = sum(probabilities)

    if total <= 0:
        raise ValueError("Sum of probabilities must be greater than zero")

    # Normalize so they sum to 1
    normalized = [p / total for p in probabilities]

    return normalized

def ask_epsilon():
    return inquirer.number(
            message="Epsilon value: ", float_allowed=True, min_allowed=0.0000000001
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
    return ask_mechanism_noise()

def ask_mechanism_noise():
    answer = inquirer.select(
            message="Which noise mechanism should the database use?",
            choices=[MechanismOptions.GAUSSIAN.value,
                     MechanismOptions.LAPLACE.value,
                     MechanismOptions.GAUSSIAN_EPSILON.value,
                     MechanismOptions.LAPLACE_EPSILON.value,
                     MechanismOptions.SAMPLING.value],
            default=MechanismOptions.GAUSSIAN.value
            ).execute()
    if answer == MechanismOptions.SAMPLING.value:
        return ask_mechanism_sampling()
    return answer

def ask_mechanism_sampling():
    answer = inquirer.select(
            message="Which subsampling mechanism should the database use?",
            choices=[MechanismOptions.SAMPLING_REPLACEMENT.value, MechanismOptions.SAMPLING_NO_REPLACEMENT.value, MechanismOptions.POISSONSAMPLING.value, MechanismOptions.NOISE.value],
            default=MechanismOptions.SAMPLING_REPLACEMENT.value
            ).execute()
    if answer ==MechanismOptions.NOISE.value:
        return ask_mechanism_noise()
    return answer

def ask_sample_size(data_size:int | None):
    sample_size = int(inquirer.number(
        message="Sample size: ",
            float_allowed=False, min_allowed=1, max_allowed=data_size
        ).execute())
    return sample_size

def ask_selected_database():
    return inquirer.select(
            message="Which database contains the correct critical entry?",
            choices=[0, 1],
            default=0,
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
            choices=[QueryOptions.AVERAGE.value,QueryOptions.MEDIAN.value, QueryOptions.SUM.value],
            default=QueryOptions.AVERAGE.value,
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
                choices=[MenuOptions.DATABASE.value, MenuOptions.ATTACKMODEL.value, MenuOptions.MECHANISM.value,MenuOptions.PRIVACY_BOUNDS.value, MenuOptions.EXIT.value],
                default=MenuOptions.DATABASE.value,
                ).execute()
    
def needs_sample_size(mechanism_name: str):
    sample_size_list = [MechanismOptions.SAMPLING_NO_REPLACEMENT.value, MechanismOptions.SAMPLING_REPLACEMENT.value]
    if mechanism_name in sample_size_list:
        return True
    return False
    
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


def mechanism_config(mechanism):
    if mechanism == MechanismOptions.GAUSSIAN.value:
        return gaussian_mechanism_config()
    elif mechanism == MechanismOptions.LAPLACE.value:
        return laplace_mechanism_config()
    elif mechanism == MechanismOptions.POISSONSAMPLING.value:
        return poission_sampling_config()
    else:
        return []

def gaussian_mechanism_config():
    mean = float(ask_mean())
    scale = float(ask_std())
    return [mean, scale]

def laplace_mechanism_config():
    scale = float(ask_std())
    return [scale]

def poission_sampling_config():
    probability = float(ask_probability())
    return [probability]

