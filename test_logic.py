import pandas as pd
import duckdb
import pytest

def test_student_data_logic():
    """
    Test to verify that DuckDB correctly calculates KPIs 
    based on the standardized student data logic.
    """
    # 1. Create dummy data mimicking the 'Factors' dataset
    data = {
        'Exam_Score': [85, 40, 95, 20, 75],
        'Hours_Studied': [10, 2, 12, 1, 8],
        'Attendance': [95, 60, 100, 40, 80],
        'Gender': ['F', 'M', 'F', 'M', 'F']
    }
    df = pd.DataFrame(data)

    # 2. Initialize in-memory DuckDB
    con = duckdb.connect(database=':memory:')
    con.execute("CREATE TABLE student_data AS SELECT * FROM df")

    # 3. Test KPI: Average Score
    # Calculation: (85+40+95+20+75) / 5 = 63.0
    avg_score = con.execute("SELECT AVG(Exam_Score) FROM student_data").fetchone()[0]
    assert avg_score == 63.0, f"Expected 63.0, but got {avg_score}"

    # 4. Test KPI: Success Rate (Score >= 70)
    # 3 students (85, 95, 75) out of 5 = 60%
    total = con.execute("SELECT COUNT(*) FROM student_data").fetchone()[0]
    successes = con.execute("SELECT COUNT(*) FROM student_data WHERE Exam_Score >= 70").fetchone()[0]
    success_rate = (successes / total) * 100
    assert success_rate == 60.0, f"Expected 60.0, but got {success_rate}"

    # 5. Test Filter Logic: Female students only
    female_avg = con.execute("SELECT AVG(Exam_Score) FROM student_data WHERE Gender = 'F'").fetchone()[0]
    # (85+95+75) / 3 = 85.0
    assert female_avg == 85.0, f"Expected 85.0 for females, but got {female_avg}"

    print("✅ All logic tests passed successfully!")

if __name__ == "__main__":
    test_student_data_logic()