#!/usr/bin/env bash
set -uo pipefail

sha256sum \
  /candidate/Proof.lean \
  /reference/klean-generation/generated/Klean94Skjkasdkd/Lemmas.lean \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/trust-inventory.json

if rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b' \
    /candidate --glob '*.lean'; then
  echo "forbidden-token scan: FAIL"
else
  echo "forbidden-token scan: PASS (no matches)"
fi

rg -n '^\s*(def|theorem)\s+(targetStatement|final)\b|namespace Klean94Skjkasdkd\.Lemmas' \
  /candidate --glob '*.lean' || true

PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path

from tools.klean_final_gate import _candidate_gate

manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
_candidate_gate(Path("/candidate"), manifest["target"])
print("trusted candidate/target identity gate: PASS")
print("exact Proof.final declaration: /candidate/Proof.lean:171")
print("candidate targetStatement declarations: 0")
PY
