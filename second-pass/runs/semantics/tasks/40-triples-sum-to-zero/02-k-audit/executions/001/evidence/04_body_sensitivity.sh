#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/forty-triples-audit
mutant="$scratch/body-sensitivity"

test ! -e "$mutant"
mkdir -p "$mutant"
cp -a "$scratch/candidate-src/reference-semantics" "$mutant/"
cp -a "$scratch/candidate-src/verification.k" "$scratch/candidate-src/spec.k" "$mutant/"
cp -a /audit-output/evidence/mutated_solution.py "$mutant/solution.py"
python3 "$scratch/trusted/py2mpy.py" "$mutant/solution.py" > "$mutant/solution.mpy"

python3 -c 'import importlib.util; p="/tmp/audit-work/forty-triples-audit/body-sensitivity/solution.py"; s=importlib.util.spec_from_file_location("mutant",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); assert m.triples_sum_to_zero([0,0,0]) is False; print("MUTANT_WITNESS [0,0,0] -> False")'

rg -n 'requires|solution[.]mpy|solution[.]py|#runTriples|closureVal' \
  "$mutant/verification.k" "$mutant/spec.k"

cd "$mutant" || exit 1
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$mutant/verification-kompiled"
build_status=$?
echo "MUTANT_PROOF_BUILD_EXIT_STATUS $build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

kprove spec.k \
  --definition "$mutant/verification-kompiled" \
  --spec-module SPEC \
  --claims length-three \
  --output pretty
