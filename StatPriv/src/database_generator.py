import numpy as np
from src.database import Database
from models.database_configuration import DatabaseConfig
from models.config import Config

class DatabaseGenerator:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.generate_databases()

    def reseed_databases(self, seed=None):
        self.config.seed = seed 
        self.generate_databases()

    def generate_databases(self): 
        config = self.config
        db_config = DatabaseConfig(config.seed, config.query, config.datasource, config.added_values[0], config.size)
        general_database = Database(db_config);
        first_database = general_database.clone_with_added_value(config.added_values[0])
        second_database = general_database.clone_with_added_value(config.added_values[1])
        self.databases = [first_database, second_database]

    def get_databases(self):
        return self.databases;
