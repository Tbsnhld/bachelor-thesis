from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def load_data(self, rng: np.random.Generator, size: int | None = None):
        pass

class BinomialSource(DataSource):
    def __init__(self, p: float):
        self.p = p

    def load_data(self, rng: np.random.Generator, size: int | None = None):
        return rng.binomial(0, self.p, size=size)

class GaussianSource(DataSource):
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std

    def load_data(self, rng: np.random.Generator, size: int | None = None):
        return rng.normal(self.mean, self.std, size=size)

class CSVSource(DataSource):
    def __init__(self, filepath: str, column: str | None = None):
        self.filepath = filepath
        self.column = column

    def load_data(self, rng: np.random.Generator, size: int | None = None):
        ds = pd.read_csv(self.filepath)
        if self.column:
            data = ds[self.column]
        else:
            data = ds.select_dtypes(include='number').to_numpy()

        if size and len(data) > size:
            data = data[:size]
        return data
