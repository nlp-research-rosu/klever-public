# Optional filtered-command diagnostic

This was an additional reviewer diagnostic, not one of the candidate's recorded
positive targets:

```sh
kprove /tmp/audit-work/fresh/spec.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --spec-module SPEC \
  --claims SPEC.concatenate-correct \
  --trusted SPEC.concatenate-loop
```

It produced no stdout for more than five minutes. A process check at elapsed
04:36 showed `kore-exec` running at about 103% CPU with about 2.5 GiB RSS. The
reviewer interrupted it with Ctrl-C; the controlling command returned status
130. This diagnostic is not used as candidate evidence and is not treated as a
failure or timeout verdict.

The candidate's exact recorded target omits `--claims`:

```sh
kprove /tmp/audit-work/fresh/spec.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --trusted SPEC.concatenate-loop
```

That exact target subsequently exited 0 and printed `#Top`; see
`stage3_prove_entry.sh` and `stage3_prove_entry.log`.
