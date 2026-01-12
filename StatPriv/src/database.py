import numpy as np
from models.database_configuration import DatabaseConfig
class Database:
    def __init__(self, db_config: DatabaseConfig) -> None:
        self.rng = np.random.default_rng(db_config.seed)
        self.db_config = db_config
        self.datasource = db_config.datasource
        self.data = self.datasource.load_data(self.rng)

    def run_query(self):
        return self.db_config.query.execute(self.data)

    def get_data(self):
        return self.data

    def clone_with_added_value(self, added_value):
        conf = self.db_config.with_added_value(added_value)
        new_database = Database(conf)
        new_database.data = self.datasource.select_value(self.data, added_value)
        return new_database 
