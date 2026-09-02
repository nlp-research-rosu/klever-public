#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/162-string-to-md5

echo 'COMMAND: bash /audit-output/evidence/stage2_fidelity.sh'
echo "SCRATCH=$scratch"
if [[ -e "$scratch" ]]; then
  echo "ERROR: scratch path already exists; refusing to merge with prior artifacts" >&2
  exit 2
fi
mkdir -p "$scratch"

cp --no-dereference \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/spec-vacuity.k \
  /candidate/spec-body-mutation.k \
  /candidate/smoke.py \
  /candidate/smoke.mpy \
  /candidate/smoke-empty.py \
  /candidate/smoke-empty.mpy \
  "$scratch/"
cp --no-dereference /reference/prompt.py "$scratch/trusted-prompt.py"
cp --no-dereference /reference/canonical.py "$scratch/trusted-canonical.py"
cp --no-dereference /reference/py2mpy.py "$scratch/trusted-py2mpy.py"
cp -a --no-dereference /reference/reference-semantics "$scratch/reference-semantics"

echo
echo '== Trusted regeneration =='
echo 'COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/162-string-to-md5/regenerated-solution.mpy'
python3 /reference/py2mpy.py /candidate/solution.py > "$scratch/regenerated-solution.mpy"
translate_rc=$?
echo "TRANSLATOR_EXIT=$translate_rc"
sha256sum /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
set +e
cmp /candidate/solution.mpy "$scratch/regenerated-solution.mpy"
cmp_rc=$?
set -e
echo "TRANSLATION_BYTE_CMP_EXIT=$cmp_rc"
if [[ "$cmp_rc" -ne 0 ]]; then
  diff -u /candidate/solution.mpy "$scratch/regenerated-solution.mpy" || true
  exit 1
fi

echo
echo '== Python syntax and documented example =='
echo 'COMMAND: python3 -m py_compile /tmp/audit-work/162-string-to-md5/solution.py'
python3 -m py_compile "$scratch/solution.py"
echo "PY_COMPILE_EXIT=$?"
echo 'COMMAND: python3 -c (load solution and evaluate empty/example)'
python3 - "$scratch/solution.py" <<'PY'
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("scratch_solution", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print("empty=" + repr(module.string_to_md5("")))
print("example=" + module.string_to_md5("Hello world"))
PY
echo "PY_EXAMPLE_EXIT=$?"

echo
echo '== Independent differential =='
python3 /audit-output/evidence/stage2_differential.py
echo "DIFFERENTIAL_EXIT=$?"
