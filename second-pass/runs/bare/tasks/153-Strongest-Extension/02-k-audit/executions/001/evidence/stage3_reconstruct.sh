#!/usr/bin/env bash
set -u

src=/tmp/audit-work/candidate-src
concrete_def=/tmp/audit-work/semantic-kompiled-fresh
proof_def=/tmp/audit-work/verification-kompiled-fresh
status=0

run_checked() {
  echo "$ $*"
  "$@"
  rc=$?
  echo "exit=$rc"
  (( rc == 0 )) || status=1
  return "$rc"
}

echo '$ tool versions'
run_checked kompile --version
run_checked krun --version
run_checked kprove --version

echo '$ fresh LLVM build from semantic.k'
run_checked kompile --backend llvm "$src/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$concrete_def"

echo '$ fresh Haskell proof build from verification.k'
run_checked kompile --backend haskell "$src/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition "$proof_def"

echo '$ structural pin: submitted solution.mpy versus StrongestProgram macro'
left=/tmp/audit-work/submitted.kore
right=/tmp/audit-work/macro.kore
echo "$ kast $src/solution.mpy --definition $proof_def --sort Program --output kore > $left"
kast "$src/solution.mpy" \
  --definition "$proof_def" --sort Program --output kore > "$left"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1
echo "$ kast $src/verification-input.mpy --definition $proof_def --sort Program --output kore > $right"
kast "$src/verification-input.mpy" \
  --definition "$proof_def" --sort Program --output kore > "$right"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1
run_checked cmp -s "$left" "$right"
run_checked sha256sum "$left" "$right"

run_case() {
  label=$1
  class_term=$2
  extension_term=$3
  echo "$ krun solution.mpy case=$label CLASS=$class_term EXTENSIONS=$extension_term"
  krun "$src/solution.mpy" --definition "$concrete_def" \
    -cCLASS="$class_term" -cEXTENSIONS="$extension_term"
  rc=$?
  echo "case=$label exit=$rc"
  (( rc == 0 )) || status=1
}

echo '$ concrete generated-semantics executions: normal and boundaries'
run_case prompt '"Slices"' \
  'strVal("SErviNGSliCes");strVal("Cheese");strVal("StuFfed")'
run_case tie '"my_class"' 'strVal("AA");strVal("Be");strVal("CC")'
run_case singleton-empty '""' 'strVal("")'
run_case punctuation '"C"' 'strVal("a-1");strVal("--");strVal("A!")'
run_case all-negative '"C"' 'strVal("abcd");strVal("a");strVal("xy")'
run_case unicode '"C"' 'strVal("é");strVal("É")'

echo '$ independent CPython outcomes for the same concrete cases'
python3 - <<'PY'
import importlib.util
import json

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension

canonical = load("/reference/canonical.py", "canonical_stage3")
candidate = load("/tmp/audit-work/candidate-src/solution.py", "candidate_stage3")
cases = [
    ("prompt", "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
    ("tie", "my_class", ["AA", "Be", "CC"]),
    ("singleton-empty", "", [""]),
    ("punctuation", "C", ["a-1", "--", "A!"]),
    ("all-negative", "C", ["abcd", "a", "xy"]),
    ("unicode", "C", ["é", "É"]),
]
for label, cls, exts in cases:
    print(json.dumps({
        "case": label,
        "class": cls,
        "extensions": exts,
        "canonical": canonical(cls, exts),
        "candidate": candidate(cls, exts),
    }, ensure_ascii=False))
PY
rc=$?
echo "python_cases_exit=$rc"
(( rc == 0 )) || status=1

echo '$ exact aggregate proof of the submitted spec.k'
kprove "$src/spec.k" --definition "$proof_def" --spec-module SPEC
rc=$?
echo "aggregate_proof_exit=$rc"
(( rc == 0 )) || status=1

echo '$ every positive claim proved independently from label-only copy'
for label in case01 case02 case03 case04 case05 case06 case07; do
  echo "$ kprove spec-labeled.k --claims SPEC-LABELED.$label"
  kprove "$src/spec-labeled.k" --definition "$proof_def" \
    --spec-module SPEC-LABELED --claims "SPEC-LABELED.$label"
  rc=$?
  echo "claim=$label exit=$rc"
  (( rc == 0 )) || status=1
done

echo "stage3_exit=$status"
exit "$status"
