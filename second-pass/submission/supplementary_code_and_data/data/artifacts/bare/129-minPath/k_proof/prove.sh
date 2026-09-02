#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
proof_tmpdir="$(mktemp -d /work/minpath-proof.XXXXXXXX)"
trap 'rm -rf "$proof_tmpdir"' EXIT

# Recreate the submitted constructor program with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Independent executable check against exhaustive path enumeration: every 2x2
# permutation for k=1..7, followed by deterministic 3x3 samples.
python3 - <<'PY'
from itertools import permutations
from random import Random
from solution import minPath


def brute(grid, k):
    n = len(grid)
    states = [([grid[r][c]], r, c) for r in range(n) for c in range(n)]
    for _ in range(k - 1):
        following = []
        for values, r, c in states:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    following.append((values + [grid[nr][nc]], nr, nc))
        states = following
    return min(values for values, _, _ in states)


for cells in permutations(range(1, 5)):
    grid = [list(cells[:2]), list(cells[2:])]
    for k in range(1, 8):
        assert minPath(grid, k) == brute(grid, k)

rng = Random(129)
for _ in range(120):
    cells = list(range(1, 10))
    rng.shuffle(cells)
    grid = [cells[0:3], cells[3:6], cells[6:9]]
    k = rng.randrange(1, 7)
    assert minPath(grid, k) == brute(grid, k)
PY

# Build the executable semantics and exercise both examples from prompt.py.
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm

grid_example_1='vList(ListItem(vList(ListItem(vInt(1)) ListItem(vInt(2)) ListItem(vInt(3)))) ListItem(vList(ListItem(vInt(4)) ListItem(vInt(5)) ListItem(vInt(6)))) ListItem(vList(ListItem(vInt(7)) ListItem(vInt(8)) ListItem(vInt(9)))))'
grid_example_2='vList(ListItem(vList(ListItem(vInt(5)) ListItem(vInt(9)) ListItem(vInt(3)))) ListItem(vList(ListItem(vInt(4)) ListItem(vInt(1)) ListItem(vInt(6)))) ListItem(vList(ListItem(vInt(7)) ListItem(vInt(8)) ListItem(vInt(2)))))'

krun solution.mpy --definition semantic-kompiled \
  -cGRID="$grid_example_1" -cKLEN=3 --output pretty \
  > "$proof_tmpdir/krun-example-1.out"
krun solution.mpy --definition semantic-kompiled \
  -cGRID="$grid_example_2" -cKLEN=1 --output pretty \
  > "$proof_tmpdir/krun-example-2.out"
rg -q 'some' "$proof_tmpdir/krun-example-1.out"
rg -q 'some' "$proof_tmpdir/krun-example-2.out"

# The Haskell backend symbolically proves every reachability claim in spec.k.
kompile verification.k \
  --main-module MINPATH-VERIFICATION \
  --syntax-module MINPATH-VERIFICATION \
  --backend haskell
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MINPATH-SPEC \
  | tee "$proof_tmpdir/kprove.out"
rg -qx '#Top' "$proof_tmpdir/kprove.out"

# Non-vacuity probe: changing the first expected path must make proof fail.
sed '0,/path3(2)/s//path3(3)/' spec.k > "$proof_tmpdir/spec-mutated.k"
if kprove "$proof_tmpdir/spec-mutated.k" \
     -I /work \
     --definition verification-kompiled \
     --spec-module MINPATH-SPEC \
     > "$proof_tmpdir/mutation.out" 2>&1; then
  echo 'ERROR: mutated specification unexpectedly proved' >&2
  exit 1
fi
echo 'mutation probe failed as expected'
