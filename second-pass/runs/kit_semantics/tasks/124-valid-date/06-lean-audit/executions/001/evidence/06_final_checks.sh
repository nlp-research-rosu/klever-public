#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
from pathlib import Path

from tools.klean_export import tree_digest

review = Path('/audit-output/REVIEW.md').read_text()
expected_end = 'VERDICT: PASS\nLEGITIMACY: LEGIT\n'
assert review.endswith(expected_end)
assert review.count('VERDICT: ') == 1
assert review.count('LEGITIMACY: ') == 1

assert tree_digest(Path('/reference/k-proof')) == (
    'b39714014c6857a733694c0cae5cffd66485b768998fb8b0432bfc875e0c95b8'
)
assert tree_digest(Path('/reference/klean-generation/generated')) == (
    'fca67d8c880040a1a2d653bcfbd2d7b52edeedac6ee618842ce89566fef07a17'
)
assert hashlib.sha256(
    Path('/reference/lemma-discovery.json').read_bytes()
).hexdigest() == (
    '32d52cfdbb4ece2bcc1496d4e59c4b26bc93fc385fb13b2ccbe6d9d55f5e9507'
)
assert not Path('/candidate').exists()

print('REVIEW final-pair check: PASS')
print('Post-preflight immutable input hash check: PASS')
print('Classification-only candidate-absence check: PASS')
PY

find /audit-output/evidence -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
tail -n 2 /audit-output/REVIEW.md
