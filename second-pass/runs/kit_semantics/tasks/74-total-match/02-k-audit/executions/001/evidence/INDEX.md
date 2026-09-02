# Auditor evidence index

All commands were run from `/tmp/audit-work/74-total-match` through
`run_logged.sh` unless the log says otherwise. Each completed log records the
working directory, shell-escaped command, output, and exit status.

| Evidence | Purpose | Result |
|---|---|---|
| `01-integrity.log`, `integrity_check.py` | Provenance, hashes, record completeness, tree comparison | exit 0 |
| `02-translation.log` | Trusted source-to-MPY regeneration and byte comparison | exit 0 |
| `03-differential.log`, `differential_test.py` | Canonical/generated Python differential testing | 26,351 cases, 0 mismatches, exit 0 |
| `04-python-syntax.log` | Independent Python syntax compilation | exit 0 |
| `05-kompile-llvm.log` | Fresh concrete-definition build | exit 0 |
| `06-krun-module.log` | Concrete execution of submitted MPY module | exit 0, final `.K` |
| `07-kompile-haskell.log` | Fresh proof-definition build | exit 0 |
| `08-kprove-sum-loop.log` | Loop-summary claim | `#Top`, exit 0 |
| `09b-kprove-entry-first-with-loop.log` | First-result entry claim with its loop circularity | `#Top`, exit 0 |
| `10b-kprove-entry-second-with-loop.log` | Second-result entry claim with its loop circularity | `#Top`, exit 0 |
| `11-kprove-all.log` | Complete unfiltered specification | `#Top`, exit 0 |
| `12-translate-ground-witness.log`, `13-krun-ground-witness.log`, `k_ground_witness.py` | Concrete satisfying witnesses | exit 0 |
| `14-constructor-compare.log`, `constructor_compare.py` | Constructor-level source/program/claim comparison | all equal, exit 0 |
| `15-rule-inventory.log`, `rule_inventory.py`, `rule-inventory.md` | Exhaustive K declaration/rule inventory | 945 items, exit 0 |
| `16-vacuity-dry-run.log`, `17-vacuity-proof.log`, `audit-vacuity.k` | Auditor-authored false-result mutation | builds; proof stuck as expected, exit 1 |
| `18-body-mutation-inspection.log`, `19-body-mutation-dry-run.log`, `20-body-mutation-proof.log` | Executed-body sensitivity mutation | builds; proof stuck on false result, exit 1 |

`09-kprove-entry-first.log` and `10-kprove-entry-second.log` are abandoned
diagnostic selections that named an entry claim without naming the loop
circularity it depends upon; they are not used as proof evidence. The corrected
bounded runs are `09b`, `10b`, and the complete run is `11`.
