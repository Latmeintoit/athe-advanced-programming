import pytest
from dataset_app.processors import DataCleaner, CSVDataSource
import os

# =====================================================================
# TASK 4: Automated Testing
# These unit tests automatically verify the logic of our application.
# Running these in a CI/CD pipeline prevents broken code from being deployed.
# =====================================================================

@pytest.fixture
def sample_data():
    """Fixture to provide sample data for tests."""
    return [
        {"id": 1, "username": "admin", "email": "admin@test.com"},
        {"id": 2, "username": "", "email": "user@test.com"},
        {"id": 3, "username": "guest", "email": ""}
    ]

def test_data_cleaner_removes_empty_usernames(sample_data):
    """Test that the cleaner correctly filters out records missing a username."""
    cleaner = DataCleaner()
    cleaned_data = cleaner.remove_empty_records(sample_data, required_key="username")
    
    assert len(cleaned_data) == 2
    assert cleaned_data[0]["id"] == 1
    assert cleaned_data[1]["id"] == 3

def test_csv_data_source_encapsulation():
    """Test that the file path is successfully encapsulated."""
    source = CSVDataSource("test.csv")
    
    # We shouldn't be able to access source.__file_path directly
    with pytest.raises(AttributeError):
        path = source.__file_path
        
    # We must use the getter
    assert source.get_file_path() == "Broken_Test.csv"
