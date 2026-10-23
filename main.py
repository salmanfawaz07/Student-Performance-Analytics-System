"""
Student Performance Analytics System
Main entry point of the application.

Run with:  python main.py
"""

import sys
import pandas as pd

from functions import (
    load_data,
    calculate_totals,
    calculate_averages,
    assign_grades,
    assign_pass_fail,
    class_statistics,
    subject_analysis,
    get_top_performers,
    attendance_analysis,
    department_summary,
    display_report,
    SUBJECT_COLUMNS,
)


def main():
    """Main program flow."""
    print("=" * 70)
    print("          STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("          Python | NumPy | Pandas | CSV")
    print("=" * 70)

    # ------------------------------------------------------------------
    # 1. Load and validate dataset
    # ------------------------------------------------------------------
    try:
        df = load_data("students.csv")
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error while loading data: {e}")
        sys.exit(1)

    print("\nDataset loaded successfully.")
    print(f"Shape: {df.shape[0]} students x {df.shape[1]} columns")
    print("\n--- Dataset Preview (first 10 rows) ---")
    print(df.head(10).to_string(index=False))
    print("\n--- Data Types ---")
    print(df.dtypes)

    # ------------------------------------------------------------------
    # 2. Enrich the DataFrame with calculated columns
    # ------------------------------------------------------------------
    try:
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_grades(df)
        df = assign_pass_fail(df)
    except Exception as e:
        print(f"\n[ERROR] Calculation failed: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 3. Generate analytical results
    # ------------------------------------------------------------------
    try:
        class_stats = class_statistics(df)
        subject_stats = subject_analysis(df)
        top_students = get_top_performers(df, n=5)
        attendance_stats = attendance_analysis(df, threshold=75)
        dept_summary = department_summary(df)
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 4. Display the complete report
    # ------------------------------------------------------------------
    display_report(
        df,
        class_stats,
        subject_stats,
        top_students,
        attendance_stats,
        dept_summary,
    )


if __name__ == "__main__":
    main()
