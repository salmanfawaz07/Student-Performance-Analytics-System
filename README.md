# Student Performance Analytics System

A beginner-friendly Python project that reads student academic records from a CSV file, processes the data using **Pandas** and **NumPy**, and generates meaningful academic performance statistics.

---

## Project Overview

This application analyses the academic performance of a class of students. It calculates totals, averages, grades, pass/fail status, subject-wise statistics, department-wise summaries, top performers, and attendance insights — all from a simple CSV dataset.

**Technology Stack:** Python 3 · NumPy · Pandas · CSV  
**Project Type:** Data analysis (not machine learning)  
**Platform:** Runs locally on Windows (or any OS with Python)

---

## Problem Statement

Educational institutions need a simple way to analyse student performance without complex software. This project provides a lightweight, offline Python solution that answers key questions such as:

- Which student has the highest / lowest average marks?
- What is the overall class average?
- Which subject has the highest / lowest average performance?
- How many students passed and failed?
- Who are the top five students?
- Which students have low attendance (< 75%)?

---

## Objectives

1. Load and validate student data from a CSV file.
2. Calculate total marks, average marks, grades, and pass/fail status for each student.
3. Generate class-level, subject-level, and department-level statistics.
4. Identify top performers and students with low attendance.
5. Present results in a clean, readable terminal report.
6. Demonstrate core Python, NumPy, and Pandas concepts suitable for a beginner course.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3   | Core programming language |
| Pandas     | CSV reading, DataFrame operations, filtering, grouping, sorting |
| NumPy      | Numerical averages, max/min, boolean conditions on arrays |
| CSV        | Simple flat-file storage of student records |

---

## Features

- Dataset validation (missing file, missing columns, non-numeric data)
- Student-wise total marks, average, grade, and pass/fail status
- Overall class average, highest and lowest performing students
- Subject-wise average, maximum, minimum, and standard deviation
- Pass/fail count and percentage
- Top 5 students ranked by average marks
- Department-wise performance summary (count, avg marks, pass rate)
- Attendance analysis (class average + list of low-attendance students)
- Clear, formatted terminal report
- Error handling for common failure cases

---

## Dataset Description

File: `students.csv`

| Column              | Description                          |
|---------------------|--------------------------------------|
| Student_ID          | Unique identifier (e.g., S001)       |
| Name                | Student full name (fictional)        |
| Department          | Computer Science / Information Technology / Electronics |
| Python              | Marks out of 100                     |
| Mathematics         | Marks out of 100                     |
| Statistics          | Marks out of 100                     |
| Data_Science        | Marks out of 100                     |
| Computer_Networks   | Marks out of 100                     |
| Attendance          | Attendance percentage (0–100)        |

- At least 20 fictional students
- Marks range 0–100; attendance 0–100
- Includes pass, fail, high and low attendance cases
- No missing or invalid values in the supplied dataset

---

## Project Folder Structure

```
student-performance-analytics/
├── main.py                  # Entry point – run this file
├── functions.py             # All reusable analytical functions
├── students.csv             # Student dataset (25 records)
├── test_functions.py        # Automated unit tests (unittest)
├── README.md                # This file
├── Project_Documentation.md # Detailed academic documentation
├── requirements.txt         # Python dependencies
└── .gitignore               # Git ignore rules
```

---

## Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your system
- pip (comes with Python)

### Steps (Windows)

1. Open **Command Prompt** or **PowerShell**.
2. Navigate to the project folder:
   ```cmd
   cd path\to\student-performance-analytics
   ```
3. (Optional but recommended) Create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install the required packages:
   ```cmd
   pip install -r requirements.txt
   ```

---

## How to Run the Project (Windows)

1. Make sure you are inside the project folder and the virtual environment is activated (if used).
2. Run:
   ```cmd
   python main.py
   ```
3. The complete analysis report will be printed in the terminal.

No internet connection is required after the packages have been installed.

### Run Automated Tests

```cmd
python -m unittest test_functions.py -v
```

This runs unit tests for pass/fail rules, grade boundaries, totals/averages, validation (duplicate IDs, invalid marks, missing columns, empty file), top-five ranking, and subject statistics.

---

## Sample Output Format

```
======================================================================
          STUDENT PERFORMANCE ANALYTICS SYSTEM
          Python | NumPy | Pandas | CSV
======================================================================

Dataset loaded successfully.
Shape: 25 students x 9 columns

--- Dataset Preview (first 10 rows) ---
...

1. DATASET OVERVIEW
...
2. STUDENT-WISE RESULTS ...
3. CLASS STATISTICS
4. SUBJECT-WISE PERFORMANCE
5. PASS / FAIL SUMMARY
6. TOP 5 STUDENTS
7. DEPARTMENT-WISE PERFORMANCE SUMMARY
8. ATTENDANCE ANALYSIS
...
FINAL SUMMARY
...
```

---

## Grading and Pass/Fail Rules

### Grade Rules (based on average marks)

| Grade | Average Marks     |
|-------|-------------------|
| A+    | 90 or above       |
| A     | 80 to below 90    |
| B     | 70 to below 80    |
| C     | 60 to below 70    |
| D     | 50 to below 60    |
| F     | below 50          |

### Pass / Fail Rules
- A student **passes** only if they score **at least 40 marks in every subject**.
- A student **fails** if they score below 40 in **any** subject.

### Attendance Rules
- Below 75% → Low attendance
- 75% or above → Satisfactory attendance  
(Attendance is analysed separately and does **not** affect academic pass/fail.)

---

## Example Analytical Questions Answered

| Question                              | How the program answers it                          |
|---------------------------------------|-----------------------------------------------------|
| Highest average student               | Class statistics section                            |
| Lowest average student                | Class statistics section                            |
| Overall class average                 | Class statistics section                            |
| Best / worst performing subject       | Subject-wise performance section                    |
| Number of students passed / failed    | Pass/Fail summary                                   |
| Top five students                     | Top 5 ranking                                       |
| Students with low attendance          | Attendance analysis section                         |
| Department performance comparison     | Department-wise summary                             |

## Actual Findings (from the supplied dataset)

When `python main.py` is run on the included `students.csv` (25 students):

| Metric | Result |
|--------|--------|
| Overall class average | 67.3 |
| Highest student | Rohan Mehta (S003) — Avg 92.0 (A+) |
| Lowest student | Pooja Nambiar (S018) — Avg 38.2 (F) |
| Passed / Failed | 21 (84%) / 4 (16%) |
| Failed students | S005, S011, S018, S022 (each has at least one subject &lt; 40) |
| Best subject (by average) | Data_Science (68.24) |
| Weakest subject | Computer_Networks (65.84) |
| Average attendance | 80.4% |
| Low attendance (&lt; 75%) | 8 students |
| Department pass rates | CS 81.8%, Electronics 71.4%, IT 100% |

**Pass/fail rule applied consistently:** a student fails if **any** subject is below 40. Siddharth Rao (S015) has Python = 49 and correctly **Passes**. Vikram Singh (S005) has Python = 38 and correctly **Fails**.

---

## Learning Outcomes

After completing and understanding this project, a student will be able to:

- Read and validate CSV data with Pandas
- Perform row-wise and column-wise calculations
- Use NumPy for numerical aggregation and boolean conditions
- Write modular, reusable functions
- Apply conditional logic for grading and pass/fail decisions
- Generate readable analytical reports in the terminal
- Handle common file and data errors gracefully
- Structure a simple Python project for submission

---

## Future Improvements

- Export the report to a text or PDF file
- Add a simple command-line menu for interactive queries
- Visualise subject averages with matplotlib (optional)
- Support multiple CSV files or academic years
- Add input validation when creating new student records

---

## Author Details

- **Name:** [Your Full Name]
- **Student ID / Roll No.:** [Your Roll Number]
- **Course:** Python with AI (EWB Courses)
- **Institution:** [Your College / University]
- **Academic Year:** [e.g., 2025-26]

---

## GitHub Repository

Repository URL: `https://github.com/[your-username]/student-performance-analytics`

*(Replace `[your-username]` with your actual GitHub username after you push the project.)*

---

## License

This project is created for academic submission purposes.
