def numerical_letter_grade(grades):
    result = []
    grade = 0.0
    for grade in grades:
        grade = float(grade)
        if grade == 4.0:
            result.append("A+")
        elif grade > 3.7:
            result.append("A")
        elif grade > 3.3:
            result.append("A-")
        elif grade > 3.0:
            result.append("B+")
        elif grade > 2.7:
            result.append("B")
        elif grade > 2.3:
            result.append("B-")
        elif grade > 2.0:
            result.append("C+")
        elif grade > 1.7:
            result.append("C")
        elif grade > 1.3:
            result.append("C-")
        elif grade > 1.0:
            result.append("D+")
        elif grade > 0.7:
            result.append("D")
        elif grade > 0.0:
            result.append("D-")
        else:
            result.append("E")
    return result


assert numerical_letter_grade([]) == []
assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == [
    "A+", "B", "C-", "C", "A-"
]
assert numerical_letter_grade([
    4.0, 3.8, 3.7, 3.5, 3.3, 3.1, 3.0, 2.8, 2.7, 2.4, 2.3, 2.1,
    2.0, 1.8, 1.7, 1.4, 1.3, 1.1, 1.0, 0.8, 0.7, 0.1, 0.0
]) == [
    "A+", "A", "A-", "A-", "B+", "B+", "B", "B", "B-", "B-", "C+",
    "C+", "C", "C", "C-", "C-", "D+", "D+", "D", "D", "D-", "D-", "E"
]
