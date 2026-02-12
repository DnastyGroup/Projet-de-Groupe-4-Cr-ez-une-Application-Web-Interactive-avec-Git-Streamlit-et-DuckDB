import pandas as pd
import duckdb
import pytest

def run_quality_tests():
    """
    Comprehensive logic tests for DuckDB integration and KPI calculations.
    """
    print("\n" + "="*30)
    print("🚀 STARTING QUALITY ASSURANCE TESTS")
    print("="*30)

    # 1. Create controlled mock data
    mock_data = {
        'exam_score': [100, 40, 70],  # Average: 70.0 | Successes: 2 (100 and 70)
        'study_hours': [10, 2, 5],
        'gender': ['F', 'M', 'F']
    }
    df = pd.DataFrame(mock_data)

    # 2. Setup DuckDB
    try:
        con = duckdb.connect(database=':memory:')
        con.execute("CREATE TABLE student_data AS SELECT * FROM df")
        print("✅ DuckDB connection and table creation: OK")

        # TEST 1: Average Score Calculation
        avg_score = con.execute("SELECT AVG(exam_score) FROM student_data").fetchone()[0]
        assert avg_score == 70.0
        print(f"✅ KPI Test (Average Score): PASSED (Got {avg_score})")

        # TEST 2: Success Rate Logic (Score >= 70)
        total = con.execute("SELECT COUNT(*) FROM student_data").fetchone()[0]
        successes = con.execute("SELECT COUNT(*) FROM student_data WHERE exam_score >= 70").fetchone()[0]
        success_rate = (successes / total) * 100
        assert success_rate == (2/3) * 100
        print(f"✅ KPI Test (Success Rate): PASSED (Got {success_rate:.1f}%)")

        # TEST 3: Data Filtering Logic
        male_count = con.execute("SELECT COUNT(*) FROM student_data WHERE gender = 'M'").fetchone()[0]
        assert male_count == 1
        print(f"✅ Filter Test (Gender): PASSED (Got {male_count} male student)")

        print("\n" + "="*30)
        print("⭐ ALL TESTS PASSED SUCCESSFULLY ⭐")
        print("="*30)

    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        exit(1)

if __name__ == "__main__":
    run_quality_tests()