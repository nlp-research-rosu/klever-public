# Excluded label-filter diagnostic

The tail of `03_rebuild_and_prove.log` records this exploratory command:

```text
timeout 300s kprove /tmp/audit-work/131-digits/03_spec_labeled.k \
  --definition /tmp/audit-work/131-digits/verification-fresh-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry-contract
```

Selecting only `entry-contract` also filters out the loop invariant that the
entry proof uses as a circularity. The auditor interrupted the diagnostic
wrapper (outer exit 130) rather than wait for a five-minute bound after that
dependency error was recognized. It is not treated as a candidate proof run or
as candidate failure.

`03b_proof_targets.log` contains the completed replacement:

1. the exact submitted two-claim spec proves with exit 0 and `#Top`;
2. the loop theorem proves alone with exit 0 and `#Top`; and
3. the entry theorem proves with exit 0 and `#Top` when the independently
   proved loop theorem is marked trusted for that modular invocation.

This is ordinary theorem dependency, not circular assumption: the loop theorem
was discharged in its own preceding invocation.
