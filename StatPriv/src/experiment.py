from src.mechanism import GaussianNoise, LaplaceNoise, Mechanism
from src.attack_model import AttackModel
from src.config import Config
from src.database import Database

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
            db = Database(self.config)
            data = db.get_data()
            # Für subsampling: data und query answer in apply_mechanism, weil Reihenfolge sich ändert
            datasize = self.config.size
            query_answer = db.run_query()
            mechanismed_answer = self.mechanism.apply_mechanism(query_answer, delta=0.0, epsilon=self.epsilon, datasize=datasize)
            attacker_decision = self.attack_model.run(mechanismed_answer)
            return self.check_decision(attacker_decision)



    def check_decision(self, attacker_decision):
        actual_added = int(self.config.added_value)
        print(attacker_decision)
        if actual_added == attacker_decision:
            return True 
        else:
            return False


#        if isinstance(self.mechanism, LaplaceNoise):
#            return self._run_laplace()
#
#        if isinstance(self.mechanism, GaussianNoise):
#            return self._run_gaussian()
#
#
#    def _run_laplace(self):
#        if self.config != None:
#            self.db = db.Database(self.config)
#            data = self.db.data
#            mechanismed_data = self.mechanism.apply_mechanism(data, delta=0.0, epsilon=self.epsilon)
#            decision = self.attack_model.run(mechanismed_data)
#            return decision 
#
#    def _run_gaussian(self):
#        self.db = db.Database(self.config)
#        data = self.db.data
#        average = data.get_average()
#        mechanismed_data = self.mechanism.apply_mechanism(data, delta=self.delta, epsilon=self.epsilon)
#        decision = self.attack_model.run(mechanismed_data)
#        return decision 
#
#    def _run_subsampling(self):
#        self.db = db.Database(self.config)
#        data = self.db.data
#        mechanismed_data = self.mechanism.apply_mechanism(data, sample_size=self.sample_size)
#        decision = self.attack_model.run(mechanismed_data)
#        ##return decision
#        pass
