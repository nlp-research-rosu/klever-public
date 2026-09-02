# Dependency-stripped diagnostic interruption

The reviewer initially invoked:

```text
kprove connection-spec.k \
  --definition /tmp/audit-work/104-unique-digits-audit/connection-fresh-kompiled \
  --spec-module CONNECTION-SPEC \
  --claims CONNECTION-SPEC.digit-loop-positive-connection
```

This selector removed the `digit-loop-general` circularity on which the selected
connection claim depends. After the isolated run produced no result for about
100 seconds, the reviewer sent SIGINT. The enclosing execution session exited
130. The partial output is retained in
`stage3_claim_connection_digit_loop_positive.log` and
`stage3_prove_all_summary.log`; it is not treated as a proof attempt, timeout,
or candidate failure.

The correct source-declared suite invocation, which makes the auxiliary
circularity available, is recorded in `stage3_connection_suite.log`; it printed
`#Top` and exited 0. `stage3_target_suite.log` likewise proves all three target
claims together, as required by their circularity dependencies.
