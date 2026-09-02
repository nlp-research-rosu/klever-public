# Audit command record

All candidate and trusted mounts were treated as read-only.  Build commands ran
from `/tmp/audit-work/129-minPath-audit`; inventory and reporting commands ran
from `/audit-output`.  Terminal transcripts named below contain the bounded
stdout/stderr and their `COMMAND_EXIT_CODE` footer.  K was v7.1.293 and Python
was 3.10.12.

## Stage 1

```bash
script -q -e -c 'python3 /audit-output/evidence/integrity_check.py' /audit-output/evidence/stage1-integrity-v3.log
script -q -e -c 'python3 /audit-output/evidence/trace_inventory.py' /audit-output/evidence/stage1-trace-inventory.log
diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
```

All three exited 0.  `stage1-integrity-v3.log` is the authoritative integrity run.
The earlier `stage1-integrity.log` and `stage1-integrity-v2.log` are preserved
exploratory versions; v2 intentionally exposed that launcher seal hashes and
pipeline-contract tree hashes are differently encoded and then stopped on a
misnamed key.  No audit conclusion relies on either superseded run.

## Stage 2

```bash
cd /tmp/audit-work/129-minPath-audit
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
sha256sum solution.mpy solution.regenerated.mpy
script -q -e -c 'python3 /audit-output/evidence/differential.py' /audit-output/evidence/stage2-differential.log
```

Translation, comparison, hashing, and the differential all exited 0.  The
translation transcript is `stage2-translation.log`.

## Stage 3

```bash
cd /tmp/audit-work/129-minPath-audit
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -o verification-audit-kompiled
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.inner-one-ahead,SPEC.inner-no-one,SPEC.outer-one-ahead,SPEC.outer-one-past,SPEC.scan-finish --depth 240
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.neighbor-finish --depth 400
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.result-loop-tail --depth 110
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail,SPEC.minpath-full-contract --trusted SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail --depth 240
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX -o runtime-audit-kompiled
krun smoke_odd.mpy --definition runtime-audit-kompiled
krun smoke_even.mpy --definition runtime-audit-kompiled
```

The Haskell compile exited 0.  The scan group, neighbor claim, and result-loop
claim each exited 0 and printed `#Top`.  The composed target exited 1 with a
stuck implication and did not print `#Top`.  The LLVM compile and both concrete
runs exited 0.  The corresponding transcripts are the `stage3-*` logs.

## Stage 4

```bash
cd /tmp/audit-work/129-minPath-audit
kast solution.mpy --definition verification-audit-kompiled --module MPY-SYNTAX --output json > solution-module.json
kast --definition verification-audit-kompiled --module VERIFICATION --sort Stmts --expression minPathBody --expand-macros --output json > minpath-body.json
script -q -e -c 'python3 /audit-output/evidence/pinning_check.py' /audit-output/evidence/stage4-pinning.log
script -q -e -c 'python3 /audit-output/evidence/adequacy_witness.py' /audit-output/evidence/stage4-witnesses.log
```

All exited 0.

## Stage 5

```bash
script -q -e -c 'python3 /audit-output/evidence/rule_inventory.py' /audit-output/evidence/stage5-rule-inventory-v3.log
script -q -e -c '/audit-output/evidence/program_rule_map.sh' /audit-output/evidence/stage5-program-rule-map.log
```

Both exited 0.  `stage5-rule-inventory-v3.log` is authoritative; v1 and v2
are preserved earlier inventories superseded by the per-file summary in v3.

## Stage 6

The reviewer-created mutation was copied to the scratch tree as
`spec-vacuity.k`, then these exact commands were run:

```bash
cd /tmp/audit-work/129-minPath-audit
kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result-loop-tail --depth 110 --dry-run
kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result-loop-tail --depth 110
```

The dry run exited 0.  The proof run exited 1 after reaching the changed
result obligation; it did not fail to parse or import.
