---
name: proving-spec
description: 'Use when a K spec does not pass kprove yet — the proof hangs, diverges, prints WarnStuckClaimState, or exits non-zero — and you need to make it pass.'
---

## What this skill does

`spec.k` is a set of K reachability claims. `kprove` attempts to prove each claim by symbolically executing from the LHS and checking it reaches the RHS under the given conditions. When the proof fails, `kprove` exits non-zero and prints a residual configuration — the state it reached but could not close. This skill provides the tools to read that residual and extend `verification.k` until the proof closes.

Use `writing-spec` before this skill if `spec.k` is not yet written.

---

## Why proofs get stuck

`kprove` closes a claim by rewriting the LHS to the RHS. It gets stuck when:

- **Symbolic arithmetic does not reduce.** The backend cannot discharge the
  remaining obligation as written. Express the result through a summary whose
  defining equations or lemmas fit a theory the prover can use.
- **The loop-invariant circularity does not fire.** The recurring symbolic
  configuration does not match the invariant claim's left-hand side closely
  enough for the claim to apply, so the prover expands another iteration. See
  [circularity debugging](../shared/kprove-debug-troubleshoot/circularity-not-applying.md).
- **A helper rule is in the spec module instead of `verification.k`.** Plain `rule` statements in the spec module are a K compiler error; only `claim`s and `[simplification]` rules are allowed there.

The repair loop below addresses each of these systematically.

---

## Before adding a proof extension

Read the [proof-extension soundness contract](../shared/proof-extension-soundness.md).
For the proposed change, answer these questions from the residual:

1. What fixed-semantics step or mathematical obligation is missing?
2. Which extension class applies?
3. **Does this replace execution?** If yes, identify the exact binding, body,
   evaluation steps, control behavior, and state footprint being replaced.
4. What is the complete matched context, including the active continuation,
   control stack, bindings, guards, and framed cells?
5. Is every frame, wildcard, or omitted cell equally general in the theorem or
   assumption that supplies the justification domain?
6. Does the extension introduce abrupt control such as return, frame popping,
   an exception, or loop control? If so, what proves the same continuation is
   discarded, preserved, or unwound under fixed semantics?
7. Does the extension's value affect a branch, result, observable state,
   exception, or postcondition? If so, what machine-checked connection theorem
   proves that fixed semantics produces that value over the complete domain?
8. Does the same fresh or opaque symbol occur in both an operational bridge and
   a summary or postcondition? That dependency is circular unless independently
   connected to fixed execution.
9. What guard makes every new equation true, and do its cases overlap existing
   equations consistently?
10. Which claim depends on the extension, and what theorem or named trust
   assumption justifies it?

Complete the contract's extension record before editing `verification.k`. If a
program-defined operation cannot be connected to execution, strengthen the
invariant, add an auxiliary execution claim, route a genuine language-model gap
to `writing-semantics`, or continue the same-session repair loop below.

Do not introduce a result-bearing oracle to make a residual disappear. Exact
syntax and bindings prove where a bridge applies, not which value it returns.
If no machine-checked connection theorem or truthful definition fixes that
value, let fixed semantics execute, strengthen the invariant, or narrow the
theorem honestly.

For an operational bridge, place its complete LHS and RHS beside the exact
supporting theorem and check that the bridge match domain is contained in the
justification domain. A theorem over one trailing computation does not justify
framing an arbitrary `<k>` continuation. Narrow the bridge to the proved context
or prove a separate context theorem; comments, priority, and a correct summary
value do not repair scope widening.

Before admitting any operational bridge, prove a bridge-free universal
connection theorem over its complete match domain. That theorem must not import
the proposed bridge; prove it with fixed semantics and independently justified
theory. Finite tests do not satisfy this precondition.

## Same-session Gate A repair loop

When `validating-proof` reports a Gate A failure, continue within the current
agent invocation and preserve the current solution and proof artifacts:

1. **First, remove or disable the offending extension.** Do not treat `#Top`
   obtained through that extension as a usable proof state.
2. Recompile and rerun without it, then inspect the genuine residual produced
   by fixed semantics and the remaining justified theory.
3. **Prefer fixed-semantics execution** and address the residual without an
   execution-bypassing rewrite.
4. **Prove an exact auxiliary execution theorem** before any operational bridge,
   covering every configuration in the proposed bridge's match domain without
   importing that bridge.
5. Strengthen the invariant or use a truthful definitional summary when that
   expresses the source computation exactly.
6. If the original intent is broader than the sound theorem currently
   available, preserve the narrower theorem honestly as partial progress and
   allow Gate B to report `SOUND-BUT-LIMITED`. When the task requires the full
   source contract, do not treat finitely many sizes, examples, or bounded
   unrollings as completion of the required target proof; keep repairing the
   symbolic theorem, or leave the required target unresolved.
7. Produce terminal `Incomplete work` only when repair attempts expose an
   evidenced hard blocker under the shared contract.

After a repaired construction reaches `#Top`, return to `validating-proof` and
restart Gate A. This loop is construction inside the original one-shot
invocation, not a retry or later audit-feedback attempt.

---

## Summary functions

A **summary function** names the mathematical result computed by the loop.
Define it in `verification.k` as a `[function, total]` declaration with
equations that cover all inputs. The example below has a convenient closed
form; other results may require a recursive definition.

```k
// verification.k
requires "semantics.k"

module VERIFICATION-SYNTAX
  imports INT
  syntax Int ::= sumTo(Int) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports SEMANTICS
  imports INT
  imports BOOL

  rule sumTo(N) => (N +Int 1) *Int N /Int 2  requires N >=Int 0
  rule sumTo(N) => 0                          requires N  <Int 0
endmodule
```

- `[function]` — this is a function symbol, not a rewrite rule.
- `[total]` — the equations cover all inputs; the prover may assume totality.
- Two guarded equations split on the sign so coverage is complete.

**Choose the simplest faithful form the prover can use.** Prefer an equivalent
closed form when it lies in a solver-supported theory. If no faithful closed
form exists, keep the recursive definition; do not replace it with an
inaccurate formula merely to make the proof close. Use explicit base/step
equations plus targeted induction, folding, or summary lemmas. A recursive
evaluator can still unfold indefinitely on a symbolic argument, so diagnose
that mechanism rather than rejecting recursion itself. See
[`k-proof-technique`](../k-proof-technique/SKILL.md) and
[symbolic-recursion debugging](../shared/kprove-debug-troubleshoot/symbolic-recursion.md).

**Add `[simplification]` lemmas** for algebraic facts the prover cannot derive on its own. A `[simplification]` rule fires during symbolic simplification, not during normal rewriting. Keep them in `verification.k` (or, if they apply only to a specific proof, in the spec module):

```k
rule (X +Int Y) ==Int X +Int Z => Y ==Int Z  [simplification]
```

---

## Invariants and lemmas

The loop-invariant claim in `spec.k` is the loop invariant. When the proof is stuck on the invariant's inductive step, you have two options:

1. **Strengthen the invariant.** Add a conjunct to the `requires` or express a tighter postcondition.
2. **Add a lemma.** Add a `[simplification]` rule to `verification.k` that lets the prover discharge the residual algebraic obligation.

Keep the invariant and the summary function consistent: the invariant postcondition (`s |-> S +Int sumTo(N)`) and the summary function definition (`sumTo(N) = N*(N+1)/2`) must describe the same quantity.

---

## The repair loop

```
run kprove → read the residual → add one lemma or strengthen invariant → re-run
```

**Step 1: run `kprove`.**

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

A bare `#Top` on stdout with exit code 0 means the claim closed under the
supplied theory; it is necessary but insufficient for a validated proof.
Failure is a non-zero exit with a `WarnStuckClaimState` warning and a residual
configuration on stdout.

**Step 2: read the residual.** The residual is the symbolic configuration `kprove` reached but could not match against the claim's RHS. Compare its term shape to the RHS. The mismatch locates what is missing.

**Step 3: bound and compare the trace.** Isolate one claim, choose a depth that
returns promptly, and compare residual configurations at nearby increasing
bounds. Use the symptom router and bounded-inspection procedure in
[the troubleshooting index](../shared/kprove-debug-troubleshoot/index.md).

**Step 4: add one classified change.** Complete the extension checkpoint, then
add the narrowest guarded lemma, summary equation, auxiliary claim, or invariant
strengthening that addresses the residual. Recompile and rerun the focused claim.

Record the extension even when the proof reaches `#Top`; prover success does not
validate the added theory.

Recompile `verification.k`:

```bash
kompile --backend haskell verification.k \
        --main-module VERIFICATION \
        --syntax-module SEMANTICS-SYNTAX \
        --output-definition verification-kompiled
```

**Important hygiene:**
- Prove claims in order: the loop invariant first (`--claims SPEC.loop-inv`), then the whole-program claim. A passing loop invariant makes the whole-program proof fast.

---

## References

- [Proof-extension soundness contract](../shared/proof-extension-soundness.md) —
  construction-time classification and extension-record requirements.
- [kprove debugging index](../shared/kprove-debug-troubleshoot/index.md) — symptom-based
  routing for residuals and command failures.
- [K functions, claims, and proof modules](../shared/k-claims.md) —
  `[function]`/`[simplification]`, claim syntax, and labels.
- [Running the K tools](../shared/running-k.md) — build commands and result
  interpretation.
- `writing-spec` — precedes this skill; produces `spec.k`.
- `validating-proof` — follows this skill; it independently rebuilds the
  extension inventory from the proof files rather than trusting the construction
  record, then applies Gate A — real-program soundness, Gate B — intent adequacy,
  and Gate C — trust and evidence auditability.
