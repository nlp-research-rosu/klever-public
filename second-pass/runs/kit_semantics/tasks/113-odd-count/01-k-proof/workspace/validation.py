from itertools import product
from pathlib import Path
import ast
import random

from solution import odd_count


TEMPLATE = "the number of odd elements in the string i of the input."


def oracle(text):
    odd_digits = sum(character in "13579" for character in text)
    return TEMPLATE.replace("i", str(odd_digits))


strings = [""]
for length in range(1, 5):
    strings.extend("".join(chars) for chars in product("0123456789", repeat=length))

rng = random.Random(20260730)
for _ in range(500):
    length = rng.randrange(0, 81)
    strings.append("".join(rng.choice("0123456789") for _ in range(length)))

expected = [oracle(text) for text in strings]
actual = odd_count(strings)
assert actual == expected

solution_function = ast.parse(Path("solution.py").read_text()).body[0]
smoke_function = ast.parse(Path("concrete-smoke.py").read_text()).body[0]
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    smoke_function, include_attributes=False
)

print(f"DIFFERENTIAL_OK cases={len(strings)} mismatches=0")
print("SMOKE_BODY_MATCH")
