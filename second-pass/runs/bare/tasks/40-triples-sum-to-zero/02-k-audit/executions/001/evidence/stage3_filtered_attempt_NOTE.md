The first reviewer reconstruction additionally tried to prove
`SPEC.triples-correct` after using `--claims` to remove its prerequisite
`SPEC.pair-correct`. The helper-free filtered proof kept unfolding the recursive
entry call for 177 seconds and was interrupted by the reviewer (shell status
130); this is not treated as a candidate proof failure. The preserved partial
log is `stage3_filtered_attempt.log`.

The definitive reconstruction in `stage3_reconstruction.log` instead checks
the claims in dependency layers: `pair-correct` alone; `pair-correct` and
`triples-correct` together; then all three claims including `program-correct`.
Each layer must exit zero and print `#Top`.
