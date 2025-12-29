from abc import ABC, abstractmethod
from scipy import stats
import numpy as np
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def load_data(self, rng: np.random.Generator):
        pass

    @abstractmethod
    def select_value(self, data, added_value):
        pass

class BernoulliSource(DataSource):
    def __init__(self, p: float, size: int):
        self.p = p
        self.size = size
        self.domain = list(range(2))

    def load_data(self, rng: np.random.Generator):
        data = rng.binomial(n=1, p=self.p, size=self.size)
        return data

    def select_value(self, data, added_value):
        size = data.size
        np.put(data, [size - 1], added_value)
        return data

    def random_variable(self):
        data = stats.binom(self.size, self.p)
        return data


class TenSource(DataSource):
    def __init__(self, size: int, p: (float)|None=None):
        self.p = p
        self.size = size
        self.domain = list(range(10))

    def load_data(self, rng: np.random.Generator):
        if self.p != None:
            data = rng.choice(a=self.domain, replace=True, p=self.p)
        else:
            data = rng.choice(a=self.domain, replace=True)
        return data

    def select_value(self, data, added_value):
        size = data.size
        np.put(data, [size - 1], added_value)
        return data

class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float, size: int):
        self.mean = mean
        self.std = std
        self.size = size
        self.domain = None

    def load_data(self, rng: np.random.Generator, added_value):
        data = np.round(rng.normal(self.mean, self.std, size=self.size), 3)
        return data

    def select_value(self, data, added_value):
        size = data.size
        np.put(data, [size - 1], added_value)
        return data

class CSVSource(DataSource):
    def __init__(self, filepath: str, column: str | None = None):
        self.filepath = filepath
        self.column = column

    def load_data(self, rng: np.random.Generator, size: int | None = None):
        ds = pd.read_csv(self.filepath)
        if self.column:
            self.data = ds[self.column]
        else:
            self.data = ds.select_dtypes(include='number').to_numpy()

        if size and len(self.data) > size:
            self.data = self.data[:size]
        return self.data
