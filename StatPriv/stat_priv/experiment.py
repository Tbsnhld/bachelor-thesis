import database as db
from mechanism import GaussianNoise, LaplaceNoise, Mechanism
from attack_model import AttackModel
from config import Config

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
        if isinstance(self.mechanism, LaplaceNoise):
            return self._run_laplace()

        if isinstance(self.mechanism, GaussianNoise):
            return self._run_gaussian()


    def _run_laplace(self):
        if self.config != None:
            self.db = db.Database(self.config)
            data = self.db.data
            mechanismed_data = self.mechanism.apply_mechanism(data, delta=0.0, epsilon=self.epsilon)
            decision = self.attack_model.run(mechanismed_data)
            return decision 

    def _run_gaussian(self):
        self.db = db.Database(self.config)
        data = self.db.data
        average = data.get_average()
        mechanismed_data = self.mechanism.apply_mechanism(data, delta=self.delta, epsilon=self.epsilon)
        decision = self.attack_model.run(mechanismed_data)
        return decision 

    def _run_subsampling(self):
        self.db = db.Database(self.config)
        data = self.db.data
        mechanismed_data = self.mechanism.apply_mechanism(data, sample_size=self.sample_size)
        decision = self.attack_model.run(mechanismed_data)
        ##return decision
        pass
