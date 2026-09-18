from abc import ABC, abstractmethod
import csv
import json

# =====================================================================
# SOLID PRINCIPLE: Open/Closed Principle (OCP)
# The application is open for extension (we can add new data sources 
# like XMLDataSource) but closed for modification.
#
# OOP PILLAR: Abstraction
# We define an abstract base class that hides implementation details.
# =====================================================================
class DataSource(ABC):
    """Abstract base class representing a generic data source."""
    
    @abstractmethod
    def load_data(self) -> list[dict]:
        """Abstract method that all child classes must implement."""
        pass


# =====================================================================
# OOP PILLAR: Inheritance
# CSVDataSource inherits from the DataSource abstract class.
# =====================================================================
class CSVDataSource(DataSource):
    """Class responsible for loading data from a CSV file."""
    
    def __init__(self, file_path: str):
        # =============================================================
        # OOP PILLAR: Encapsulation
        # The file path is private (__file_path) and cannot be modified 
        # directly from outside the class.
        # =============================================================
        self.__file_path = file_path

    def get_file_path(self) -> str:
        """Getter for the private file path."""
        return self.__file_path

    def load_data(self) -> list[dict]:
        """Implementation of the abstract method for CSV files."""
        data = []
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Error: The file {self.__file_path} was not found.")
        return data


class JSONDataSource(DataSource):
    """Class responsible for loading data from a JSON file."""
    
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def load_data(self) -> list[dict]:
        """Implementation of the abstract method for JSON files."""
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.__file_path} was not found.")
            return []


# =====================================================================
# SOLID PRINCIPLE: Single Responsibility Principle (SRP)
# This class has only ONE job: cleaning and filtering the data. 
# It does not care where the data came from or where it goes.
# =====================================================================
class DataCleaner:
    """Class responsible for filtering and cleaning raw dataset rows."""
    
    def remove_empty_records(self, data: list[dict], required_key: str) -> list[dict]:
        """Removes dictionaries from the list that lack the required key."""
        cleaned = [row for row in data if row.get(required_key)]
        return cleaned


# =====================================================================
# SOLID PRINCIPLE: Dependency Inversion Principle (DIP)
# The DataPipeline depends on the abstract 'DataSource', NOT concrete 
# implementations like 'CSVDataSource'.
# =====================================================================
class DataPipeline:
    """Orchestrates the loading and processing of data."""
    
    def __init__(self, data_source: DataSource, cleaner: DataCleaner):
        self.data_source = data_source
        self.cleaner = cleaner

    def run_pipeline(self, required_key: str) -> list[dict]:
        # =============================================================
        # OOP PILLAR: Polymorphism
        # 'load_data()' behaves differently depending on whether 
        # data_source is a CSVDataSource or JSONDataSource at runtime.
        # =============================================================
        raw_data = self.data_source.load_data()
        cleaned_data = self.cleaner.remove_empty_records(raw_data, required_key)
        return cleaned_data
