import ast
import subprocess

from solution import prime_length


def oracle_is_prime(n):
    if n < 2:
        return False
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            return False
        candidate += 1
    return True


def main():
    with open("solution.py", encoding="utf-8") as stream:
        solution_tree = ast.parse(stream.read(), filename="solution.py")
    with open("concrete-smoke.py", encoding="utf-8") as stream:
        smoke_tree = ast.parse(stream.read(), filename="concrete-smoke.py")
    solution_function = next(
        node for node in solution_tree.body if isinstance(node, ast.FunctionDef)
    )
    smoke_function = next(
        node for node in smoke_tree.body if isinstance(node, ast.FunctionDef)
    )
    assert ast.dump(solution_function, include_attributes=False) == ast.dump(
        smoke_function, include_attributes=False
    )

    generated = subprocess.run(
        ["python3", "py2mpy.py", "solution.py"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    with open("solution.mpy", encoding="utf-8") as stream:
        assert stream.read() == generated

    prompt_cases = {
        "Hello": True,
        "abcdcba": True,
        "kittens": True,
        "orange": False,
    }
    for string, expected in prompt_cases.items():
        assert prime_length(string) is expected

    mismatches = []
    for length in range(0, 201):
        string = "x" * length
        actual = prime_length(string)
        expected = oracle_is_prime(length)
        if actual is not expected:
            mismatches.append((length, actual, expected))

    print("artifact identity: solution.mpy regenerated exactly")
    print("concrete smoke function AST: identical to solution.py")
    print("prompt examples: 4 passed")
    print("differential domain: string lengths 0..200")
    print("oracle: independent trial division through floor(sqrt(n))")
    print("mismatches:", len(mismatches))
    if mismatches:
        raise AssertionError(mismatches)


if __name__ == "__main__":
    main()
