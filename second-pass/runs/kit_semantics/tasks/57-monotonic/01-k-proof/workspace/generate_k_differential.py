import argparse
from itertools import product


def adjacent_pair_oracle(values):
    nondecreasing = all(
        values[index] <= values[index + 1]
        for index in range(len(values) - 1)
    )
    nonincreasing = all(
        values[index] >= values[index + 1]
        for index in range(len(values) - 1)
    )
    return nondecreasing or nonincreasing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    args = parser.parse_args()

    if args.shard_count < 1:
        parser.error("--shard-count must be positive")
    if not 0 <= args.shard_index < args.shard_count:
        parser.error("--shard-index must be in [0, shard-count)")

    print("def monotonic(l: list):")
    print("    return l == sorted(l) or l == sorted(l, reverse=True)")
    print()

    selected = 0
    total = 0
    for length in range(5):
        for values in product(range(-2, 3), repeat=length):
            values = list(values)
            if total % args.shard_count == args.shard_index:
                expected = adjacent_pair_oracle(values)
                print(f"assert monotonic({values!r}) == {expected!r}")
                selected += 1
            total += 1

    print()
    print(
        f"# generated_cases={selected} total_cases={total} "
        f"shard={args.shard_index}/{args.shard_count}"
    )


if __name__ == "__main__":
    main()
