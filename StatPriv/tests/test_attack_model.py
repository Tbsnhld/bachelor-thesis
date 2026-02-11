import pytest
from src.attack_model import MaximumLikelihood
import numpy as np
from helper import helper 
class TestMaximumLikelihood:
    def create_max_li(self, config):
        max_li = MaximumLikelihood(config)
        return max_li

    def test_likelihood(self):
        config = helper.make_config(added_values=[10,500], size=50, mean=40, std=15)
        databases = helper.make_database_generator(config)
        database = databases.databases[0]
        database2 = databases.databases[1]
        
        max_li = self.create_max_li(config)
        li_0 = max_li.likelihood(database, 15)
        li_1 = max_li.likelihood(database2, 15)

        assert li_0 > li_1

    def test_likelihood_ratio_equal(self):
        h0 = 0.434323
        h1 = 0.434323
        
        config = helper.make_config([0,1], 50, 0.5, None, None)
        max_li = self.create_max_li(config)

        assert max_li.likelihood_ratio(h0, h1) == 1

    def test_likelihood_ratio_above_one(self):
        h0 = 0.5
        h1 = 0.4
        
        config = helper.make_config([0,1], 50, 0.5, None, None)
        max_li = self.create_max_li(config)

        assert max_li.likelihood_ratio(h0, h1) > 1

    def test_likelihood_ratio_below_one(self):
        h0 = 0.4
        h1 = 0.5
        
        config = helper.make_config([0,1], 50, 0.5, None, None)
        max_li = self.create_max_li(config)

        assert max_li.likelihood_ratio(h0, h1) < 1

    def test_run(self):
        config = helper.make_config([10,500], 50, 0.5, 350, 100)
        database_generator = helper.make_database_generator(config)
        observed_answer = 400
        
        max_li = self.create_max_li(config)
        return_value = max_li.run(observed_answer, database_generator.get_databases())
        assert return_value == 1



