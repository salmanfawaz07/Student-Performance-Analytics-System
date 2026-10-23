# Project Documentation  
## Student Performance Analytics System

---

### 1. Project Title and Student Details

**Project Title:** Student Performance Analytics System  

**Student Details**  
- Name: [Your Full Name]  
- Roll Number / Student ID: [Your Roll Number]  
- Course: Python with AI (EWB Courses)  
- Institution: [Your College / University Name]  
- Submission Date: [Date of Submission]

---

### 2. Objective

The main objective of this project is to develop a functional Python application that:

- Reads student academic records from a CSV file  
- Processes the data using Pandas and NumPy  
- Generates meaningful academic performance statistics  
- Answers key analytical questions about student performance, subject strength, pass/fail rates, and attendance  

The system is designed to run completely offline on a local Windows machine after the required Python packages have been installed.

---

### 3. Problem Statement

Educational institutions and teachers often need quick insights into class performance. Manually calculating averages, identifying weak students, and checking attendance is time-consuming and error-prone.  

This project solves that problem by providing a simple, automated Python tool that:

- Loads student data from a CSV file  
- Calculates totals, averages, grades, and pass/fail status  
- Produces subject-wise, department-wise, and attendance analyses  
- Displays a complete, readable report in the terminal  

No database, web server, paid API, or machine-learning model is required.

---

### 4. Technologies Used

| Technology | Version Guidance | Role in the Project |
|------------|------------------|---------------------|
| Python     | 3.8+             | Core language       |
| Pandas     | ≥ 1.5            | Data loading, DataFrame operations, grouping, filtering, sorting |
| NumPy      | ≥ 1.23           | Numerical averages, max/min, boolean array conditions |
| CSV        | —                | Data storage format |

---

### 5. Dataset Description

**File name:** `students.csv`  

**Number of records:** 25 fictional students  

**Columns:**

| Column Name         | Data Type | Description |
|---------------------|-----------|-------------|
| Student_ID          | String    | Unique ID (S001–S025) |
| Name                | String    | Student name (fictional) |
| Department          | String    | Computer Science / Information Technology / Electronics |
| Python              | Integer   | Marks out of 100 |
| Mathematics         | Integer   | Marks out of 100 |
| Statistics          | Integer   | Marks out of 100 |
| Data_Science        | Integer   | Marks out of 100 |
| Computer_Networks   | Integer   | Marks out of 100 |
| Attendance          | Integer   | Percentage (0–100) |

The dataset intentionally contains:
- Students who pass all subjects  
- Students who fail one or more subjects (score < 40)  
- High and low attendance cases  
- Variation across three departments  

No missing or invalid values are present in the supplied file.

---

### 6. Implementation Methodology (Step by Step)

1. **Project setup**  
   Create the folder structure, `requirements.txt`, and `.gitignore`.

2. **Dataset creation**  
   Prepare a realistic `students.csv` with at least 20 students and the required columns.

3. **Reusable functions (`functions.py`)**  
   Implement ten modular functions:
   - `load_data()` – load & validate CSV  
   - `calculate_totals()` – row-wise sum of subject marks  
   - `calculate_averages()` – row-wise average using NumPy  
   - `assign_grades()` – map average to letter grade  
   - `assign_pass_fail()` – check minimum 40 in every subject  
   - `class_statistics()` – overall average, highest & lowest student  
   - `subject_analysis()` – subject-wise mean, max, min, std  
   - `get_top_performers()` – top 5 by average  
   - `attendance_analysis()` – average attendance + low-attendance list  
   - `display_report()` – formatted terminal output  
   - (Extra helper) `department_summary()` – department-wise aggregation  

4. **Main program (`main.py`)**  
   - Print project title  
   - Call `load_data()` and handle errors  
   - Enrich the DataFrame with calculated columns  
   - Call analysis functions  
   - Call `display_report()` to show the complete output  

5. **Testing**  
   Run the program, verify calculations against manual checks, and test error cases (missing file, wrong columns).

6. **Documentation**  
   Write `README.md` and this `Project_Documentation.md`.

---

### 7. Explanation of Python Fundamentals Used

| Concept              | Where it is used |
|----------------------|------------------|
| Variables & data types | Storing DataFrames, dictionaries of statistics, numeric averages |
| Lists                | `SUBJECT_COLUMNS`, `REQUIRED_COLUMNS`, building grade lists |
| Dictionaries         | Returning structured results from `class_statistics()`, `subject_analysis()`, etc. |
| Conditions / if-elif | Grade assignment logic, pass/fail decision, attendance threshold |
| For loops            | Iterating over subjects for statistics, building grade list |
| Functions            | All analytical logic is modularised into reusable functions |
| Error handling       | `try-except` blocks for missing file, invalid data, unexpected errors |
| Modules / imports    | Separating concerns between `main.py` and `functions.py` |

---

### 8. Explanation of NumPy Operations

NumPy is used meaningfully, not just for the sake of using it:

- **`np.mean(..., axis=1)`** – calculates each student’s average marks from a 2-D array of subject scores.  
- **`np.all(scores >= 40, axis=1)`** – checks whether every subject mark is ≥ 40 for each student (pass/fail).  
- **`np.where(condition, "Pass", "Fail")`** – creates the Status column efficiently.  
- **`np.mean`, `np.max`, `np.min`, `np.std`** – used in subject-wise and attendance calculations.  

These operations work directly on NumPy arrays obtained from the Pandas DataFrame via `.to_numpy()`.

---

### 9. Explanation of Pandas Operations

| Operation | Purpose |
|-----------|---------|
| `pd.read_csv()` | Load the dataset into a DataFrame |
| `.columns`, `.shape`, `.dtypes` | Inspect structure |
| `.sum(axis=1)` | Calculate total marks per student |
| `.nlargest()` | Select top 5 performers |
| Boolean filtering (`df[df["Attendance"] < 75]`) | Find low-attendance students |
| `.groupby("Department").agg(...)` | Department-wise summary |
| `.to_string()` | Clean tabular display in the terminal |

Pandas vectorised operations are preferred wherever they are clearer and more efficient than explicit Python loops.

---

### 10. Description of Reusable Functions

| Function | Responsibility |
|----------|----------------|
| `load_data(filepath)` | Load CSV, check existence, validate required columns and numeric types |
| `calculate_totals(df)` | Add `Total_Marks` column |
| `calculate_averages(df)` | Add `Average_Marks` column (NumPy mean) |
| `assign_grades(df)` | Add `Grade` column based on defined rules |
| `assign_pass_fail(df)` | Add `Status` column (Pass/Fail) |
| `class_statistics(df)` | Return overall average + highest/lowest student info |
| `subject_analysis(df)` | Return dictionary of subject-wise statistics |
| `get_top_performers(df, n=5)` | Return ranked top-n DataFrame |
| `attendance_analysis(df, threshold=75)` | Return average attendance + low-attendance students |
| `department_summary(df)` | Return department-wise aggregation |
| `display_report(...)` | Print the complete formatted report |

---

### 11. Grading and Pass/Fail Logic

**Grade Rules (based on Average Marks):**

- A+ : ≥ 90  
- A  : 80 – 89.99  
- B  : 70 – 79.99  
- C  : 60 – 69.99  
- D  : 50 – 59.99  
- F  : < 50  

**Pass/Fail Rules:**

- Pass → score ≥ 40 in **every** subject  
- Fail → score < 40 in **any** subject  

**Attendance:**

- < 75% → Low attendance  
- ≥ 75% → Satisfactory  
(Attendance does **not** affect the academic Pass/Fail status.)

---

### 12. Key Features

- Complete offline operation after package installation  
- Clear error messages for missing file or invalid data  
- Student-wise, subject-wise, department-wise, and attendance analyses  
- Top-5 ranking  
- Readable terminal report with sections and a final summary  
- Modular code that is easy to understand and defend in a viva  

---

### 13. Actual Output and Findings

Results obtained by running `python main.py` on the included `students.csv` (25 students):

| Metric | Value |
|--------|-------|
| Total students | 25 |
| Overall class average | 67.3 |
| Highest student | Rohan Mehta (S003) — Average 92.0, Grade A+ |
| Lowest student | Pooja Nambiar (S018) — Average 38.2, Grade F |
| Passed | 21 students (84.0%) |
| Failed | 4 students (16.0%) |
| Failed Student IDs | S005 (Python 38), S011 (Math 39, Networks 38), S018 (multiple below 40), S022 (Math 35, Data_Science 38) |
| Best subject (avg) | Data_Science — 68.24 |
| Weakest subject (avg) | Computer_Networks — 65.84 |
| Subject minimums in dataset | Python 35, Mathematics 35, Statistics 38, Data_Science 38, Computer_Networks 36 |
| Average attendance | 80.4% |
| Low attendance (below 75%) | 8 students |
| Department pass rates | Computer Science 81.8%, Electronics 71.4%, Information Technology 100% |

**Pass/fail consistency:** The rule "at least 40 in every subject" is applied uniformly with `np.all(scores >= 40, axis=1)`. Siddharth Rao (S015) has Python = 49 and is correctly marked Pass. There is no inconsistency between S005 and S015 in the current dataset.

Automated tests (`python -m unittest test_functions.py -v`) cover boundary cases (39 vs 40), grade cut-offs, totals/averages, validation, and ranking. All 25 tests pass.
<img width="394" height="569" alt="image" src="https://github.com/user-attachments/assets/f9298643-6729-4c2d-965f-27d7d667eec7" />

---

### 14. Screenshots Section

**Instructions for adding real screenshots:**

1. Run `python main.py` in Command Prompt / PowerShell.  
2. Capture the terminal output (use Windows Snipping Tool or Print Screen).  
3. Save the images as `screenshot1.png`, `screenshot2.png`, etc. inside the project folder or a `screenshots/` subfolder.  
4. Insert them here in the final PDF or printed report:

   - Screenshot 1: Project title and dataset preview  
   - Screenshot 2: Student-wise results table  
   - Screenshot 3: Class statistics + subject-wise performance  
   - Screenshot 4: Pass/Fail summary + Top 5 students  
   - Screenshot 5: Department summary + Attendance analysis + Final summary  

*(Screenshots are not embedded in this Markdown file; add them when preparing the printed/PDF submission.)*

---

### 15. Challenges Faced and Solutions

| Challenge | Solution |
|-----------|----------|
| Ensuring pass/fail is consistent for every student | Single function `assign_pass_fail()` using `np.all(scores >= 40, axis=1)` — same rule for student table, counts, and department rates |
| Validating marks without silently changing data | `load_data()` raises clear `ValueError` for out-of-range, non-numeric, duplicate IDs, blank names, or empty file |
| Explaining why enriched DataFrame has more columns | Report states original CSV has 9 columns; after analysis 13 (added Total, Average, Grade, Status) |
| Subject minimum of 35 not visible in first 10 rows | Confirmed in full CSV: S018 Python=35, S022 Mathematics=35 — correct, not a bug |
| Making tests independent of production data | `test_functions.py` builds tiny controlled DataFrames; never modifies `students.csv` |
| Consistent column names across files | Single `SUBJECT_COLUMNS` and `REQUIRED_COLUMNS` list in `functions.py` |
| NumPy vs Pandas choice | NumPy for array mean/all/where; Pandas for DataFrame load, filter, group, sort |
| Avoiding modification of original CSV | All functions work on `df.copy()` |
| Readable terminal output | Separators, `to_string()` alignment, clear section headings |
| Missing file handling | Explicit `FileNotFoundError` with a user-friendly message |

---

### 16. Learning Outcomes

By building this project the student learns:

- How to structure a small Python project with multiple modules  
- Practical use of Pandas DataFrames for real tabular data  
- Meaningful application of NumPy for numerical computation  
- Writing reusable functions and clean main-program flow  
- Basic error handling and data validation  
- Generating human-readable analytical reports  
- Preparing professional README and documentation suitable for academic submission  

---

### 17. Final Outcome

A complete, working Student Performance Analytics System has been developed. The program successfully:

- Loads and validates the student dataset  
- Calculates all required academic metrics  
- Identifies top performers, weak subjects, and low-attendance students  
- Produces a comprehensive terminal report  

The project meets all the stated requirements of the EWB Courses “Python with AI” assignment and is ready for local execution, testing, and GitHub submission.

---

### 18. GitHub Repository Link

Repository URL: `https://github.com/[your-username]/student-performance-analytics`

*(Replace the placeholder with the actual URL after the repository has been created and the code has been pushed.)*

---

**End of Project Documentation**
<img width="301" height="568" alt="image" src="https://github.com/user-attachments/assets/1de06928-ceda-42c3-b014-a7ba77398154" />
![Uploading image.png…]()

