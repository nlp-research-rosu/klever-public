# Reviewer command ledger

All commands ran in the container on 2026-07-26. Logs named below include the
exit status and bounded relevant output. Candidate inputs remained read-only;
all K outputs and generated artifacts were created in
`/tmp/audit-work/rebuild`.

## Toolchain and provenance

```bash
command -v kompile kprove krun kast python3
kompile --version
kprove --version
krun --version
python3 --version
```

Log: `00-toolchain.log` (exit 0).

```bash
python3 /audit-output/evidence/provenance_check.py
python3 /audit-output/evidence/extract_generation_trace.py \
  > /audit-output/evidence/01-trace-inspection.log
```

Logs: `01-provenance.log` (exit 0) and `01-trace-inspection.log` (exit 0).

## Scratch copy, trusted regeneration, and differential testing

```bash
mkdir -p /tmp/audit-work/rebuild
cp -a /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/prove.sh /tmp/audit-work/rebuild/
cp -a /reference/prompt.py /reference/canonical.py /reference/py2mpy.py \
  /tmp/audit-work/rebuild/
python3 /reference/py2mpy.py /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
cmp /tmp/audit-work/rebuild/solution.mpy \
  /tmp/audit-work/rebuild/regenerated-solution.mpy
python3 /audit-output/evidence/differential_test.py
```

Logs: `02-translation-identity.log` and `02-differential.log` (all exit 0).

## Fresh builds, positive proof, and concrete execution

Run from `/tmp/audit-work/rebuild`:

```bash
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC
python3 /audit-output/evidence/concrete_semantics_test.py
```

Logs: `03-kompile-concrete.log`, `03-kompile-proof.log`,
`03-kprove-positive.log`, and `03-concrete-semantics.log` (all exit 0).
`03-concrete-semantics-parser-bug.log` preserves the reviewer's first run,
whose K executions exited 0 and printed correct results but whose local regex
was incorrectly double-escaped; the corrected script and rerun are preserved.

## Program pinning and ground witnesses

```bash
python3 /audit-output/evidence/extract_claim_program.py \
  > /tmp/audit-work/rebuild/claimed-program.mpy
kast /tmp/audit-work/rebuild/solution.mpy \
  --definition /tmp/audit-work/rebuild/concrete-kompiled \
  --sort Program --output json \
  > /tmp/audit-work/rebuild/solution.kast.json
kast /tmp/audit-work/rebuild/claimed-program.mpy \
  --definition /tmp/audit-work/rebuild/concrete-kompiled \
  --sort Program --output json \
  > /tmp/audit-work/rebuild/claimed-program.kast.json
cmp /tmp/audit-work/rebuild/solution.kast.json \
  /tmp/audit-work/rebuild/claimed-program.kast.json
python3 /audit-output/evidence/claim_witness.py
```

Logs: `04-program-pinning.log` and `04-ground-witnesses.log` (exit 0).

## Static inventory and body sensitivity

```bash
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
rg -n '^[[:space:]]*(requires|module|imports|syntax|configuration|rule|claim|endmodule)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
rg -n 'function|total|functional|simplification|priority|owise|opaque|macro|alias|hook|concrete' \
  /candidate/*.k
rg -n -C 5 'countAllOccurrences|findString|lengthString' \
  /usr/include/kframework/builtin/domains.md
cp -a /audit-output/evidence/spec-body-mutant.k \
  /tmp/audit-work/rebuild/
kprove spec-body-mutant.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-BODY-MUTANT --dry-run
kprove spec-body-mutant.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-BODY-MUTANT
```

Inventory and dry-run commands exited 0. The final body-mutant `kprove`
intentionally exited 1 with `WarnStuckClaimState`; see
`05-body-mutation-proof.log`.

## Fresh non-vacuity mutation

```bash
cp -a /audit-output/evidence/spec-vacuity.k /tmp/audit-work/rebuild/
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-VACUITY --dry-run
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-VACUITY
```

The dry run exited 0. The proof intentionally exited 1 with
`WarnStuckClaimState`; see `06-vacuity-proof.log`.
