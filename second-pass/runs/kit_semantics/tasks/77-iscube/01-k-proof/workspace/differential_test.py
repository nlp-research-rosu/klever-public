from solution import iscube


def independent_oracle(a):
    cubes = {n * n * n for n in range(-10, 11)}
    return a in cubes


inputs = list(range(-1000, 1001))
mismatches = [
    (a, iscube(a), independent_oracle(a))
    for a in inputs
    if iscube(a) != independent_oracle(a)
]

print(f"inputs: {len(inputs)}")
print(f"range: {inputs[0]}..{inputs[-1]}")
print(f"mismatches: {len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
