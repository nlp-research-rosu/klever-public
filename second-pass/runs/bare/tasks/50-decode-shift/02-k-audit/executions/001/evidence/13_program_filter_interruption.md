# Isolated program-filter diagnostic

Command:

`kprove spec.k --definition semantic-proof-kompiled --spec-module SPEC --claims program-correct`

The command was launched at `2026-07-23T13:23:12Z` from
`/tmp/audit-work/50-decode-shift/candidate-src`. Filtering to only
`program-correct` also removes the `loop-correct` circularity that the entry
claim uses. The resulting proof kept consuming CPU while symbolically
unrolling an arbitrary-length `Chars` input and emitted no result. The reviewer
sent SIGINT after approximately three minutes. The unified execution tool
reported exit status 130; because SIGINT terminated the logging wrapper before
its epilogue, `13_kprove_program_correct.log` contains the exact command and
start time but no synthetic completion record.

This is a dependency-isolation diagnostic, not a positive reconstruction
result. Positive closure of the end-to-end target is tested with
`loop-correct` present and separately by the complete aggregate.
