# Audit command index

All commands ran on 2026-07-26 in the mounted audit container.  The associated
typescript logs record `COMMAND_EXIT_CODE`; command output is bounded.

## Provenance and source preparation

```bash
python3 /audit-output/evidence/stage1_integrity.py
python3 /audit-output/evidence/pipeline_tree_hash.py
python3 /audit-output/evidence/generation_trace_summary.py
```

All exited 0 in `stage1_integrity.log`, `pipeline_tree_hash.log`, and
`generation_trace_summary.log`.  `stage1_integrity_attempt1.log` preserves a
reviewer-script error (exit 1) fixed before the successful run.

The scratch copy was made with:

```bash
mkdir -p /tmp/audit-work/120-maximum/candidate /tmp/audit-work/120-maximum/reference
cp -a /candidate/prompt.py /candidate/prove.sh /candidate/py2mpy.py \
  /candidate/semantic.k /candidate/solution.mpy /candidate/solution.py \
  /candidate/spec.k /candidate/verification.k \
  /tmp/audit-work/120-maximum/candidate/
cp -a /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  /tmp/audit-work/120-maximum/reference/
```

The exact file listing and post-copy hashes are in `scratch_copy.log` (exit 0).

## Fidelity and differential checks

```bash
python3 /tmp/audit-work/120-maximum/reference/py2mpy.py \
  /tmp/audit-work/120-maximum/candidate/solution.py \
  > /tmp/audit-work/120-maximum/solution.regenerated.mpy
cmp -s /tmp/audit-work/120-maximum/solution.regenerated.mpy \
  /tmp/audit-work/120-maximum/candidate/solution.mpy
python3 /audit-output/evidence/differential_test.py
python3 /audit-output/evidence/program_pinning.py
python3 /audit-output/evidence/claim_witness.py
```

All exited 0.  See `translator_regeneration.log`, `differential_test.log`,
`program_pinning.log`, and `claim_witness.log`.

## Toolchain and clean builds

Working directory for these commands was
`/tmp/audit-work/120-maximum/candidate`.

```bash
export PATH="/home/agent/.nix-profile/bin:$PATH"
kompile --version
krun --version
kprove --version

kompile --backend llvm semantic.k \
  --main-module MAXIMUM \
  --syntax-module MAXIMUM-SYNTAX \
  --output-definition concrete-kompiled

kompile --backend haskell verification.k \
  --main-module MAXIMUM-VERIFICATION \
  --syntax-module MAXIMUM-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAXIMUM-SPEC
```

All exited 0.  The positive proof printed `#Top`.  See `tool_versions.log`,
`kompile_concrete.log`, `kompile_proof.log`, and `kprove_positive.log`.

## Concrete generated-semantics checks

```bash
python3 /audit-output/evidence/semantic_differential.py

kompile --backend llvm /audit-output/evidence/length_boundary_harness.k \
  --main-module LENGTH-BOUNDARY-HARNESS \
  --syntax-module LENGTH-BOUNDARY-HARNESS \
  -I /tmp/audit-work/120-maximum/candidate \
  --output-definition boundary-harness-kompiled

python3 /audit-output/evidence/run_length_boundary.py
```

All exited 0.  The first script records every internal `krun` command and
result in `semantic_differential.log`; the harness build and run are in
`kompile_length_boundary.log` and `run_length_boundary.log`.

One direct `-cARGS` parse of a 1,000-element varied list was killed with exit
137 in `semantic_differential_attempt1.log`.  It produced a K argument-parser
failure before semantic execution.  The preserved
`semantic_differential_attempt1.py` reproduces it.  A first harness build used
the wrong syntax module (build exit 0, subsequent parse exit 113); those logs
are `kompile_length_boundary_attempt1.log` and
`run_length_boundary_attempt1.log`.  The corrected compact harness executes
the same candidate body on 1,000 zeros and exits 0.

## Static inventory and sensitivity tests

```bash
nl -ba semantic.k
nl -ba verification.k
nl -ba spec.k
rg -n '\[(function|total|functional|simplification|concrete|priority|owise)|^\s*(syntax|rule|claim|configuration|imports|requires)' \
  semantic.k verification.k spec.k
```

The output and exit 0 are in `source_inventory.log`.

Body mutation:

```bash
kprove /audit-output/evidence/spec-body-mutation.k -I . \
  --definition verification-kompiled \
  --spec-module MAXIMUM-BODY-MUTATION \
  --dry-run > /dev/null

kprove /audit-output/evidence/spec-body-mutation.k -I . \
  --definition verification-kompiled \
  --spec-module MAXIMUM-BODY-MUTATION
```

The dry run exited 0; proof exited 1 with `WarnStuckClaimState`.  See
`body_mutation_dry_run.log` and `body_mutation_proof.log`.

Fresh false-postcondition mutation:

```bash
kprove /audit-output/evidence/spec-vacuity-fresh.k -I . \
  --definition verification-kompiled \
  --spec-module MAXIMUM-SPEC-VACUITY-FRESH \
  --dry-run > /dev/null

kprove /audit-output/evidence/spec-vacuity-fresh.k -I . \
  --definition verification-kompiled \
  --spec-module MAXIMUM-SPEC-VACUITY-FRESH
```

The dry run exited 0; proof exited 1 with the expected unmet equality between
`.List` and `dropInts(size(L) -Int K, sortInts(L))`.  See
`vacuity_dry_run.log` and `vacuity_proof.log`.
