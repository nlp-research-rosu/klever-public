import ast
from itertools import product
from pathlib import Path

from solution import is_happy


def oracle(s):
    if len(s) < 3:
        return False
    return all(len({s[i], s[i + 1], s[i + 2]}) == 3 for i in range(len(s) - 2))


def first_function_ast(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    return ast.dump(tree.body[0], include_attributes=False)


# The LLVM smoke program must exercise the exact function AST in solution.py.
assert first_function_ast("solution.py") == first_function_ast("smoke.py")

examples = {
    "a": False,
    "aa": False,
    "abcd": True,
    "aabb": False,
    "adb": True,
    "xyy": False,
    "abca": True,
    "abac": False,
    "åßç": True,
    "ååç": False,
}

for text, expected in examples.items():
    assert oracle(text) is expected
    assert is_happy(text) is expected

count = 0
for length in range(8):
    for chars in product("abc", repeat=length):
        text = "".join(chars)
        assert is_happy(text) is oracle(text)
        count += 1

print(f"differential cases: {count + len(examples)}, mismatches: 0")
