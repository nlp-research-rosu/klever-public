# kprove debug and troubleshoot

Start with the exact command, exit status, and residual configuration. Match the
observed symptom below, then open only the owning reference.

| Symptom | Open |
|---|---|
| K command is missing from the shell | [running-k.md — Shell setup](../running-k.md#shell-setup) |
| Backend or kompiled-definition mismatch | [running-k.md — Backends](../running-k.md#backends) |
| K cannot find the requested main syntax module | [running-k.md — Backends](../running-k.md#backends) |
| Unsure whether `#Top` means success | [running-k.md — Reading the result](../running-k.md#reading-the-result) |
| Proof module rejects an ordinary rule | [k-claims.md — Functions and simplification](../k-claims.md#functions-and-simplification) |
| `Unused filtering labels` from `--claims` or `--exclude` | [k-claims.md — Claim labels](../k-claims.md#claim-labels) |
| A symbolic helper keeps expanding | [symbolic-recursion.md](symbolic-recursion.md) |
| A loop repeats and the invariant is never applied | [circularity-not-applying.md](circularity-not-applying.md) |
| The proof runs without revealing where progress stops | Bounded inspection below |

## Bounded inspection

First isolate one claim with `--claims`. Then rerun it with a proof-step bound
that returns promptly:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.claim-label \
  --depth N
```

Choose `N` from the scale of the observed trace, not from a universal fixed
number. Compare the residual configuration at nearby increasing bounds:

- New program points indicate continued symbolic progress.
- The same non-reducing subterm indicates a missing rule, undecidable guard, or
  helper that cannot simplify.
- Repeated loop-head shapes without claim application indicate a circularity
  matching problem.
- Rapidly growing helper terms indicate symbolic recursion.

A depth-limited result is diagnostic, not a proof result. Fix one identified
mechanism, rebuild if needed, and rerun the isolated claim without the bound.
