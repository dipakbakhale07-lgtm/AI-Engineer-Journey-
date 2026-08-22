import csv

def filter_students(min_marks):
    results = []

    with open("practise/students.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for student in reader:
            if int(student["marks"]) >= min_marks:
                results.append(student)

    return results

students = filter_students(80)

for student in students:
    print(student)