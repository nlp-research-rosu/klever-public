# Remaining proof obligation

The full-domain target `minpath-full-contract` does not close.  Its final
bounded command is recorded in `prove.sh`.  It exits 1 with
`WarnStuckClaimState` after reaching the correct returned reference and a
concrete two-pair heap.  The failed implication contains the unreduced term

```text
snocVS(vCons(1, vCons(neighborMin, vCons(1, .ValSeq))), neighborMin)
```

on one side and the structurally identical four-element `vCons` sequence on
the other.  The residual also reports two unexplored branches, corresponding
to larger symbolic pair counts.  This is not a fixed-semantics execution gap:
the separate generalized `result-loop-tail` reachability claim closes with
`#Top`, but this backend invocation does not consume that claim while proving
the full-call target and instead unrolls the result loop again.

Repair attempts preserved in the current files include an exact evaluated
loop-head claim, a source-level wrapper claim, an exact `#while` back-edge
variant, and modular `--trusted` composition with every helper retained by
`--claims`.  The wrapper was removed because it did not close; the independently
proved generalized loop claim remains.  No operational loop-summary rewrite
was installed.

The guarded selector and range `[simplification]` rules in `verification.k`
are functional data lemmas, not control-flow rewrites.  They remain explicit
downstream proof obligations for the pipeline's Lean arm; no Lean project is
present in this workspace.  A repository-wide search found no `Proof.final`,
`native_decide`, or `Lean.ofReduceBool`, so the continuation's Lean-specific
validation warning was not applicable here.
