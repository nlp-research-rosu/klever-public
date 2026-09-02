def numerical_letter_grade(grades):
    letter_grades = []
    grade = 0.0
    for grade in grades:
        if grade == 4.0:
            letter_grades.append("A+")
        elif grade > 3.7:
            letter_grades.append("A")
        elif grade > 3.3:
            letter_grades.append("A-")
        elif grade > 3.0:
            letter_grades.append("B+")
        elif grade > 2.7:
            letter_grades.append("B")
        elif grade > 2.3:
            letter_grades.append("B-")
        elif grade > 2.0:
            letter_grades.append("C+")
        elif grade > 1.7:
            letter_grades.append("C")
        elif grade > 1.3:
            letter_grades.append("C-")
        elif grade > 1.0:
            letter_grades.append("D+")
        elif grade > 0.7:
            letter_grades.append("D")
        elif grade > 0.0:
            letter_grades.append("D-")
        else:
            letter_grades.append("E")
    return letter_grades


observed_example = numerical_letter_grade([4.0, 3, 1.7, 2, 3.5])
observed_boundaries = numerical_letter_grade([
    4.0, 3.8, 3.7, 3.4, 3.3, 3.1, 3.0, 2.8, 2.7,
    2.4, 2.3, 2.1, 2.0, 1.8, 1.7, 1.4, 1.3, 1.1,
    1.0, 0.8, 0.7, 0.1, 0.0, -1.0, 5.0
])
observed_empty = numerical_letter_grade([])
