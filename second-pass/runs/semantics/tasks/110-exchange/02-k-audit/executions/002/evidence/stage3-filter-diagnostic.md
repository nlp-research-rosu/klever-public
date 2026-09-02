# Entry-only filter diagnostic

Command:

`kprove spec.k --definition audit-verification-kompiled --spec-module EXCHANGE-SPEC --claims EXCHANGE-SPEC.exchange-correct --output pretty`

The command was manually interrupted with SIGINT after approximately fourteen
minutes; the tool session returned exit status 130. Filtering to the entry claim
also filters out `odd-loop` and `even-loop`, which are required circularities,
so this is not the dependency-closed target proof. The command log
`stage3-kprove-exchange-correct-qualified.log` contains the command and no
terminal prover output because SIGINT terminated the capture process.

The correct dependency-closed positive command is recorded in
`stage3-kprove-all.log`; it printed `#Top` and exited 0. Both circularities were
also run independently with module-qualified labels and each printed `#Top`.
