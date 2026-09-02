"""Independent finite checks for the Python implementation and K harness."""

import ast
import itertools

from solution import filter_integers


class IntegerSubclass(int):
    pass


def oracle(values):
    """Classify through the concrete type's MRO, not through isinstance()."""
    return [
        value
        for value in values
        if any(base is int for base in type(value).__mro__)
    ]


def function_ast(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "filter_integers"
    )


solution_function = function_ast("solution.py")
harness_function = function_ast("concrete-tests.py")
assert ast.dump(solution_function) == ast.dump(harness_function)

pool = [
    -2,
    0,
    7,
    True,
    False,
    IntegerSubclass(9),
    3.5,
    "text",
    None,
    [],
    {},
    (1,),
]

checked = 0
for length in range(5):
    for values in itertools.product(pool, repeat=length):
        actual = filter_integers(list(values))
        expected = oracle(values)
        assert actual == expected, (values, actual, expected)
        checked += 1

print(f"python differential: {checked} lists, 0 mismatches")
print("solution/concrete K harness function ASTs: identical")
