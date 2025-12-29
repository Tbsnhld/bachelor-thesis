import numpy as np
from models.database_configuration import DatabaseConfig
class Database:
    def __init__(self, config: DatabaseConfig) -> None:
        self.rng = np.random.default_rng(config.seed)
        self.config = config
        self.datasource = config.datasource
        self.data = self.datasource.load_data(self.rng, size=config.size)

    def run_query(self):
        return self.config.query.execute(self.data)

    def get_data(self):
        return self.data

    def clone_with_added_value(self, added_value):
        data = self.datasource.select_value(self.data, added_value)
        return data
