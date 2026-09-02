#!/usr/bin/env bash
set -euo pipefail

required_files=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/canonical.py
)

for path in "${required_files[@]}"; do
  test -f "$path"
  test ! -L "$path"
done
echo "required_regular_non_symlink_files=${#required_files[@]}"

test -d /candidate
test ! -L /candidate
test -d /generation-evidence/codex-trace
test ! -L /generation-evidence/codex-trace
if find /candidate /generation-evidence/codex-trace -type l -print -quit | grep -q .; then
  echo "unexpected_symlink"
  exit 1
fi
echo "candidate_and_trace_symlinks=0"

test ! -e /reference/reference-semantics
echo "generated_mode_reference_semantics=ABSENT"

cmp -s /candidate/prompt.py /reference/prompt.py
echo "candidate_prompt_cmp_trusted=0"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "candidate_translator_cmp_trusted=0"

python3 - <<'PY'
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit["audit_campaign"] == lock
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
print("campaign_block_equals_lock=true")
print("record_layout=legacy-selected-stage1")
print("semantics_mode=GENERATED_SEMANTICS")
PY

sha256sum -c <<'EOF'
ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745  /audit-campaign-lock.json
ba4d0641a184fb3cdd632060a25d6408a7e91fe9d79b5c341407e74b80536327  /candidate/prompt.py
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  /candidate/py2mpy.py
b74f3a3f40b1416f878efb45645d27f822b9d06b04bcd6191329a2229357b82d  /reference/canonical.py
16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24  /run.json
2849005988b10330bdff00910d274aa55561a8b8715c2af71bc1481c5117cdc0  /task.json
5312fec397c251105bae13f869484e3c93c9890aa11f55b1368e919c5218e3a1  /generation-result.json
2bcba06bebf5545f181442e43d762ee53a6b7085e0821e4147c0203b096ce43a  /generation-evidence/invocation.json
7ab90821d3a9a76f5bbe3e844cdaf71a0a09da7aa509e6be8835e2be9f1bf938  /generation-evidence/metrics.json
e5a2df158cf507c489f8817a3b692d2fa9eacf971aa86bfd1ea06edefbb3edf7  /generation-evidence/usage.json
9c4be23b46b5d64f171b6cd7c4f782db78efa5d464fa08c3b2a8d1ce279aac2c  /generation-evidence/codex-last.txt
26e50fe65cabd5f42e28c6cdedb4b285e41156fb2387f40b4afd8c3eea8662bf  /generation-evidence/codex-output.log
4fbd8d83152646045c82c9b1c86a3c0c9bf686de949fcbf8c3eff6755a261d9e  /generation-evidence/prompt.txt
051a853e02f6bf5870f832c367f0fc58eddb0861dc29aa7162d5a2531f7460df  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl
EOF

PYTHONPATH=/opt/humaneval python3 - <<'PY'
from pathlib import Path
from tools.pipeline_contract import sha256_tree

candidate = sha256_tree(Path("/candidate"))
trace = sha256_tree(Path("/generation-evidence/codex-trace"))
print(f"pipeline_tree_candidate={candidate}")
print(f"pipeline_tree_trace={trace}")
assert candidate == "2912ea3c0e4486e103d25d57ade56084b7f5534d35b8782cb3fc9a08c479138b"
assert trace == "f769a846b3cff15293680c9b9e1ea798cb9ee8d2d6141bd15dd8b51e9e68e190"
print("nested_manifest_tree_hashes_match=true")
PY
