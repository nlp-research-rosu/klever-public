import random

from solution import concatenate


def main() -> None:
    rng = random.Random(20260724)
    alphabet = ["", "a", "Z", " ", "\n", "é", "λ", "🙂"]
    cases = [
        [],
        [""],
        ["a", "b", "c"],
        ["", "xy", "", "z"],
        ["é", "λ", "🙂"],
    ]
    for _ in range(250):
        cases.append(
            [
                "".join(rng.choice(alphabet) for _ in range(rng.randrange(5)))
                for _ in range(rng.randrange(9))
            ]
        )

    mismatches = 0
    for strings in cases:
        expected = "".join(strings)
        actual = concatenate(strings)
        if actual != expected:
            mismatches += 1
            print("MISMATCH", repr(strings), repr(actual), repr(expected))

    print(f"cases={len(cases)} mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
