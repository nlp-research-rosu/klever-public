# Reviewer command ledger

All commands below were run from `/tmp/audit-work/proof` with
`PATH=/home/agent/.nix-profile/bin:$PATH`. The corresponding bounded terminal
transcripts are the named files in this directory.

| Operation | Exact command | Exit | Transcript |
|---|---|---:|---|
| Trusted translation | `python3 py2mpy.py solution.py > regenerated-solution.mpy && cmp -s solution.mpy regenerated-solution.mpy` | 0 | `02-regeneration.log` |
| Differential test | `python3 /audit-output/evidence/differential_test.py` | 0 | `02-differential-results.log` |
| LLVM definition | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-fresh` | 0 | `03-kompile-runtime.log` |
| Proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled-fresh` | 0 | `03-kompile-verification.log` |
| Fixed-semantics lemma definition | `kompile --backend haskell reference-semantics/semantics.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition lemma-kompiled-fresh` | 0 | `03-kompile-lemma.log` |
| Simplification lemma | `kprove lemma-spec.k --definition lemma-kompiled-fresh --spec-module LEMMA-SPEC` | 0, `#Top` | `03-kprove-lemma.log` |
| ASCII concrete suite | `krun concrete_checks_ascii.mpy --definition runtime-kompiled-fresh` | 0 | `03-concrete-krun-ascii.log` |
| Unicode source-literal probe | `krun concrete_checks.mpy --definition runtime-kompiled-fresh` | 113, expected decoder limitation | `03-concrete-krun.log` |
| Expanded submitted module | `kast solution.mpy --definition verification-kompiled-fresh --module VERIFICATION --sort Module --expand-macros --output kore > solution-expanded.kore` | 0 | `04-program-term-identity.log` |
| Expanded claim module | `kast proof-program.mpy --definition verification-kompiled-fresh --module VERIFICATION --sort Module --expand-macros --output kore > proof-program-expanded.kore` | 0 | `04-program-term-identity.log` |
| Program-term comparison | `cmp solution-expanded.kore proof-program-expanded.kore` | 0 | `04-program-term-identity.log` |
| Body-mutation definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled-body-mutation` (from `/tmp/audit-work/body-mutation`) | 0 | `04-body-mutation-kompile.log` |
| Body-mutation proof | `kprove spec.k --definition verification-kompiled-body-mutation --spec-module SPEC --claims SPEC.valid-name-txt` (from `/tmp/audit-work/body-mutation`) | 1, expected stuck claim | `04-body-mutation-kprove.log` |
| False-result parse/build | `kprove reviewer-vacuity.k --definition verification-kompiled-fresh --spec-module REVIEWER-VACUITY --dry-run` | 0 | `06-false-mutation-build.log` |
| False-result proof | `kprove reviewer-vacuity.k --definition verification-kompiled-fresh --spec-module REVIEWER-VACUITY` | 1, expected stuck claim | `06-false-mutation-kprove.log` |
| Unicode-code-sequence ground claims | `kprove unicode-intseq-spec.k --definition verification-kompiled-fresh --spec-module UNICODE-INTSEQ-SPEC` | 0, `#Top` | `07-unicode-intseq-ground-checks.log` |

Each positive target was run separately by `run_positive_claims.sh` as:

```text
kprove spec.k --definition verification-kompiled-fresh --spec-module SPEC --claims SPEC.<label>
```

The ten labels were `empty-name`, `bad-dot-count`, `bad-initial`,
`bad-extension`, `too-many-digits-txt`, `too-many-digits-exe`,
`too-many-digits-dll`, `valid-name-txt`, `valid-name-exe`, and
`valid-name-dll`. Every command exited 0 and printed `#Top`; each has a
separate `03-kprove-<label>.log`.
