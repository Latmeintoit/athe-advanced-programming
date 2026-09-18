from processors import CSVDataSource, JSONDataSource, DataCleaner, DataPipeline
import os

def create_dummy_data():
    """Helper function to create a dummy dataset for testing the application."""
    with open('dummy_dataset.csv', 'w') as f:
        f.write("id,name,value\n")
        f.write("1,Alice,100\n")
        f.write("2,,200\n") # Missing name
        f.write("3,Bob,300\n")

def main():
    print("--- Starting Large Dataset Application ---")
    
    # 1. Create a dummy dataset (simulating downloading from datasetlist.com)
    create_dummy_data()

    # 2. Instantiate our OOP classes
    csv_source = CSVDataSource('dummy_dataset.csv')
    cleaner = DataCleaner()

    # 3. Inject dependencies into our Pipeline (Dependency Inversion)
    pipeline = DataPipeline(data_source=csv_source, cleaner=cleaner)

    # 4. Run the application
    print("Processing CSV Data...")
    results = pipeline.run_pipeline(required_key='name')
    
    print("\nCleaned Data Results (Notice row 2 with missing name is gone):")
    for row in results:
        print(row)
        
    # Cleanup dummy data
    if os.path.exists('dummy_dataset.csv'):
        os.remove('dummy_dataset.csv')

if __name__ == "__main__":
    main()
