#!/usr/bin/env bash
set -uo pipefail

log_path=/audit-output/evidence/02_program_fidelity.log
scratch_record=/audit-output/evidence/scratch-path.txt
exec >"$log_path" 2>&1

run() {
    printf '\n$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf '[exit %d]\n' "$status"
    return "$status"
}

scratch_path=$(mktemp -d /tmp/audit-work/83-audit.XXXXXX)
printf '%s\n' "$scratch_path" >"$scratch_record"
printf 'Fresh scratch directory: %s\n' "$scratch_path"

run mkdir -p "$scratch_path/reference-semantics"
run cp -a /reference/reference-semantics/. "$scratch_path/reference-semantics/"
run cp -a /reference/py2mpy.py "$scratch_path/py2mpy.py"
run cp -a /reference/canonical.py "$scratch_path/trusted-canonical.py"
run cp -a /reference/prompt.py "$scratch_path/trusted-prompt.py"
run cp -a /candidate/prompt.py "$scratch_path/candidate-prompt.py"
run cp -a /candidate/py2mpy.py "$scratch_path/candidate-py2mpy.py"

candidate_sources=(
    solution.py
    solution.mpy
    verification.k
    spec.k
    prove.sh
    PROOF.md
    spec-vacuity.k
    spec-body-mutation.k
    concrete-tests.py
    concrete-tests.mpy
    validate.py
)
for rel in "${candidate_sources[@]}"; do
    run cp -a "/candidate/$rel" "$scratch_path/$rel"
done

printf '\n$ cd %q\n' "$scratch_path"
cd "$scratch_path" || exit 2
printf '[exit 0]\n'

printf '\n$ python3 py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 py2mpy.py solution.py >solution.regenerated.mpy
translate_status=$?
printf '[exit %d]\n' "$translate_status"

run cmp -s solution.regenerated.mpy solution.mpy
run sha256sum solution.py solution.mpy solution.regenerated.mpy
run diff -u solution.mpy solution.regenerated.mpy
run python3 /audit-output/evidence/02_differential.py \
    "$scratch_path/trusted-canonical.py" \
    "$scratch_path/solution.py"

run find "$scratch_path" \
    -path "$scratch_path/reference-semantics" -prune -o \
    -printf '%y %P -> %l\n'

printf '\nScript exit: 0 (individual command statuses above)\n'
