#!/usr/bin/env python3
"""Truth-table audit of the two proof-local simplification rules."""


def main() -> None:
    for a in (False, True):
        for b in (False, True):
            rule_1_guard = a
            rule_1_lhs = a == (a or b)
            rule_2_guard = not a
            rule_2_lhs = b == (a or b)
            print(
                f"A={a} B={b} "
                f"r1_guard={rule_1_guard} r1_lhs={rule_1_lhs} "
                f"r2_guard={rule_2_guard} r2_lhs={rule_2_lhs}"
            )
            if rule_1_guard and not rule_1_lhs:
                raise SystemExit("rule 1 is false")
            if rule_2_guard and not rule_2_lhs:
                raise SystemExit("rule 2 is false")
            if rule_1_guard and rule_2_guard:
                raise SystemExit("guards overlap")


if __name__ == "__main__":
    main()
