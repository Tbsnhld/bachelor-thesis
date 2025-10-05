import pytest
from stat_priv.database import Database
import numpy as np
class TestDatabase:

    def test_reseed(self):
        gen1 = Database(seed=12)
        gen2 = Database(seed=12)

        assert np.array_equal(
            gen1.generate_data(3, 0.3),
            gen2.generate_data(3, 0.3)
        )

    ##def test_generate_data(self):
        ##assert Database.generate_data() = 

