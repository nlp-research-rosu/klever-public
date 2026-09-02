Diagnostic attempt (not a candidate target-proof command)

Command, run in `/tmp/audit-work/candidate-scratch`:

```sh
kprove spec.k --definition audit-verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.entry-keep \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
```

The process was manually interrupted after approximately 300 seconds, with
exit status 130 and no emitted output. Claim filtering removes the separately
proved invariant from the selected claim set before it can be reused; this is
not the candidate's recorded split-proof workflow. The unfiltered entry-phase
command in `prove_all_entries.log` retained the trusted, separately proved
invariant, covered all three entry claims, printed `#Top`, and exited 0.
