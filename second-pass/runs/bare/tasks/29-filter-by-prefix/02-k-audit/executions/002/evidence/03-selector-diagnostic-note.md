# Aborted claim-selector diagnostic

Command:

```text
kprove spec.k --definition verification-kompiled --claims program-correct --trusted loop-correct
```

Working directory:
`/tmp/audit-work/29-filter-by-prefix/candidate-src`.

The selector retained `program-correct` but did not retain the separately
named `loop-correct` claim, despite marking that omitted label trusted. It
produced no proof output for roughly four minutes and was manually interrupted.
The containing PTY command exited 130, so `run_logged.sh` did not get control
back to append an `EXIT_STATUS` line to
`03-kprove-program-after-loop.log`.

This was not used as a positive proof command. The corrected command retained
both labels while trusting only the already-proved helper:

```text
kprove spec.k --definition verification-kompiled \
  --claims loop-correct,program-correct --trusted loop-correct
```

It exited 0 with `#Top` in `03-kprove-program-with-proved-loop.log`. The
stronger combined run with neither claim trusted also exited 0 with `#Top` in
`03-kprove-all.log`.
