#!/usr/bin/env bash
set -uo pipefail

scratch_path=$(sed -n '1p' /audit-output/evidence/scratch-path.txt)
log_path=/audit-output/evidence/03_reconstruction.log
exec >"$log_path" 2>&1

run_bounded() {
    local label=$1
    shift
    local raw_path="$scratch_path/reviewer-${label}.raw.log"
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@" >"$raw_path" 2>&1
    local status=$?
    printf '[exit %d]\n' "$status"
    printf '[raw output: %s; ' "$raw_path"
    wc -c <"$raw_path" | tr -d '\n'
    printf ' bytes; '
    wc -l <"$raw_path" | tr -d '\n'
    printf ' lines]\n'
    sed -n '1,160p' "$raw_path"
    local line_count
    line_count=$(wc -l <"$raw_path")
    if [ "$line_count" -gt 320 ]; then
        printf '[... middle omitted from bounded evidence ...]\n'
        tail -n 160 "$raw_path"
    elif [ "$line_count" -gt 160 ]; then
        sed -n '161,320p' "$raw_path"
    fi
    return 0
}

printf 'Clean reconstruction (UTC): '
date -u +%Y-%m-%dT%H:%M:%SZ
printf 'Scratch: %s\n' "$scratch_path"
printf 'Candidate-provided compiled trees were not copied.\n'

printf '\n$ cd %q\n' "$scratch_path"
cd "$scratch_path" || exit 2
printf '[exit 0]\n'

run_bounded tool-versions kompile --version
run_bounded proof-tool-version kprove --version
run_bounded prebuild-tree find . -maxdepth 1 -type d -printf '%f\n'

printf '\n$ cp -a /audit-output/evidence/03_concrete_review.py ./reviewer-concrete.py\n'
cp -a /audit-output/evidence/03_concrete_review.py ./reviewer-concrete.py
printf '[exit %d]\n' "$?"

printf '\n$ python3 py2mpy.py reviewer-concrete.py > reviewer-concrete.mpy\n'
python3 py2mpy.py reviewer-concrete.py >reviewer-concrete.mpy
printf '[exit %d]\n' "$?"

run_bounded llvm-kompile \
    kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition reviewer-runtime-kompiled

run_bounded concrete-krun \
    krun reviewer-concrete.mpy \
    --definition reviewer-runtime-kompiled \
    --output none

run_bounded haskell-kompile \
    kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition reviewer-verification-kompiled

run_bounded proof-one \
    kprove spec.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.starts-one-ends-one-digit

run_bounded proof-multi \
    kprove spec.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.starts-one-ends-multi-digit

run_bounded proof-all \
    kprove spec.k \
    --definition reviewer-verification-kompiled \
    --spec-module SPEC

run_bounded postbuild-tree find . -maxdepth 1 -type d -printf '%f\n'

printf '\nResult summary extracted from bounded raw logs:\n'
for label in proof-one proof-multi proof-all; do
    raw_path="$scratch_path/reviewer-${label}.raw.log"
    top_count=$(grep -c '^#Top$' "$raw_path" || true)
    printf '%s: exact-#Top-lines=%s\n' "$label" "$top_count"
done

printf '\nScript exit: 0 (individual command statuses above)\n'
