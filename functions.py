"""
Student Performance Analytics System - Reusable Functions Module
This module contains all analytical functions used by main.py.
"""

import pandas as pd
import numpy as np
import os


# Subject columns used throughout the analysis
SUBJECT_COLUMNS = [
    "Python",
    "Mathematics",
    "Statistics",
    "Data_Science",
    "Computer_Networks",
]

REQUIRED_COLUMNS = [
    "Student_ID",
    "Name",
    "Department",
] + SUBJECT_COLUMNS + ["Attendance"]


def load_data(filepath="students.csv"):
    """
    Load and validate the CSV dataset.
    Returns a cleaned DataFrame or raises informative errors.
    Does not silently fix or drop invalid records.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file '{filepath}' not found. "
            "Please ensure students.csv is in the same folder as main.py."
        )

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Unable to read CSV file: {e}")

    if len(df) == 0:
        raise ValueError("Dataset is empty. At least one student record is required.")

    # Check for required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Dataset is missing required columns: {missing_cols}. "
            f"Found columns: {list(df.columns)}"
        )

    # Unique Student_IDs
    if df["Student_ID"].duplicated().any():
        dupes = df.loc[df["Student_ID"].duplicated(keep=False), "Student_ID"].unique()
        raise ValueError(f"Duplicate Student_ID values found: {list(dupes)}")

    # Non-blank Name and Department
    if df["Name"].isna().any() or (df["Name"].astype(str).str.strip() == "").any():
        raise ValueError("One or more students have a blank Name.")
    if df["Department"].isna().any() or (df["Department"].astype(str).str.strip() == "").any():
        raise ValueError("One or more students have a blank Department.")

    # Validate that mark and attendance columns are numeric and in range 0–100
    numeric_cols = SUBJECT_COLUMNS + ["Attendance"]
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            bad_rows = df.index[df[col].isna()].tolist()
            raise ValueError(
                f"Column '{col}' contains non-numeric or missing values "
                f"(row indices: {bad_rows})."
            )
        if (df[col] < 0).any() or (df[col] > 100).any():
            raise ValueError(
                f"Column '{col}' has values outside the valid range 0–100. "
                "Please correct the dataset before analysis."
            )

    # Keep only required columns so extra CSV columns cannot affect subject maths
    df = df[REQUIRED_COLUMNS].copy()
    return df


def calculate_totals(df):
    """
    Calculate total marks for every student across all subjects.
    Uses Pandas sum along axis=1 (row-wise).
    """
    df = df.copy()
    df["Total_Marks"] = df[SUBJECT_COLUMNS].sum(axis=1)
    return df


def calculate_averages(df):
    """
    Calculate average marks for every student.
    Uses NumPy mean for the numerical calculation demonstration.
    """
    df = df.copy()
    # Convert subject scores to NumPy array for meaningful NumPy usage
    scores_array = df[SUBJECT_COLUMNS].to_numpy(dtype=float)
    # NumPy mean along axis=1 gives average per student
    df["Average_Marks"] = np.mean(scores_array, axis=1).round(2)
    return df


def assign_grades(df):
    """
    Assign letter grades based on average marks.
    Grade rules:
        A+ : >= 90
        A  : 80 - 89.99
        B  : 70 - 79.99
        C  : 60 - 69.99
        D  : 50 - 59.99
        F  : < 50
    """
    df = df.copy()

    def get_grade(avg):
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    # Apply grade function using a list comprehension + loop style for clarity
    grades = []
    for avg in df["Average_Marks"]:
        grades.append(get_grade(avg))
    df["Grade"] = grades
    return df


def assign_pass_fail(df):
    """
    Determine pass/fail status.
    A student passes only if they score at least 40 in EVERY subject.
    Uses NumPy for the numerical condition check.
    """
    df = df.copy()
    # Convert to NumPy array
    scores = df[SUBJECT_COLUMNS].to_numpy(dtype=float)
    # Check if all subjects >= 40 for each student (axis=1)
    passed = np.all(scores >= 40, axis=1)
    df["Status"] = np.where(passed, "Pass", "Fail")
    return df


def class_statistics(df):
    """
    Calculate overall class statistics:
    - Overall average
    - Highest average student
    - Lowest average student
    - Number of students
    """
    overall_avg = round(float(np.mean(df["Average_Marks"].to_numpy())), 2)
    highest_idx = df["Average_Marks"].idxmax()
    lowest_idx = df["Average_Marks"].idxmin()

    highest_student = {
        "Student_ID": df.loc[highest_idx, "Student_ID"],
        "Name": df.loc[highest_idx, "Name"],
        "Average": df.loc[highest_idx, "Average_Marks"],
        "Grade": df.loc[highest_idx, "Grade"],
    }
    lowest_student = {
        "Student_ID": df.loc[lowest_idx, "Student_ID"],
        "Name": df.loc[lowest_idx, "Name"],
        "Average": df.loc[lowest_idx, "Average_Marks"],
        "Grade": df.loc[lowest_idx, "Grade"],
    }

    return {
        "overall_average": overall_avg,
        "highest_student": highest_student,
        "lowest_student": lowest_student,
        "total_students": len(df),
    }


def subject_analysis(df):
    """
    Calculate subject-wise statistics: average, maximum, minimum.
    Uses both Pandas and NumPy.
    """
    results = {}
    for subject in SUBJECT_COLUMNS:
        values = df[subject].to_numpy(dtype=float)
        results[subject] = {
            "average": round(float(np.mean(values)), 2),
            "maximum": float(np.max(values)),
            "minimum": float(np.min(values)),
            "std_dev": round(float(np.std(values)), 2),
        }
    return results


def get_top_performers(df, n=5):
    """
    Rank and return the top n students by average marks.
    """
    top = df.nlargest(n, "Average_Marks")[
        ["Student_ID", "Name", "Department", "Average_Marks", "Grade", "Status"]
    ].copy()
    top = top.reset_index(drop=True)
    top.index = top.index + 1  # Rank starting from 1
    top.index.name = "Rank"
    return top


def attendance_analysis(df, threshold=75):
    """
    Calculate average attendance and identify students with low attendance.
    """
    avg_attendance = round(float(np.mean(df["Attendance"].to_numpy())), 2)
    low_attendance = df[df["Attendance"] < threshold][
        ["Student_ID", "Name", "Department", "Attendance"]
    ].copy()
    low_attendance = low_attendance.sort_values("Attendance").reset_index(drop=True)

    return {
        "average_attendance": avg_attendance,
        "low_attendance_students": low_attendance,
        "low_count": len(low_attendance),
        "threshold": threshold,
    }


def department_summary(df):
    """
    Department-wise performance summary (average marks and pass rate).
    """
    summary = (
        df.groupby("Department")
        .agg(
            Student_Count=("Student_ID", "count"),
            Avg_Marks=("Average_Marks", "mean"),
            Avg_Attendance=("Attendance", "mean"),
            Pass_Count=("Status", lambda x: (x == "Pass").sum()),
        )
        .reset_index()
    )
    summary["Avg_Marks"] = summary["Avg_Marks"].round(2)
    summary["Avg_Attendance"] = summary["Avg_Attendance"].round(2)
    summary["Pass_Rate_%"] = (
        (summary["Pass_Count"] / summary["Student_Count"]) * 100
    ).round(1)
    return summary


def display_report(df, class_stats, subject_stats, top_students, attendance_stats, dept_summary):
    """
    Display the complete analysis in a clean, readable terminal format.
    """
    separator = "=" * 70
    thin_sep = "-" * 70

    print(separator)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM - FULL REPORT")
    print(separator)

    # 1. Dataset overview
    print("\n1. DATASET OVERVIEW")
    print(thin_sep)
    print(f"   Total Students              : {class_stats['total_students']}")
    print(f"   Original CSV columns        : 9 (ID, Name, Dept, 5 subjects, Attendance)")
    print(f"   After analysis (enriched)   : {df.shape[1]} columns "
          f"(added Total_Marks, Average_Marks, Grade, Status)")
    print(f"   Dimensions                  : {df.shape[0]} rows x {df.shape[1]} columns")

    # 2. Student-wise results
    print("\n2. STUDENT-WISE RESULTS (Total, Average, Grade, Status, Attendance)")
    print(thin_sep)
    display_cols = [
        "Student_ID",
        "Name",
        "Department",
        "Total_Marks",
        "Average_Marks",
        "Grade",
        "Status",
        "Attendance",
    ]
    # Use to_string for clean alignment
    print(df[display_cols].to_string(index=False))

    # 3. Class statistics
    print("\n3. CLASS STATISTICS")
    print(thin_sep)
    print(f"   Overall Class Average Marks : {class_stats['overall_average']}")
    hs = class_stats["highest_student"]
    ls = class_stats["lowest_student"]
    print(
        f"   Highest Performing Student  : {hs['Name']} ({hs['Student_ID']}) "
        f"- Avg: {hs['Average']} | Grade: {hs['Grade']}"
    )
    print(
        f"   Lowest Performing Student   : {ls['Name']} ({ls['Student_ID']}) "
        f"- Avg: {ls['Average']} | Grade: {ls['Grade']}"
    )

    # 4. Subject-wise analysis
    print("\n4. SUBJECT-WISE PERFORMANCE")
    print(thin_sep)
    print(f"{'Subject':<22} {'Average':>10} {'Maximum':>10} {'Minimum':>10} {'Std Dev':>10}")
    print(thin_sep)
    for subject, stats in subject_stats.items():
        print(
            f"{subject:<22} {stats['average']:>10.2f} "
            f"{stats['maximum']:>10.0f} {stats['minimum']:>10.0f} "
            f"{stats['std_dev']:>10.2f}"
        )

    # Identify best and worst subjects
    best_subject = max(subject_stats, key=lambda s: subject_stats[s]["average"])
    worst_subject = min(subject_stats, key=lambda s: subject_stats[s]["average"])
    print(f"\n   Highest Average Subject : {best_subject} "
          f"({subject_stats[best_subject]['average']})")
    print(f"   Lowest Average Subject  : {worst_subject} "
          f"({subject_stats[worst_subject]['average']})")

    # 5. Pass / Fail summary
    print("\n5. PASS / FAIL SUMMARY")
    print(thin_sep)
    pass_count = (df["Status"] == "Pass").sum()
    fail_count = (df["Status"] == "Fail").sum()
    total = len(df)
    pass_pct = round((pass_count / total) * 100, 1)
    fail_pct = round((fail_count / total) * 100, 1)
    print(f"   Passed : {pass_count} students ({pass_pct}%)")
    print(f"   Failed : {fail_count} students ({fail_pct}%)")
    print("   Rule: Pass only if ALL five subjects are >= 40; otherwise Fail.")

    # 6. Top 5 performers
    print("\n6. TOP 5 STUDENTS (by Average Marks)")
    print(thin_sep)
    print(top_students.to_string())

    # 7. Department-wise summary
    print("\n7. DEPARTMENT-WISE PERFORMANCE SUMMARY")
    print(thin_sep)
    print(dept_summary.to_string(index=False))

    # 8. Attendance analysis
    print("\n8. ATTENDANCE ANALYSIS")
    print(thin_sep)
    print(f"   Class Average Attendance : {attendance_stats['average_attendance']}%")
    print(
        f"   Students with attendance below {attendance_stats['threshold']}% : "
        f"{attendance_stats['low_count']}"
    )
    if attendance_stats["low_count"] > 0:
        print("\n   List of students with low attendance:")
        print(attendance_stats["low_attendance_students"].to_string(index=False))
    else:
        print("   No students have low attendance.")

    # 9. Final summary
    print("\n" + separator)
    print("                         FINAL SUMMARY")
    print(separator)
    print(f"   • Total students analysed     : {total}")
    print(f"   • Overall class average       : {class_stats['overall_average']}")
    print(f"   • Top student                 : {hs['Name']} ({hs['Average']})")
    print(f"   • Students passed             : {pass_count} ({pass_pct}%)")
    print(f"   • Students failed             : {fail_count} ({fail_pct}%)")
    print(f"   • Best subject                : {best_subject}")
    print(f"   • Weakest subject             : {worst_subject}")
    print(f"   • Average attendance          : {attendance_stats['average_attendance']}%")
    print(f"   • Low attendance students     : {attendance_stats['low_count']}")
    print(separator)
    print("   Analysis completed successfully.")
    print(separator)
