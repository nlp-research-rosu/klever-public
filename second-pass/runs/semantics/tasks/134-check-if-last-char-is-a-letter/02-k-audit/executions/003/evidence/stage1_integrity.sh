#!/usr/bin/env bash
set -euo pipefail
set -x

required_records=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/usage.json
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T06-30-11-019f8ebd-805f-71e1-ba58-cb3a4a52cb13.jsonl
)

for artifact in "${required_records[@]}"; do
  test -f "$artifact"
  test ! -L "$artifact"
  test -r "$artifact"
done

python3 - <<'PY'
import json
from pathlib import Path

audit_input = json.loads(Path("/audit-input.json").read_text())
campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["audit_campaign"] == campaign_lock
print("campaign block structural match: yes")
PY

test "$(sha256sum /audit-campaign-lock.json | cut -d ' ' -f 1)" = \
  ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745
test "$(sha256sum /reference/canonical.py | cut -d ' ' -f 1)" = \
  d70c2571220d5f6310e7f79f8e30fd875affb5b4ac70f749173a5a4b0fe7f21b
test "$(sha256sum /reference/prompt.py | cut -d ' ' -f 1)" = \
  4a14cb9f380c3fda4feb1325fdc1d1562888d52852c3cdd327f1eaeaff4d22df
test "$(sha256sum /reference/py2mpy.py | cut -d ' ' -f 1)" = \
  406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
test "$(sha256sum /generation-evidence/codex-last.txt | cut -d ' ' -f 1)" = \
  1503d052a9783a857223db5cff0d19fb7510cff426d553ef7c051ae298a2e806
test "$(sha256sum /generation-evidence/codex-output.log | cut -d ' ' -f 1)" = \
  6314ebf6e534bbe06bad012c4148b1e344622832b9716d831591f3b197343e95
test "$(sha256sum /generation-evidence/prompt.txt | cut -d ' ' -f 1)" = \
  3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09
test "$(sha256sum /generation-evidence/metrics.json | cut -d ' ' -f 1)" = \
  b4023f82d518d81187aaa398e61bd6e2eb6366ab9a0e5150da168cf59558bd12
test "$(sha256sum /generation-evidence/usage.json | cut -d ' ' -f 1)" = \
  3cb7f6c5b1f78245772f5d15be98a2df8be0f22359de120d8e48064eac087f58
test "$(sha256sum /generation-evidence/invocation.json | cut -d ' ' -f 1)" = \
  c82958219d0c2702981f25162de5979149c1ed7842a9d8abf9f97a688fed562a
test "$(sha256sum /run.json | cut -d ' ' -f 1)" = \
  321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0
test "$(sha256sum /task.json | cut -d ' ' -f 1)" = \
  093de584b5e0ecf60bf4c1e16cb754a9515f8d1293315610cd5bff0402821e78
test "$(sha256sum /generation-result.json | cut -d ' ' -f 1)" = \
  e3c5138d935a0a0a2a628baece34e89c12e017ffb997b62d5f85343cd113c153
test "$(sha256sum /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T06-30-11-019f8ebd-805f-71e1-ba58-cb3a4a52cb13.jsonl | cut -d ' ' -f 1)" = \
  50efe90d45843b81a3a5a86523f0168df94d5eb5b7a1005711dbc61b91fda4f3

test -d /reference/reference-semantics
test -d /candidate/reference-semantics
test -z "$(find /candidate /reference /generation-evidence -type l -print -quit)"
cmp /candidate/prompt.py /reference/prompt.py
cmp /candidate/py2mpy.py /reference/py2mpy.py
diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics

find /candidate -type f -printf '%P\n' | sort |
  while IFS= read -r relative_path; do
    sha256sum "/candidate/$relative_path"
  done

echo "STAGE1_INTEGRITY_OK"
