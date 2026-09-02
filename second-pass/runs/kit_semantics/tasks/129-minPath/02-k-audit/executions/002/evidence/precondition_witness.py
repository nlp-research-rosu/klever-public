#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

work = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/audit-work/minpath-129")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath

candidate = load("witness_candidate", work / "solution.py")
canonical = load("witness_canonical", work / "canonical.py")

def formal_values(flat, n, k):
    one_index = flat.index(1)
    row, col = divmod(one_index, n)
    grid = [flat[i:i+n] for i in range(0, n*n, n)]
    vals = []
    for rr, cc in ((row-1,col),(row+1,col),(row,col-1),(row,col+1)):
        if 0 <= rr < n and 0 <= cc < n:
            vals.append(grid[rr][cc])
    neighbor = min(vals)
    out = [1 if i % 2 == 0 else neighbor for i in range(k)]
    valid_perm = len(flat) == n*n and set(flat) == set(range(1, n*n+1))
    return grid, row, col, neighbor, out, valid_perm

flat, n, k = [1,2,3,4], 2, 3
grid, row, col, neighbor, formal_out, valid = formal_values(flat, n, k)
witnesses = {
    "inner-one-ahead": {"I": row, "J": col},
    "inner-no-one": {"I": row, "J": col + 1},
    "outer-one-ahead": {"I": 0},
    "outer-one-past": {"I": 1, "J": 0},
    "scan-finish": {"initial_i": 0, "initial_row": 0, "initial_col": 0},
    "neighbor-finish": {"R": row, "C": col},
    "result-loop-tail": {"R": 1, "A": []},
    "minpath-full-contract": {"N": n, "K": k},
}
checks = {
    "validPerm": valid,
    "one_position_in_bounds": 0 <= row < n and 0 <= col < n,
    "inner_one_ahead_pre": 0 <= row < n and 0 <= col <= n and row == row and col <= col,
    "inner_no_one_pre": 0 <= row < n and 0 <= col + 1 <= n and not (row == row and col + 1 <= col),
    "outer_one_ahead_pre": 0 <= 0 <= n and 0 <= row,
    "outer_one_past_pre": 0 <= 1 <= n and 1 > row and (1 < n or 0 == n),
    "result_loop_pre": 1 > 0 and k > 0,
    "full_target_pre": n >= 2 and k > 0 and valid,
}
candidate_out = candidate([r[:] for r in grid], k)
canonical_out = canonical([r[:] for r in grid], k)
result = {
    "P": flat, "N": n, "K": k, "grid": grid,
    "oneRow": row, "oneCol": col, "neighborMin": neighbor,
    "witness_assignments": witnesses, "precondition_checks": checks,
    "formal_finishRel_output": formal_out,
    "candidate_output": candidate_out, "canonical_output": canonical_out,
    "all_preconditions_satisfied": all(checks.values()),
    "all_outputs_equal": formal_out == candidate_out == canonical_out,
}
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(0 if result["all_preconditions_satisfied"] and result["all_outputs_equal"] else 1)
