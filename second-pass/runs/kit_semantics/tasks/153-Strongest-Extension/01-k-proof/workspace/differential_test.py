import itertools
import random

from solution import Strongest_Extension


def oracle(class_name, extensions):
    if not extensions:
        return class_name + "."

    def score(extension):
        return sum(
            1 if character.isupper()
            else -1 if character.islower()
            else 0
            for character in extension
        )

    best_index = max(
        range(len(extensions)),
        key=lambda index: score(extensions[index]),
    )
    return class_name + "." + extensions[best_index]


def main():
    cases = [
        ("Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
        ("my_class", ["AA", "Be", "CC"]),
        ("", []),
        ("Tie", ["Ab", "Cd", "XYzz"]),
        ("Unicode", ["é", "A", "ΩΩ", "ß"]),
    ]

    alphabet = "AaZz09_-"
    small_strings = [
        "".join(chars)
        for length in range(3)
        for chars in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(20260730)
    for _ in range(2000):
        class_name = rng.choice(small_strings)
        extensions = [
            rng.choice(small_strings)
            for _ in range(rng.randrange(0, 9))
        ]
        cases.append((class_name, extensions))

    mismatches = []
    for class_name, extensions in cases:
        actual = Strongest_Extension(class_name, extensions)
        expected = oracle(class_name, extensions)
        if actual != expected:
            mismatches.append(
                (class_name, extensions, actual, expected)
            )

    print(
        "differential_cases="
        f"{len(cases)} mismatches={len(mismatches)}"
    )
    if mismatches:
        for mismatch in mismatches[:10]:
            print(mismatch)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
