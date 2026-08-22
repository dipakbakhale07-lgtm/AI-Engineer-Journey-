# DAY 3 — AI-ASSISTED CODING & DEBUGGING

## Challenge

30-Day AI Builder Challenge

## Day

DAY 03 / 30

## Objective

Practice controlling and debugging AI-assisted Python code instead of blindly accepting the output.

---

#AIAssistedCoding

AI can help with:

 # CodeGeneration
# CodeExplanation
# Debugging
# BugDetection
# TestCases
# Refactoring

But generated code must be understood and tested.

# Functions

A function is a reusable block of code.

def add(a, b):
    return a + b
add → #Function
a,b → #Inputs
return → #Output
#InputProcessingOutput

A useful way to understand code:

# Input
  ↓
# Processing
  ↓
# Output

Our CSV project:

# students.csv
      ↓
# ReadData
      ↓
# CheckMarks
      ↓
# Filter
      ↓
# MatchingStudents
#CSV

CSV = Comma-Separated Values

Example:

name,age,marks
Aarav,16,85
Rahul,16,91

Our program filtered students using:

if int(student["marks"]) >= min_marks:

With 80 as the minimum:

Aarav → 85 ✅
Rahul → 91 ✅
🐛 #Debugging

Debugging means finding and fixing problems in software.

Our workflow:

# Read
 ↓
# Understand
 ↓
# Identify
 ↓
# ix
 ↓
# Test
 #FileNotFoundError

We encountered a file-path problem because Python couldn't find:

students.csv

The actual file was inside:

practise/students.csv

After correcting the path, the program worked.

Lesson

When a file isn't found, check:

# FileExists?
 ↓
# CorrectName?
 ↓
# CorrectPath?
 ↓
# WorkingDirectory?
#NameError

We intentionally changed:

filter_students()

to:

filter_student()

Python produced a NameError because filter_student wasn't defined.

We restored:

filter_students()

and the program worked.

Lesson

Check:

# Spelling
# FunctionNames
# VariableNames
# Definitions
# PowerShellVsPython

Python code such as:

with open(...)

should be executed by Python, not directly as a PowerShell command.

For example:

py .\practise\csv_filter.py
# JSON

JSON = JavaScript Object Notation

Example:

{
  "name": "Dipak",
  "role": "AI Builder"
}

JSON is commonly used for structured data and API communication.
 
# APIAndJSON
# Application
 ↓
# APIRequest
 ↓
# Server
 ↓
# JSONResponse
 ↓
# Application

Our JSON practice successfully produced:

Name: Dipak
Role: AI Builder
Day: 3
Skills: Python, Machine Learning, LLMs, RAG
🧪 #Testing

A fix isn't complete just because the error disappears.

# Fix
 ↓
 Run
 ↓
# CheckOutput
 ↓
# ExpectedVsActual

For our CSV exercise:

Expected → marks >= 80
Actual   → Aarav 85, Rahul 91
Result   → #PASS ✅