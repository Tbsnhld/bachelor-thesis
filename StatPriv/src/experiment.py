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

    def set_database_config(self, config: Config):
        self.config = config
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
            # Für subsampling: data und query answer in apply_mechanism, weil Reihenfolge sich ändert
            datasize = self.config.size

            query_answer = self.run_query(databases) 
            mechanismed_answer = self.mechanism.apply_mechanism(query_answer, delta=0.0, epsilon=self.epsilon, datasize=datasize)
            attacker_decision = self.attack_model.run(mechanismed_answer, databases)
            return self.check_decision(attacker_decision)


    #selected database is always the first one
    def run_query(self, databases):
        selected_database = databases[0]
        return selected_database.run_query()

    #Searched database is always the first one
    def check_decision(self, attacker_decision):
        
        if attacker_decision == 0:
            return True 
        else:
            return False
