import ast
import inspect

import concrete_tests
import solution


def oracle(a, b, c):
    x, y, z = sorted((a, b, c))
    return x * x + y * y == z * z


examples = [
    (3, 4, 5, True),
    (1, 2, 3, False),
    (5, 12, 13, True),
    (6, 8, 10, True),
    (2, 2, 3, False),
    (3.0, 4.0, 5.0, True),
    (1.5, 2.0, 2.5, True),
    (3, 4.0, 5, True),
    (1.0, 2, 3.0, False),
    (0.3, 0.4, 0.5, True),
]

for a, b, c, expected in examples:
    assert solution.right_angle_triangle(a, b, c) is expected

mismatches = []
tested = 0
for a in range(1, 31):
    for b in range(1, 31):
        for c in range(1, 31):
            tested += 1
            actual = solution.right_angle_triangle(a, b, c)
            expected = oracle(a, b, c)
            if actual != expected:
                mismatches.append((a, b, c, actual, expected))

for a2 in range(1, 21):
    for b2 in range(1, 21):
        for c2 in range(1, 21):
            a = a2 / 2
            b = b2 / 2
            c = c2 / 2
            tested += 1
            actual = solution.right_angle_triangle(a, b, c)
            expected = oracle(a, b, c)
            if actual != expected:
                mismatches.append((a, b, c, actual, expected))

solution_def = ast.parse(inspect.getsource(solution.right_angle_triangle)).body[0]
concrete_def = ast.parse(
    inspect.getsource(concrete_tests.right_angle_triangle)
).body[0]
assert ast.dump(solution_def) == ast.dump(concrete_def)
assert not mismatches, mismatches[:10]

print(
    f"validation: examples={len(examples)}, "
    f"positive_numeric_triples={tested}, mismatches={len(mismatches)}, "
    "concrete_harness_ast=identical"
)
