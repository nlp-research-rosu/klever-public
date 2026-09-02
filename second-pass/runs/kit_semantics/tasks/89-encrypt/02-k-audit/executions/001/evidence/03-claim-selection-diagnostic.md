# Standalone entry-claim diagnostic

Command:

```text
kprove /tmp/audit-work/reconstruction/spec.k --definition /tmp/audit-work/reconstruction/verification-kompiled --spec-module SPEC --claims SPEC.encrypt-entry
```

Observed output before interruption: none after the command header.

Observed exit status after reviewer `Ctrl-C`: `130`.

Interpretation: `--claims SPEC.encrypt-entry` excludes the separately named
`SPEC.encrypt-loop` circularity from the selected specification. The backend
therefore kept unrolling the symbolic loop. This is not a positive target
command and is not a candidate failure. The complete module command, with both
claims present, is recorded in `03-kprove-all-claims.log`; it returned `#Top`
and exit 0. The helper claim also closes independently in
`03-kprove-encrypt-loop.log`.
