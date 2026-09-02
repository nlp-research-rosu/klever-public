from solution import parse_nested_parens


def balanced_groups(pair_count):
    groups = []

    def visit(prefix, opened, closed):
        if opened == pair_count and closed == pair_count:
            groups.append(prefix)
            return
        if opened < pair_count:
            visit(prefix + "(", opened + 1, closed)
        if closed < opened:
            visit(prefix + ")", opened, closed + 1)

    visit("", 0, 0)
    return groups


def oracle(text):
    answer = []
    for group in text.split():
        prefix_depths = []
        running = 0
        for character in group:
            running += 1 if character == "(" else -1
            prefix_depths.append(running)
        answer.append(max(prefix_depths))
    return answer


groups = []
for pairs in range(1, 6):
    groups.extend(balanced_groups(pairs))

cases = {"", " ", "(()()) ((())) () ((())()())"}
for group in groups:
    cases.add(group)
    cases.add("  " + group + "  ")
for left in groups:
    for right in groups:
        cases.add(left + " " + right)
        cases.add(left + "   " + right)

mismatches = []
for case in sorted(cases):
    actual = parse_nested_parens(case)
    expected = oracle(case)
    if actual != expected:
        mismatches.append((case, actual, expected))

print(f"differential cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:10])
