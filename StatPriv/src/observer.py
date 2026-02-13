import csv
from src.data_source import DataSource
from src.mechanism import Mechanism
from abc import ABC, abstractmethod
from models.config import Config
from pathlib import Path
import json
import os


SCRIPT_DIR = Path(__file__).resolve().parent.parent
REPORT_CSV = 'reports/csv'
PATH = SCRIPT_DIR / REPORT_CSV

class Observer(ABC):
    @abstractmethod
    def update(self, info) -> None:
        pass


class SuccessRateObserver(Observer):
    def __init__(self):
        self.success_rate: float = 0
        self.nr_run: int = 0
        self.correctly_guessed: int = 0


    def update(self, info):
        if info == True or info == False:
            self.nr_run = self.nr_run + 1
            if info == True:
                self.correctly_guessed = self.correctly_guessed + 1
            self.success_rate = self.correctly_guessed / self.nr_run

    def finalize(self):
        print(f"Nr runs: {self.nr_run}")
        print(f"Nr times correctly guessed: {self.correctly_guessed}")
        print(f"Success_rate: {self.success_rate}")

class DataGeneratorObserver(Observer):
    def __init__(self, file_name):
        self.success_rate: float = 0
        self.nr_run: int = 0
        self.correctly_guessed: int = 0
        self.config = None
        self.file_name = file_name

    def update(self, info):
        if type(info) == Config:
            self.config = info 

        if info == True or info == False:
            self.nr_run = self.nr_run + 1
            if info == True:
                self.correctly_guessed = self.correctly_guessed + 1
            self.success_rate = self.correctly_guessed / self.nr_run

    def finalize(self):
        advantage = abs(self.success_rate - 0.5)


        file_path = PATH / self.file_name
        fieldnames = [
                'Datasource', 
                'Database size',
                'p',
                'mean',
                'std',
                'p_list',
                'H0 value',
                'H1 value',
                'Query',
                'Mechanism',
                'Sample Size',
                'Scale',
                'Attack Model',
                'Alpha-value',
                'Success Rate',
                'Advantage',
                'Monte Carlo Runcount',
                'Relative Utility Loss'
                ]

        file_exists = os.path.isfile(file_path)
        rel_util_loss = None
        util_loss = getattr(self.config.mechanism, "util_loss", None)
        if util_loss:
            rel_util_loss = self.calculate_relative_utility_loss(
                self.config.mechanism.util_loss, 
                self.config.sensitivity
            )
            

        with open(file_path, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            

            #Fill data with config information
            data =  [{
                    'Database size': self.config.size,
                    'Query': type(self.config.query).__name__,
                    'H0 value': self.config.added_values[0],
                    'H1 value': self.config.added_values[1],
                    'Success Rate': self.success_rate,
                    'Advantage': advantage,
                    'Monte Carlo Runcount': self.nr_run,
                    'Attack Model': self.config.attack_type,
                    'Alpha-value': self.config.alpha,
                    'Relative Utility Loss' : rel_util_loss
                    }]
                    
            data_source_information = self.datasource_to_row(self.config.datasource)
            mechanism_information = self.mechanism_to_row(self.config.mechanism)
            data[0].update(data_source_information)
            data[0].update(mechanism_information)

            if not file_exists:
                writer.writeheader()
            writer.writerows(data)


    def datasource_to_row(self, data_source: DataSource) -> dict[str, any]:
        """
        Convert any DataSource instance into a flat CSV row (dict).
        Keeps a consistent schema across different source classes.
        """
        base = {
                "Datasource": type(data_source).__name__,
                }

        # Source-specific fieldata_source (fill missing with None)
        if type(data_source).__name__ == "BernoulliSource":
            base.update({
                "p": getattr(data_source, "p", None),
                "mean": None,
                "std": None,
                "p_list": None,
                })

        elif type(data_source).__name__ == "TenSource":
            p = getattr(data_source, "p", None)
            p = [round(prob, 3) for prob in p]
            base.update({
                "p": None,
                "mean": None,
                "std": None,
                "p_list": json.dumps(p) if p is not None else None,
                })

        elif type(data_source).__name__ == "GaussianSource":
            base.update({
                "p": None,
                "mean": getattr(data_source, "mean", None),
                "std": getattr(data_source, "std", None),
                "p_list": None,
                })

        else:
            # Unknown datasource: still write something usable
            base.update({
                "p": getattr(data_source, "p", None),
                "mean": getattr(data_source, "mean", None),
                "std": getattr(data_source, "std", None),
                "p_list": json.dumps(getattr(data_source, "p", None)) if isinstance(getattr(ds, "p", None), (list, tuple)) else None,
                })

        return base
        
    def mechanism_to_row(self, mechanism: Mechanism) -> dict[str, any]:
        """
        Convert any Mechanism instance into a flat CSV row (dict).
        Keeps a consistent schema across different mechanism classes.
        """
        base = {
                "Mechanism": type(mechanism).__name__,
                "Sample Size": getattr(mechanism, "sample_size", None),
                "Scale": getattr(mechanism, "scale", None),
                }
        return base

    def calculate_relative_utility_loss(self, util_loss, sensitivity):
        rel_util_loss = util_loss/pow(sensitivity,2)
        return rel_util_loss


class ExperimentGraphicObserver(Observer):
    def update(self, turnout) -> None:
        pass





