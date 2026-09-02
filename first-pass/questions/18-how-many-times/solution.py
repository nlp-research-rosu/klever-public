# solution.py — canonical shape, ONE function. The slice-compare takes the
# sanctioned statement-level rewrite (inline window scan — the symbolic slice
# atom partially unfolds and never matches fold guards; see DEESCAPE.md #18).
# i/j/ok pre-bound for the fixed frame shape. Diff-tested.


def how_many_times(string, substring):
    times = 0
    i = 0
    ok = True
    j = 0
    for i in range(len(string) - len(substring) + 1):
        ok = True
        j = 0
        for j in range(len(substring)):
            if string[i + j] != substring[j]:
                ok = False
        if ok:
            times += 1
    return times
