import pandas as pd
import duckdb

def test_kpi_calculations():
    """
    Test if DuckDB correctly calculates the average score KPI.
    """
    print("Running DuckDB logic tests...")
    
    # 1. Create mock data
    mock_data = {
        'exam_score': [50, 100, 60], # Average should be 70.0
        'study_hours': [2, 8, 5],
        'attendance': [70, 95, 80]
    }
    df_test = pd.DataFrame(mock_data)
    
    # 2. Connect to DuckDB in-memory
    connection = duckdb.connect(database=':memory:')
    connection.execute("CREATE TABLE students AS SELECT * FROM df_test")
    
    # 3. Run the SQL query used in the app
    result = connection.execute("SELECT AVG(exam_score) FROM students").fetchone()[0]
    
    # 4. Assert the result
    expected_value = 70.0
    if result == expected_value:
        print(f"✅ TEST PASSED: Calculated average ({result}) matches expected value.")
    else:
        print(f"❌ TEST FAILED: Expected {expected_value}, but got {result}")
        raise ValueError("KPI calculation error in DuckDB!")

if __name__ == "__main__":
    test_kpi_calculations()