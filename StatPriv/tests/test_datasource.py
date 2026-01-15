import pytest
    
from src.data_source import *  
from models.database_configuration import DatabaseConfig 
from src.query import *
import numpy as np
from scipy import stats
from models.enums_query import QueryType

@pytest.fixture
def rng():
    return np.random.default_rng(seed=12345)

class TestBernoulliSource:
    def test_init_sets_attributes(self):
        source = BernoulliSource(p=0.3, size=10)

        assert source.p == 0.3
        assert source.size == 10
        assert source.domain == [0, 1]

    def test_likelihood_bernoulli_mean(self, rng):
        source = BernoulliSource(p=0.3, size=10)
        query = AverageQuery()
        data = source.load_data(rng)
         
        database_conf = DatabaseConfig(seed=12345, query=query, datasource=source, added_value=1, size=10)
        database_conf_2 = DatabaseConfig(seed=12345, query=query, datasource=source, added_value=0, size=10)
        likelihood = source.likelihood(database_conf, query, observed_value=0.353)
        likelihood2 = source.likelihood(database_conf_2, query, observed_value=0.353)

        assert likelihood != likelihood2

    def test_likelihood_bernoulli_median(self, rng):
        source = BernoulliSource(p=0.45, size=10)
        query = MedianQuery()
        data = source.load_data(rng)
         
        database_conf = DatabaseConfig(seed=12345, query=query, datasource=source, added_value=1, size=10)
        database_conf_2 = DatabaseConfig(seed=12345, query=query, datasource=source, added_value=0, size=10)
        likelihood = source.likelihood(database_conf, query, observed_value=0.353)
        likelihood2 = source.likelihood(database_conf_2, query, observed_value=0.353)

        assert likelihood != likelihood2

    def test_load_data(self, rng):
        source = BernoulliSource(p=0.3, size=10)
        data = source.load_data(rng)

        assert data.size == 10

    def test_select_value(self, rng):
        added_value = 3
        source = BernoulliSource(p=0.3, size=10)
        data = source.load_data(rng)

        data_changed = source.select_value(data, added_value)
        assert data_changed[-1] == added_value

    def test_random_variable(self):
        source = BernoulliSource(p=0.3, size=50)
        rv_1 = source.random_variable(probability=0.3, size=50)
        rv_2 = source.random_variable(probability=0.5, size=50)

        assert rv_1.mean()/50 == 0.3
        assert rv_1.mean() == source.query_distribution(0.3, QueryType.AVERAGE).mean()

    def snap_observed(self):
        source = BernoulliSource(p=0.3, size=10)
        observed = 0.0682
        expected = 0.1

        assert expected == source.snap_observed(observed)




