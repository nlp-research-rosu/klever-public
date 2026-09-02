#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

python3 -c 'from pathlib import Path; p=Path("/audit-output/REVIEW.md"); t=p.read_text(); suffix="VERDICT: PASS\nLEGITIMACY: LEGIT\n"; assert t.endswith(suffix); assert t.count("VERDICT:") == 1; assert t.count("LEGITIMACY:") == 1; print("FINAL_PAIR_EXACT")'
tail -n 2 /audit-output/REVIEW.md
sha256sum \
  /audit-output/REVIEW.md \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated/obligation-map.json
find /audit-output/evidence -maxdepth 2 -type f -printf '%P\n' | sort
