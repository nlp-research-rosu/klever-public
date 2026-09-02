import ast

from solution import is_simple_power


def oracle(x, n):
    """Enumerate n**e for e >= 0 using multiplication, independently."""
    if n == 0:
        return x == 1 or x == 0
    if n == 1:
        return x == 1
    if n == -1:
        return x == 1 or x == -1

    power = 1
    limit = max(1, abs(x))
    while abs(power) <= limit:
        if power == x:
            return True
        power *= n
    return False


def function_ast(path):
    with open(path, encoding="utf-8") as stream:
        tree = ast.parse(stream.read(), filename=path)
    return ast.dump(tree.body[0], include_attributes=False)


assert function_ast("solution.py") == function_ast("smoke.py")

mismatches = []
cases = 0
for x in range(-100, 101):
    for n in range(-12, 13):
        cases += 1
        actual = is_simple_power(x, n)
        expected = oracle(x, n)
        if actual != expected:
            mismatches.append((x, n, actual, expected))

print(f"cases={cases} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:20])
    raise SystemExit(1)
