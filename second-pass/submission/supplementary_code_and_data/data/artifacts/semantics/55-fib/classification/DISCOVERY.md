# Trust-boundary discovery

The canonical inventory contains six rules from `FIB-VERIFICATION`. All six
are classified as `DEFINITION`.

- `fibBody`, `fibClosure`, and `fibProgram` are named expansions of the
  translated program body, closure value, and module term. They package syntax
  used by the claims and do not add execution behavior or mathematical facts.
- The two guarded `fibRun` equations are the base and recursive clauses of the
  mathematical tail-recursive Fibonacci summary.
- `fibSpec` defines the task-level summary by initializing `fibRun` with
  `(0, 1, 0)`.

None of the six inventory rules carries the `simplification` attribute. No
inventory rule is an `OPERATIONAL_RULE`: execution is supplied by the imported
reference semantics, while the local rules only name program terms and define
the mathematical summary.

## Separately proved derived lemmas

There is no canonical inventory rule that qualifies as a
`PROVED_DERIVED_LEMMA`. In particular, Stage 1 does not prove any one of these
six rule statements against a definition lacking that rule and then install
the exact proved statement as a reusable rule.

Stage 1 does contain the separately labeled auxiliary proof claim
`FIB-SPEC.fib-loop` in `spec.k`. Its evidence is:

1. `verification.k` defines `FIB-VERIFICATION` without a `fib-loop` rule.
2. `spec.k` states `FIB-SPEC.fib-loop` as a circular reachability claim.
3. `FIB-SPEC.fib-all-natural` explicitly declares
   `depends(FIB-SPEC.fib-loop)`.
4. `prove.sh` compiles `verification.k` and invokes `kprove spec.k` for the
   complete `FIB-SPEC` module.

That claim is proof evidence used by the target claim, but it is not a rule in
the canonical inventory and is never installed into the verification module.
It therefore does not cause any inventory entry to be classified as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. The verification module introduces no
additional trusted mathematical fact beyond its defining equations.
