import database as db

class Experiment():
    def __init__(self, dbconf, attack_model, mechanism):
        self.db = db.Database(dbconf)
        self.attack_model = attack_model
        self.mechanism = mechanism
