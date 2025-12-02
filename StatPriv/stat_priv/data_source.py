from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class DataSource(ABC):
    @abstractmethod
    def load_data(self, rng: np.random.Generator, added_value, size: int | None = None):
        pass

class BernoulliSource(DataSource):
    def __init__(self, p: float):
        self.p = p
        self.domain = list(range(1))

    def load_data(self, rng: np.random.Generator, added_value, size: int | None = None):
        data = rng.binomial(n=1, p=self.p, size=size)
        data = self.select_value(added_value, data)
        return data

    def select_value(self, value, data):
        size = data.size
        np.put(data, [size - 1], value)
        return data


class TenSource(DataSource):
    def __init__(self, p: (float)|None=None):
        self.p = p
        self.domain = list(range(10))

    def load_data(self, rng: np.random.Generator, added_value, size: int | None = None):
        if self.p != None:
            data = rng.choice(a=self.domain, replace=True, p=self.p)
        else:
            data = rng.choice(a=self.domain, replace=True)
        data = self.select_value(added_value, data)
        return data

    def select_value(self, value, data):
        size = data.size
        np.put(data, [size - 1], value)
        return data

class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std
        self.domain = None

    def load_data(self, rng: np.random.Generator, added_value, size: int | None = None):
        data = np.round(rng.normal(self.mean, self.std, size=size), 3)
        data = self.select_value(added_value, data)
        return data

    def select_value(self, value, data):
        size = data.size
        np.put(data, [size - 1], value)
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
