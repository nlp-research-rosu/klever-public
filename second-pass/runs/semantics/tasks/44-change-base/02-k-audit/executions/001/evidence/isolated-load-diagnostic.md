# Isolated load diagnostic

The first attempt to isolate the load claim used `spec-entry-load.k`, which
omitted the direct-call recursive summary claim. That claim is an auxiliary
circularity needed by the load claim. The prover remained CPU-active for more
than five minutes without output and was intentionally interrupted (tool exit
130). A second diagnostic retained both claims but selected only `entry-load`
with `--claims`; filtering also removed the helper circularity, and that run was
likewise intentionally interrupted (tool exit 130). Neither diagnostic is
treated as a target-proof failure.

Three short syntax experiments then established that this K version has no
source-level `trusted` claim attribute; logs 13, 14, and 15 are parser failures
with exit 113. A further run combining `--claims entry-load` with
`--trusted entry-call` still filtered the helper before proving and was
intentionally interrupted (log 16, tool exit 130).

The successful auditable separate load-entry run is log 17. It uses only
`--trusted SPEC-LABELED.entry-call`, with no `--claims` filter: K skips
reproving that byte-identical, separately closed helper but retains it as a
circularity, and proves the only remaining claim (`entry-load`) with exit 0 and
`#Top`. The original unmodified two-claim module was also run as a unit with no
trusted claims.
