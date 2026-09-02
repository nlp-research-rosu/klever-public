# Standalone entry-selector diagnostic

Command:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.pluck-entry
```

The command was started from `/tmp/audit-work/68-pluck` after a successful
fresh build and a successful standalone `SPEC.pluck-loop` proof.  It was
interrupted by the reviewer after more than 13 minutes of active `kore-exec`
CPU use.  Selecting only `SPEC.pluck-entry` excludes `SPEC.pluck-loop` from the
selected claim set, so this diagnostic removes the circularity that the entry
proof needs and is not the candidate's target proof.  It is not used as a
positive or negative verdict datum.  The unmodified full `SPEC` invocation,
which includes both the loop circularity and entry theorem, is recorded
separately.
