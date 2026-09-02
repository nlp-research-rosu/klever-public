import random

from solution import numerical_letter_grade


def table_oracle(grades):
    cutoffs = [
        (4.0, "A+", "equal"),
        (3.7, "A", "greater"),
        (3.3, "A-", "greater"),
        (3.0, "B+", "greater"),
        (2.7, "B", "greater"),
        (2.3, "B-", "greater"),
        (2.0, "C+", "greater"),
        (1.7, "C", "greater"),
        (1.3, "C-", "greater"),
        (1.0, "D+", "greater"),
        (0.7, "D", "greater"),
        (0.0, "D-", "greater"),
    ]
    result = []
    for grade in grades:
        chosen = "E"
        for cutoff, letter, relation in cutoffs:
            if relation == "equal" and grade == cutoff:
                chosen = letter
                break
            if relation == "greater" and grade > cutoff:
                chosen = letter
                break
        result.append(chosen)
    return result


boundary_values = [
    0.0, 0.1, 0.7, 0.8, 1.0, 1.1, 1.3, 1.4, 1.7, 1.8,
    2.0, 2.1, 2.3, 2.4, 2.7, 2.8, 3.0, 3.1, 3.3, 3.4,
    3.7, 3.8, 4.0, 0, 1, 2, 3, 4,
]

rng = random.Random(20260729)
cases = [[], boundary_values, [4.0, 3, 1.7, 2, 3.5]]
for _ in range(1000):
    length = rng.randrange(0, 25)
    case = []
    for _ in range(length):
        if rng.randrange(4) == 0:
            case.append(rng.randrange(0, 5))
        else:
            case.append(rng.randrange(0, 401) / 100.0)
    cases.append(case)

mismatches = 0
for case in cases:
    expected = table_oracle(case)
    actual = numerical_letter_grade(case)
    if actual != expected:
        mismatches += 1
        print("mismatch", case, expected, actual)

print(f"cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
