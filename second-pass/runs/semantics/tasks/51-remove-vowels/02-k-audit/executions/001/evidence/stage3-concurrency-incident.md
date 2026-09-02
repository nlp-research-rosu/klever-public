# Stage 3 concurrency incident

An exploratory attempt launched four labeled `kprove` invocations
concurrently. This was not used as candidate evidence:

- `SPEC.loop-empty` completed with exit 0 and `#Top`.
- `SPEC.loop-vowel` encountered a transient toolchain diagnostic ("K requires
  Java 17 ... detected version is .") and exited 2.
- `SPEC.loop-nonvowel` and `SPEC.entry` produced no prover result while the
  concurrent processes contended; both reviewer-owned sessions were interrupted
  with Ctrl-C and the terminal tool reported process exit 130.

The checks were then serialized. The empty claim closed alone, the two recursive
claims closed as the mutually inductive pair they are, and the entry claim
closed with those already-proved helpers marked trusted in a reviewer-only
spec. The successful serialized logs, not this incident, are the reconstruction
evidence.
