#!/usr/bin/env python3
"""Independent finite checks supporting the Stage 3 mathematical audit."""

from itertools import product


def operational_loop(codes, current=(), depth=0, accumulated=()):
    current = list(current)
    accumulated = list(accumulated)
    for code in codes:
        if code == 32:
            continue
        current.append(code)
        if code == 40:
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            accumulated.append(tuple(current))
            current = []
    return tuple(accumulated), tuple(current), depth


def scan_groups(codes, current=(), depth=0, accumulated=()):
    if not codes:
        return tuple(accumulated)
    code, rest = codes[0], codes[1:]
    if code == 32:
        return scan_groups(rest, current, depth, accumulated)
    if code == 40:
        return scan_groups(rest, current + (40,), depth + 1, accumulated)
    new_current = current + (code,)
    new_depth = depth - 1
    if new_depth == 0:
        return scan_groups(rest, (), 0, accumulated + (new_current,))
    return scan_groups(rest, new_current, new_depth, accumulated)


def balanced_tail_definition(codes, depth):
    if not codes:
        return depth == 0
    code, rest = codes[0], codes[1:]
    if code == 32:
        return balanced_tail_definition(rest, depth)
    if code == 40:
        return balanced_tail_definition(rest, depth + 1)
    return (
        code == 41
        and depth > 0
        and balanced_tail_definition(rest, depth - 1)
    )


def balanced_tail_oracle(codes, depth):
    for code in codes:
        if code == 32:
            continue
        if code not in (40, 41):
            return False
        depth += 1 if code == 40 else -1
        if depth < 0:
            return False
    return depth == 0


def paren_space_definition(codes):
    if not codes:
        return True
    return (
        codes[0] in (32, 40, 41)
        and paren_space_definition(codes[1:])
    )


def main():
    alphabet = (32, 40, 41, 120)
    checked = 0
    domain_cases = 0
    for length in range(8):
        for codes in product(alphabet, repeat=length):
            for current, depth, accumulated in (
                ((), 0, ()),
                ((40,), 1, ()),
                ((40, 40), 2, ((40, 41),)),
            ):
                output, _, _ = operational_loop(
                    codes, current, depth, accumulated
                )
                if balanced_tail_oracle(
                    codes, depth
                ) and paren_space_definition(codes):
                    assert output == scan_groups(
                        codes, current, depth, accumulated
                    )
                    checked += 1
            for depth in (0, 1, 2, -1):
                assert balanced_tail_definition(
                    codes, depth
                ) == balanced_tail_oracle(codes, depth)
            assert paren_space_definition(codes) == all(
                code in (32, 40, 41) for code in codes
            )
            if balanced_tail_oracle(codes, 0):
                domain_cases += 1

    witnesses = {
        "constant_empty_summary": (40, 41),
        "space_not_ignored": (32, 40, 41),
        "close_without_emit_reset": (40, 41, 40, 41),
        "invalid_char_uses_source_else_branch": (40, 120),
    }
    assert scan_groups(witnesses["constant_empty_summary"]) == ((40, 41),)
    assert operational_loop(witnesses["space_not_ignored"])[0] == ((40, 41),)
    assert scan_groups(witnesses["close_without_emit_reset"]) == (
        (40, 41),
        (40, 41),
    )
    assert operational_loop(witnesses["invalid_char_uses_source_else_branch"])[
        0
    ] == ((40, 120),)
    outside_invariant = ((40,), (120,), -1, ())
    assert operational_loop(*outside_invariant)[0] != scan_groups(
        *outside_invariant
    )
    outside_domain = ((41, 40), (), 0, ())
    assert operational_loop(*outside_domain)[0] != scan_groups(*outside_domain)

    print(f"operational_vs_scan_state_cases={checked}")
    print(f"balanced_top_level_domain_cases={domain_cases}")
    print("mismatches=0")
    for name, codes in witnesses.items():
        print(
            f"{name}: codes={codes} "
            f"operational={operational_loop(codes)} "
            f"scan={scan_groups(codes)}"
        )
    print(
        "out_of_invariant_boundary: "
        f"state={outside_invariant} "
        f"operational={operational_loop(*outside_invariant)[0]} "
        f"scan={scan_groups(*outside_invariant)}"
    )
    print(
        "out_of_domain_boundary: "
        f"state={outside_domain} "
        f"operational={operational_loop(*outside_domain)[0]} "
        f"scan={scan_groups(*outside_domain)}"
    )


if __name__ == "__main__":
    main()
