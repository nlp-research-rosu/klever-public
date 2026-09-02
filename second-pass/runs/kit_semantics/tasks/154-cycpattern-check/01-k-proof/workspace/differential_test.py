from itertools import product

from solution import cycpattern_check


def oracle(a, b):
    if b == "":
        return True
    return any(b[i:] + b[:i] in a for i in range(len(b)))


def words(alphabet, maximum_length):
    yield ""
    for length in range(1, maximum_length + 1):
        for letters in product(alphabet, repeat=length):
            yield "".join(letters)


def main():
    cases = [
        ("abcd", "abd"),
        ("hello", "ell"),
        ("whassup", "psus"),
        ("abab", "baa"),
        ("efef", "eeff"),
        ("himenss", "simen"),
    ]
    corpus = list(words("ab", 4))
    cases.extend((a, b) for a in corpus for b in corpus)

    mismatches = []
    for a, b in cases:
        expected = oracle(a, b)
        actual = cycpattern_check(a, b)
        if actual != expected:
            mismatches.append((a, b, expected, actual))

    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(mismatch)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
