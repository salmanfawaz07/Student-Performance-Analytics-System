"""
Unit tests for Student Performance Analytics System.
Uses Python's built-in unittest framework.
Run with:  python -m unittest test_functions.py -v
"""

import unittest
import pandas as pd
import numpy as np
import os
import tempfile

from functions import (
    SUBJECT_COLUMNS,
    REQUIRED_COLUMNS,
    load_data,
    calculate_totals,
    calculate_averages,
    assign_grades,
    assign_pass_fail,
    class_statistics,
    subject_analysis,
    get_top_performers,
    department_summary,
)


def make_student(sid, name, dept, marks, attendance=80):
    """Helper: marks is a list of 5 subject scores."""
    row = {
        "Student_ID": sid,
        "Name": name,
        "Department": dept,
        "Attendance": attendance,
    }
    for col, val in zip(SUBJECT_COLUMNS, marks):
        row[col] = val
    return row


def make_df(rows):
    return pd.DataFrame(rows)


class TestPassFail(unittest.TestCase):
    """Pass only if every subject is >= 40."""

    def test_all_40_passes(self):
        df = make_df([make_student("T1", "Test", "CS", [40, 40, 40, 40, 40])])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_pass_fail(df)
        self.assertEqual(df.iloc[0]["Status"], "Pass")

    def test_one_39_fails(self):
        df = make_df([make_student("T2", "Test", "CS", [40, 39, 40, 40, 40])])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_pass_fail(df)
        self.assertEqual(df.iloc[0]["Status"], "Fail")

    def test_python_38_fails_even_if_others_high(self):
        df = make_df([make_student("T3", "Test", "CS", [38, 95, 95, 95, 95])])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_pass_fail(df)
        self.assertEqual(df.iloc[0]["Status"], "Fail")

    def test_one_40_and_rest_100_passes(self):
        df = make_df([make_student("T4", "Test", "CS", [40, 100, 100, 100, 100])])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_pass_fail(df)
        self.assertEqual(df.iloc[0]["Status"], "Pass")

    def test_multiple_below_40_fails(self):
        df = make_df([make_student("T5", "Test", "CS", [35, 42, 38, 40, 36])])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_pass_fail(df)
        self.assertEqual(df.iloc[0]["Status"], "Fail")


class TestGrades(unittest.TestCase):
    """Grade boundaries based on average marks."""

    def _grade_for_avg(self, avg):
        # Build a row whose average is exactly avg (all subjects = avg)
        marks = [avg] * 5
        df = make_df([make_student("G", "G", "CS", marks)])
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_grades(df)
        return df.iloc[0]["Grade"]

    def test_grade_90_is_A_plus(self):
        self.assertEqual(self._grade_for_avg(90), "A+")

    def test_grade_89_is_A(self):
        self.assertEqual(self._grade_for_avg(89), "A")

    def test_grade_80_is_A(self):
        self.assertEqual(self._grade_for_avg(80), "A")

    def test_grade_79_is_B(self):
        self.assertEqual(self._grade_for_avg(79), "B")

    def test_grade_70_is_B(self):
        self.assertEqual(self._grade_for_avg(70), "B")

    def test_grade_69_is_C(self):
        self.assertEqual(self._grade_for_avg(69), "C")

    def test_grade_60_is_C(self):
        self.assertEqual(self._grade_for_avg(60), "C")

    def test_grade_59_is_D(self):
        self.assertEqual(self._grade_for_avg(59), "D")

    def test_grade_50_is_D(self):
        self.assertEqual(self._grade_for_avg(50), "D")

    def test_grade_49_is_F(self):
        self.assertEqual(self._grade_for_avg(49), "F")


class TestTotalsAndAverages(unittest.TestCase):
    def test_total_and_average(self):
        marks = [80, 70, 60, 90, 50]  # total 350, avg 70.0
        df = make_df([make_student("A1", "Alice", "CS", marks)])
        df = calculate_totals(df)
        df = calculate_averages(df)
        self.assertEqual(df.iloc[0]["Total_Marks"], 350)
        self.assertEqual(df.iloc[0]["Average_Marks"], 70.0)


class TestTopPerformers(unittest.TestCase):
    def test_top_five_order(self):
        rows = [
            make_student("S1", "Low", "CS", [50, 50, 50, 50, 50]),
            make_student("S2", "High", "CS", [95, 95, 95, 95, 95]),
            make_student("S3", "Mid", "CS", [70, 70, 70, 70, 70]),
            make_student("S4", "Top2", "CS", [90, 90, 90, 90, 90]),
            make_student("S5", "Top3", "CS", [85, 85, 85, 85, 85]),
            make_student("S6", "Top4", "CS", [80, 80, 80, 80, 80]),
        ]
        df = make_df(rows)
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_grades(df)
        df = assign_pass_fail(df)
        top = get_top_performers(df, n=5)
        names = list(top["Name"])
        self.assertEqual(names[0], "High")
        self.assertEqual(names[1], "Top2")
        self.assertEqual(names[2], "Top3")
        self.assertEqual(names[3], "Top4")
        self.assertEqual(names[4], "Mid")


class TestValidation(unittest.TestCase):
    def _write_csv(self, content):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_data("definitely_does_not_exist_xyz.csv")

    def test_missing_required_column(self):
        # Missing Attendance
        content = (
            "Student_ID,Name,Department,Python,Mathematics,Statistics,"
            "Data_Science,Computer_Networks\n"
            "S1,A,CS,50,50,50,50,50\n"
        )
        path = self._write_csv(content)
        try:
            with self.assertRaises(ValueError) as ctx:
                load_data(path)
            self.assertIn("missing required columns", str(ctx.exception).lower())
        finally:
            os.remove(path)

    def test_duplicate_student_id(self):
        header = ",".join(REQUIRED_COLUMNS)
        row = "S1,Alice,CS,50,50,50,50,50,80"
        content = f"{header}\n{row}\n{row}\n"
        path = self._write_csv(content)
        try:
            with self.assertRaises(ValueError) as ctx:
                load_data(path)
            self.assertIn("duplicate", str(ctx.exception).lower())
        finally:
            os.remove(path)

    def test_invalid_mark_out_of_range(self):
        header = ",".join(REQUIRED_COLUMNS)
        # Python = 150 (invalid)
        row = "S1,Alice,CS,150,50,50,50,50,80"
        content = f"{header}\n{row}\n"
        path = self._write_csv(content)
        try:
            with self.assertRaises(ValueError) as ctx:
                load_data(path)
            self.assertIn("0", str(ctx.exception))  # mentions range 0-100
        finally:
            os.remove(path)

    def test_empty_dataset(self):
        header = ",".join(REQUIRED_COLUMNS)
        content = header + "\n"
        path = self._write_csv(content)
        try:
            with self.assertRaises(ValueError) as ctx:
                load_data(path)
            self.assertIn("empty", str(ctx.exception).lower())
        finally:
            os.remove(path)

    def test_non_numeric_mark(self):
        header = ",".join(REQUIRED_COLUMNS)
        row = "S1,Alice,CS,abc,50,50,50,50,80"
        content = f"{header}\n{row}\n"
        path = self._write_csv(content)
        try:
            with self.assertRaises(ValueError):
                load_data(path)
        finally:
            os.remove(path)


class TestPassFailCounts(unittest.TestCase):
    def test_pass_fail_totals(self):
        rows = [
            make_student("P1", "Pass1", "CS", [50, 50, 50, 50, 50]),
            make_student("F1", "Fail1", "CS", [39, 80, 80, 80, 80]),
            make_student("P2", "Pass2", "IT", [60, 60, 60, 60, 60]),
            make_student("F2", "Fail2", "IT", [100, 100, 100, 100, 30]),
        ]
        df = make_df(rows)
        df = calculate_totals(df)
        df = calculate_averages(df)
        df = assign_grades(df)
        df = assign_pass_fail(df)

        pass_count = (df["Status"] == "Pass").sum()
        fail_count = (df["Status"] == "Fail").sum()
        self.assertEqual(pass_count, 2)
        self.assertEqual(fail_count, 2)
        self.assertEqual(pass_count + fail_count, len(df))

        # Department pass rates
        dept = department_summary(df)
        cs = dept[dept["Department"] == "CS"].iloc[0]
        self.assertEqual(cs["Pass_Count"], 1)
        self.assertEqual(cs["Student_Count"], 2)


class TestSubjectAnalysis(unittest.TestCase):
    def test_subject_stats_ignore_non_subject_cols(self):
        rows = [
            make_student("S1", "A", "CS", [10, 20, 30, 40, 50], attendance=99),
            make_student("S2", "B", "CS", [60, 70, 80, 90, 100], attendance=50),
        ]
        df = make_df(rows)
        stats = subject_analysis(df)
        self.assertEqual(stats["Python"]["minimum"], 10)
        self.assertEqual(stats["Python"]["maximum"], 60)
        self.assertEqual(stats["Computer_Networks"]["minimum"], 50)
        self.assertEqual(stats["Computer_Networks"]["maximum"], 100)
        # Attendance must not appear as a subject
        self.assertNotIn("Attendance", stats)


if __name__ == "__main__":
    unittest.main()
