# Reviewer command ledger

All build and proof commands ran in `/tmp/audit-work/reconstruction`; source
inputs were copied from the trusted mounts and the candidate's source files.
No candidate-provided compiled definition or cache was copied or used.
Transcript logs include `COMMAND_EXIT_CODE`.

## Provenance and fidelity

```bash
python3 /audit-output/evidence/provenance_check.py
```

Exit 0. Full output: `01-provenance.log`.

```bash
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
sha256sum regenerated-solution.mpy solution.mpy
```

Exit 0; both SHA-256 values are
`0b6ee658c0a0596c2ff21804180dddb99aff49f6094f4577f7c8dc82b42e6669`.
Full output: `02-translation.log`.

```bash
python3 /audit-output/evidence/differential_test.py \
  --subject /tmp/audit-work/reconstruction/solution.py
```

Exit 0; 20,742 cases, zero mismatches, zero mutations, zero example
failures. Full output: `02-differential.log`.

## Fresh definitions and positive claims

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. Full output: `03-runtime-build.log`.

```bash
python3 concrete_cases.py
python3 py2mpy.py concrete_cases.py > concrete_cases.mpy
krun concrete_cases.mpy --definition runtime-kompiled
```

Exit 0; final `<k>` is `.K`, `<exc>` is `NoExc`, and `<exit-code>` is 0.
Full output: `03-concrete-execution.log`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0. Full output: `03-proof-build.log`.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

Exit 0; output `#Top`. Full output: `03-kprove-loop.log`.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant
```

Exit 0; output `#Top`. This loads all three claims, treats only the separately
proved loop claim as the lemma, and proves both untrusted entry claims. Full
output: `03-kprove-entries.log`.

An exploratory command that combined
`--claims SPEC.sum-squares --trusted SPEC.loop-invariant` excluded the lemma
from the selected claim set and expanded the loop. The reviewer interrupted
that diagnostic with exit 130 after establishing the selection error. No
transcript was produced before SIGINT; this ledger preserves the exact command
and status. It is not a candidate proof attempt. The exact composition command
above then closed promptly.

## Pinning, adequacy, and extension checks

```bash
kast regenerated-solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > submitted-program-term.kore
kast \
  --expression 'Module(sumSquaresDef)' \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > claimed-program-term.kore
cmp -s submitted-program-term.kore claimed-program-term.kore
```

Exit 0; both terms have SHA-256
`0e3756c7b1b48e1fe936ba874b3dbddd7086db6afe43214f0354fd649af9d95b`.
Full output: `04-program-pinning.log`.

```bash
kprove ground-summary.k \
  --definition verification-kompiled \
  --spec-module GROUND-SUMMARY
```

Exit 0; output `#Top`. Ground prompt and common-multiple summaries reduce to
6, 0, -126, and 4. Full output: `04-ground-summary-config.log`.

The preceding exploratory attempt used bare functional claims. This backend
reported that functional claims are unsupported and exited 113; the reviewer
re-expressed the same equalities as ordinary configuration reachability claims.
That tool-interface diagnostic is preserved in `04-ground-summary.log`.

```bash
krun concrete_cases.mpy --definition runtime-kompiled \
  --color off > fixed-concrete.out
krun concrete_cases.mpy --definition verification-kompiled \
  --color off > extended-concrete.out
cmp -s fixed-concrete.out extended-concrete.out
```

Exit 0; outputs are byte-identical with SHA-256
`8584b20bb68c21cc84a2dc1562e0ac70b0cf753cb5671092db1a19a205c29e4c`.
Full output: `05-fixed-vs-extended.log`.

```bash
kprove projection-opposite.k \
  --definition verification-kompiled \
  --spec-module PROJECTION-OPPOSITE
```

Actual exit 1 as expected; `WarnStuckClaimState` shows actual value 2 against
the false destination 3. Full output: `05-projection-opposite.log`.

```bash
kprove body-sensitivity.k \
  --definition verification-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY
```

Actual exit 1 as expected; `WarnStuckClaimState` shows that the materially
changed executed body returns 2 against the original result 0. Full output:
`04-body-sensitivity.log`.

## Exhaustive inventory and fresh non-vacuity

```bash
python3 /audit-output/evidence/k_inventory.py \
  > /audit-output/evidence/05-k-inventory.md
python3 /audit-output/evidence/k_disposition.py \
  > /audit-output/evidence/05-k-dispositions.csv
```

Both exit 0. The inventory contains all 1,250 top-level records before omitting
only 27 `endmodule` table rows: 235 syntax declarations, one configuration,
five contexts, 714 rules, three claims, and all module/import/require records.

```bash
kprove fresh-vacuity.k \
  --definition verification-kompiled \
  --spec-module AUDIT-FRESH-VACUITY
```

Actual exit 1 as expected; the artifact builds and reaches
`WarnStuckClaimState` with actual result 44 against the false result 45.
Full output: `06-fresh-vacuity.log`.
