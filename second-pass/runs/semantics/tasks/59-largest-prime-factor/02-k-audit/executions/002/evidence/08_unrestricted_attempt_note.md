The first unrestricted bridge-free connection attempt (`compare-gt`) exited 1
with a stuck symbolic branch involving abstract `$cells` metadata. The next
claim (`compare-mod-zero`) did not promptly finish and the reviewer interrupted
the aggregate script; its empty per-claim log is therefore not treated as a
candidate proof failure. The exact reachable scope was then isolated in
`08c_bridge-connections-reachable.k`, and all five bridge-free claims closed
individually with `#Top`.
