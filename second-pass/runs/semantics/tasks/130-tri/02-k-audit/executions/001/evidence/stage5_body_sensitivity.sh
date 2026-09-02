#!/usr/bin/env bash
set -u
set -o pipefail

mut_dir=/tmp/audit-work/body-mutation
echo '$ test ! -e /tmp/audit-work/body-mutation'
test ! -e "$mut_dir"
fresh_rc=$?
echo "exit=$fresh_rc"
if [ "$fresh_rc" -ne 0 ]; then
  exit 1
fi

echo '$ mkdir -p /tmp/audit-work/body-mutation/reference-semantics'
mkdir -p "$mut_dir/reference-semantics"
echo "exit=$?"
echo '$ cp -a /reference/reference-semantics/. /tmp/audit-work/body-mutation/reference-semantics/'
cp -a /reference/reference-semantics/. "$mut_dir/reference-semantics/"
echo "exit=$?"
echo '$ cp /candidate/spec.k /tmp/audit-work/body-mutation/spec.k'
cp /candidate/spec.k "$mut_dir/spec.k"
echo "exit=$?"

echo '$ python3 /audit-output/evidence/make_body_mutation.py | tee /tmp/audit-work/body-mutation/verification.k /audit-output/evidence/verification-body-mutated.k >/dev/null'
python3 /audit-output/evidence/make_body_mutation.py \
  | tee "$mut_dir/verification.k" \
        /audit-output/evidence/verification-body-mutated.k >/dev/null
generate_rc=${PIPESTATUS[0]}
echo "exit=$generate_rc"

cd "$mut_dir" || exit 90
echo '$ diff -u /candidate/verification.k verification.k'
diff -u /candidate/verification.k verification.k
diff_rc=$?
echo "exit=$diff_rc (expected 1 for a textual mutation)"

echo '$ kompile verification.k --backend haskell --main-module TRI-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
build_rc=$?
echo "exit=$build_rc"

if [ "$build_rc" -eq 0 ]; then
  for module in TRI-LOOP-SPEC TRI-CORRECT-SPEC; do
    echo "\$ kprove spec.k --definition verification-kompiled --spec-module $module --output pretty"
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module "$module" \
      --output pretty
    echo "module=$module exit=$?"
  done
fi

# Mutation proof failures are expected sensitivity evidence. The wrapper only
# fails if mutation generation or compilation failed.
if [ "$generate_rc" -ne 0 ] || [ "$build_rc" -ne 0 ]; then
  exit 1
fi
exit 0
