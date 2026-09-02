#!/usr/bin/env bash
set -u
status=0

src=/tmp/audit-work/candidate-src
proof_def=/tmp/audit-work/verification-kompiled-fresh

echo '$ local declaration/rule extraction'
rg -n '^\s*(configuration|syntax|rule|claim)\b|\[(function|total|functional|macro|simplification|priority|owise|anywhere)' \
  "$src/semantic.k" "$src/verification.k" "$src/spec.k"
rc=$?
echo "inventory_extract_exit=$rc"
(( rc == 0 )) || status=1

echo '$ K false-conclusion witness U1: prove ASCII-only uppercase result'
kprove "$src/spec-unsound-witness.k" --definition "$proof_def" \
  --spec-module SPEC-UNSOUND-WITNESS \
  --claims SPEC-UNSOUND-WITNESS.unicode-upper
rc=$?
echo "kprove_U1_exit=$rc"
(( rc == 0 )) || status=1

echo '$ K false-conclusion witness U2: prove ASCII-only lowercase result'
kprove "$src/spec-unsound-witness.k" --definition "$proof_def" \
  --spec-module SPEC-UNSOUND-WITNESS \
  --claims SPEC-UNSOUND-WITNESS.unicode-lower
rc=$?
echo "kprove_U2_exit=$rc"
(( rc == 0 )) || status=1

echo '$ Python ground truth for U1 and U2'
python3 - <<'PY'
import importlib.util
import json

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension

canonical = load("/reference/canonical.py", "canonical_unsound_witness")
candidate = load("/tmp/audit-work/candidate-src/solution.py", "candidate_unsound_witness")
for label, extensions, k_claimed in [
    ("U1", ["--", "É"], "C.--"),
    ("U2", ["é", "--"], "C.é"),
]:
    print(json.dumps({
        "witness": label,
        "input": ["C", extensions],
        "K_proved_result": k_claimed,
        "canonical_result": canonical("C", extensions),
        "candidate_python_result": candidate("C", extensions),
        "K_result_is_false_of_real_program": (
            k_claimed != canonical("C", extensions)
            and canonical("C", extensions) == candidate("C", extensions)
        ),
    }, ensure_ascii=False))
PY
rc=$?
echo "python_witness_exit=$rc"
(( rc == 0 )) || status=1

echo "stage5_exit=$status"
exit "$status"
