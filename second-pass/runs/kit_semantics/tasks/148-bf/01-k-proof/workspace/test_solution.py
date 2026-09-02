import ast
import itertools

from solution import bf


PLANETS = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)
INVALID = ("", "Pluto", "mercury", "Sun", "Neptune ", "🪐", "Earth\0")


def oracle(planet1, planet2):
    positions = {name: position for position, name in enumerate(PLANETS)}
    if planet1 not in positions or planet2 not in positions:
        return ()
    low = min(positions[planet1], positions[planet2])
    high = max(positions[planet1], positions[planet2])
    return tuple(
        name
        for position, name in enumerate(PLANETS)
        if low < position < high
    )


def main():
    inputs = PLANETS + INVALID
    mismatches = []
    for planet1, planet2 in itertools.product(inputs, repeat=2):
        actual = bf(planet1, planet2)
        expected = oracle(planet1, planet2)
        if actual != expected:
            mismatches.append((planet1, planet2, actual, expected))

    with open("solution.py", encoding="utf-8") as solution_file:
        solution_tree = ast.parse(solution_file.read())
    with open("krun_examples.py", encoding="utf-8") as krun_file:
        krun_tree = ast.parse(krun_file.read())
    same_function_ast = ast.dump(solution_tree.body[0]) == ast.dump(krun_tree.body[0])

    print(f"pairs_checked={len(inputs) ** 2}")
    print(f"mismatches={len(mismatches)}")
    print(f"krun_function_ast_matches_solution={same_function_ast}")
    if mismatches or not same_function_ast:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
