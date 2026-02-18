import numpy.random as npr
from models.enums_query import QueryType
from src.mechanism import GaussianNoise, LaplaceNoise, Mechanism
from src.attack_model import AttackModel
from models.config import Config
from src.database_generator import DatabaseGenerator

class Experiment():
    def __init__(self):
        self.attack_model = None
        self.config = None 
        self.epsilon = None
        self.delta = None
        self.sample_size = None
        self.query = None
        self.mechanism = None

    def set_experiment_config(self, config: Config):
        self.config = config
        self.query = config.query
        self.mechanism = config.mechanism
        return self

    def set_attack_model(self, attack_model: AttackModel):
        self.attack_model = attack_model
        return self

    def set_mechanism(self, mechanism: Mechanism):
        self.mechanism = mechanism
        return self

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def set_delta(self, delta): 
        self.delta = delta
        return self

    def set_query(self, query):
        self.query = query
        return self

    def set_sample_size(self, sample_size):
        self.sample_size = sample_size
        return self

    def run(self):
        if self.config != None:
            datagenerator = DatabaseGenerator(self.config)
            databases = datagenerator.get_databases()
            datasize = self.config.size
            database_decision = self.random_select() 
            selected_database = self.select_database(databases, database_decision)

            selected_database_data = selected_database.get_data()
            pre_mechanism_data = self.mechanism.pre_query_mechanism(selected_database_data, datasize=datasize)
            selected_database.set_data(pre_mechanism_data)
            query_answer = self.run_query(selected_database) 

            sensitivity = self.config.sensitivity 
            post_mechanism_answer = self.mechanism.post_query_mechanism(query_answer, delta=self.delta, epsilon=self.epsilon, datasize=datasize, sensitivity=sensitivity)
            attacker_decision = self.attack_model.run(post_mechanism_answer, databases)
            return self.check_decision(attacker_decision, database_decision)

    def select_database(self, databases, decision):
        return databases[decision] 

    def run_query(self, database):
        return database.run_query()

    def check_decision(self, attacker_decision, selected_database):
        if attacker_decision == None:
            return None
        if attacker_decision == selected_database:
            if attacker_decision == 0:
                return int(0) #True positive
            else:
                return int(1) #True negative
        else:
            if attacker_decision == 0:
                return int(2) #False negative
            else:
                return int(3) #False positive

    def random_select(self):
        return npr.randint(0,2) 
