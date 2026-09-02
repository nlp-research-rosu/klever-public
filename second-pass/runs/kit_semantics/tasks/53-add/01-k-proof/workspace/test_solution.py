import operator

from solution import add


def main():
    values = (-100, -7, -1, 0, 1, 8, 100)
    checked = 0
    for x in values:
        for y in values:
            assert add(x, y) == operator.add(x, y)
            checked += 1
    print(f"CPython differential checks: {checked}; mismatches: 0")


if __name__ == "__main__":
    main()
