import pytest
from src.database import Database
from models.enums_data_source import DataSourceType
from src import factory 
import numpy as np
class TestDatabase:

    def test_get_data(self):
        config = factory.make_database_config(size=50)
        db = Database(config)
        data = db.get_data()


        assert data.size == 50

    def test_clone_with_added_value(self):
        config = factory.make_database_config(added_value=1)
        db = Database(config)
        clone = db.clone_with_added_value(0)
        data_db = db.get_data()
        data_clone = clone.get_data()

        assert data_clone[data_clone.size-1] == 0
        assert data_clone[data_clone.size-1] != data_db[data_db.size - 1]
        



