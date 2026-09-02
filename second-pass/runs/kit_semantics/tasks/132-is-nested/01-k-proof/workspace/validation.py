import ast
import itertools

from solution import is_nested


def brute_force_oracle(value):
    target = "[[]]"
    for positions in itertools.combinations(range(len(value)), 4):
        candidate = "".join(value[position] for position in positions)
        if candidate == target:
            return True
    return False


def implementation_body(path):
    with open(path, encoding="utf-8") as source_file:
        module = ast.parse(source_file.read(), filename=path)
    return ast.dump(module.body[0], include_attributes=False)


assert implementation_body("solution.py") == implementation_body("concrete_tests.py")

checked = 0
mismatches = []
for size in range(13):
    for characters in itertools.product("[]", repeat=size):
        value = "".join(characters)
        expected = brute_force_oracle(value)
        actual = is_nested(value)
        checked += 1
        if actual != expected:
            mismatches.append((value, actual, expected))

print("oracle=brute-force four-index subsequence search")
print("domain=all square-bracket strings of lengths 0..12")
print("checked=" + str(checked))
print("mismatches=" + str(len(mismatches)))
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
