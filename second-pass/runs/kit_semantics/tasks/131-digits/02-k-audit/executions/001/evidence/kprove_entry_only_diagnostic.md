Command:

```text
kprove spec.k --definition /tmp/audit-work/rebuilt-verification-kompiled --spec-module SPEC --claims SPEC.digits-entry
```

The fresh entry-only selector remained compute-bound without output for
approximately nine minutes and was manually interrupted with Ctrl-C. The
containing execution cell exited 130. This is not counted as a successful proof
or as a candidate failure: selecting only `SPEC.digits-entry` omits its
`SPEC.digits-loop` auxiliary circularity. The submitted positive proof command
selects the complete `SPEC` module; that separate run is recorded in
`kprove_all_fresh.log`.
