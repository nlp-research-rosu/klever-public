# Evidence index

The decisive records are:

- provenance: `logs/stage1-provenance-final.log`
- generation trace inspection: `logs/stage1-generation-trace-summary.log`
- trusted translation identity: `logs/stage2-translation-identity.log`
- independent Python differential: `logs/stage2-differential.log`
- fresh builds: `logs/stage3-kompile-concrete.log`,
  `logs/stage3-kompile-proof.log`
- positive proofs: `logs/stage3-kprove-candidate-shape.log`,
  `logs/stage3-kprove-all.log`, `logs/stage3-kprove-loop.log`
- concrete semantics: `logs/stage3-semantics-config-safe.log`,
  `logs/stage5-unicode-semantic-compare.log`
- pinning and body sensitivity: `logs/stage4-program-pinning.log`,
  `logs/stage4-body-mutation-kprove.log`
- static inventory: `rule-inventory.md`,
  `logs/stage5-numbered-sources.log`
- non-vacuity: `spec-vacuity-audit.k`,
  `logs/stage6-vacuity-dry-run.log`,
  `logs/stage6-vacuity-kprove.log`

Superseded diagnostic records are intentionally retained:

- `logs/stage3-semantics-differential.log` is the first auditor run, which
  stopped on an auditor-side K-token decoder error.
- `logs/stage3-semantics-differential-rerun.log` corrected token decoding but
  exposed invalid UTF-16 surrogate-pair injection.
- `logs/stage3-semantics-differential-final.log`,
  `logs/stage3-semantics-unicode-witness.log`, and
  `logs/stage3-semantics-nonascii-injection-limitation.log` isolate the
  non-ASCII `krun -cS` serialization issue. The compiled-literal comparison
  supersedes them for semantics fidelity.
- `logs/stage3-semantics-differential-authoritative.log` is the same
  non-ASCII injection experiment under its original, prematurely chosen
  filename; it is not the final authority.
- `logs/stage3-kprove-program.log` records a manually stopped diagnostic that
  filtered out the required loop circularity.
- `logs/stage5-unicode-wrapper-kompile.log` records an auditor work-directory
  mistake; `logs/stage5-unicode-wrapper-kompile-rerun.log` is the successful
  build.
