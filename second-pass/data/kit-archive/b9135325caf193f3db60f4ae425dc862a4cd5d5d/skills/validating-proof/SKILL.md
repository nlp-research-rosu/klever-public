---
name: validating-proof
description: 'Use when kprove reports success (#Top) and you must audit proof-local functions, lemmas, or rewrites, theorem intent, or the trust boundary before writing PROOF.md.'
---

## Verification is not validation

`kprove` exiting 0 with `#Top` proves closure under the supplied semantics, claims,
and proof extensions. Before reporting a proof of the program, read the
[proof-extension soundness contract](../shared/proof-extension-soundness.md) and
audit the extensions, intended property, and evidence independently.

## Rebuild the proof-extension inventory

Do not copy the construction record uncritically. Inspect `verification.k`, the
spec module, and imported proof-local modules for functions, totality attributes,
simplification and concrete rules, priority rules, ordinary rewrites, auxiliary
claims, opaque terms, and framed or omitted cells. Reconstruct the contract's
record for every extension contributing to claim closure.

For each operational bridge, identify the fixed-semantics behavior it preempts
and compare binding, evaluation, control, and every affected cell. For each
equational symbol, check guard coverage and pairwise overlap. For each opaque
term, trace whether it affects control, observable state, or the final result.

## Operational-bridge context procedure

For every operational bridge:

1. Reconstruct its complete matched context: LHS, RHS, guards, priority, active
   continuation, control stack, bindings, and framed or omitted cells.
2. Require a bridge-free universal connection theorem over the bridge's
   complete match domain. It must not import the proposed bridge; inspect its
   imports and dependencies to verify that it uses only fixed semantics and
   independently justified theory. Reconstruct the exact justification scope
   from that theorem and check that every bridge match lies inside it; an exact
   trailing computation does not justify an arbitrary continuation frame.
3. Choose a satisfiable boundary witness. Compare the fixed-semantics
   configuration with the corresponding bridge-enabled configuration over the
   result, control state, and every observable cell.
4. When the bridge admits a broader suffix, place an observable continuation
   immediately after the bridged region, such as a distinct result, state
   update, output, allocation, or exception. Fixed and bridge-enabled behavior
   must agree; rejection because the narrowed bridge does not match is also
   valid containment evidence.
5. Record the artifacts, commands, and results. This operational-sensitivity
   check is separate from the false-postcondition mutation in A5: the former
   tests execution fidelity, while the latter tests result constraint.

If a bridge introduces return, frame popping, exception propagation, loop
control, cleanup, or another abrupt effect, a value-only comparison is
insufficient. Any reachable context in which the bridge discards, preserves, or
unwinds different computation is a Gate A failure.

## Result-bearing abstraction procedure

For every fresh, opaque, or newly summarized value:

1. Trace each fresh or opaque symbol through rules and claims. Mark every
   branch, returned value, observable state, exception, and postcondition it can
   influence.
2. Classify its origin. For an **Externally trusted boundary**, confirm that the
   operation is fixed, intentionally outside the program-defined code being
   verified and outside the theorem, and that the proof is
   interpretation-parametric or makes every value-level conclusion conditional
   on the named contract. This path does not require a connection theorem or
   opposite-interpretation witnesses; record the contract and every dependent
   claim. A program-derived abstraction continues through the remaining steps.
3. Check whether the same symbol appears in both an operational bridge and the
   final summary or postcondition. Treat that as a circular dependency, not as
   evidence that the source computation has the same meaning.
4. Require a bridge-free universal connection theorem over the complete matched
   domain showing that fixed semantics produces exactly the abstraction's
   value. The theorem must not import the proposed bridge; verify its imports
   and dependencies use only fixed semantics plus independently justified
   theory. Truthful exhaustive equations may supply the value; a name,
   `[total]`, opacity, or finite differential evidence does not.
5. Choose satisfiable ground witnesses for distinct observable outcomes.
   Compare each fixed-semantics value with bridge-enabled execution, then
   attempt the opposite ground interpretation. If the extended theory admits
   the wrong branch, result, state, or exception—or merely leaves that equality
   unconstrained—Gate A fails.
6. Record both the witness artifacts and the machine-checked theorem. Ground
   checks detect result-bearing oracle failures; they do not replace the
   universal connection theorem.

## Gate A — Real-program soundness

Apply A1–A5 from the shared contract:

1. Confirm program-defined bodies execute or have exact auxiliary execution claims.
2. Compare each bridge's complete state footprint with fixed semantics.
3. Confirm binding, evaluation order, context containment, control, and
   exceptional behavior with the operational-bridge procedure.
4. Apply the result-bearing abstraction procedure, then check equation truth,
   overlap, coverage, descent, and totalization guards.
5. Exhibit a satisfiable witness and run a meaningful false-postcondition mutation.

## Gate A failure: repair before reporting

Every Gate A failure takes this back-edge unless an enumerated, evidenced hard
blocker prevents further repair. Until then, withhold the final status and do
not write `PROOF.md`. First remove or disable every offending extension,
discard `#Top` obtained through it as an unusable proof state, and return to
`proving-spec`. Rerun fixed semantics to expose the genuine residual, repair the
construction, rebuild, recover `#Top`, and restart Gate A within the same agent
invocation.

Only after repair attempts encounter an evidenced hard blocker may validation
select terminal `Incomplete work`. Hard blockers are unavailable required tools
or inputs, an out-of-scope fixed-semantics language gap, repeated external
backend or resource failure, or inconsistent requirements. Record the failed
repair attempts and concrete evidence for the blocker.

A difficult proof is not a hard blocker. A slower safe encoding is not a hard
blocker. Repair that requires redesign is not a hard blocker. `#Top` obtained
only through an unsound shortcut is not a hard blocker and cannot justify
stopping. Keep the original solution and proof artifacts and continue the
one-shot repair loop unless one of the evidenced blockers prevents further
progress.

### A5 non-vacuity procedure

Confirm the proof is discriminating by mutating a result or postcondition to a
small, deliberate false alternative. Choose a mutation that is false for a
satisfiable input, place it in a distinct spec module, and run that artifact.
For the conventional filenames and module names, the exact command is:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
kprove spec-vacuity.k --definition verification-kompiled \
       --spec-module SPEC-VACUITY || echo "EXPECTED FAILURE"
```

The mutated proof must exit non-zero and produce a stuck claim whose residual
shows the unmet condition. A useful off-by-one residual has this shape:

```
kore-exec: Warning (WarnStuckClaimState):
    The configuration's term unifies with the destination's term, but the
    implication check between the conditions has failed. ...
  { S #Equals S +Int 1 }
[Error] Prover: backend terminated because the configuration cannot be
rewritten further. See output for more details.
```

Record the exact mutation, satisfiable witness, command, exit code, and residual.
If the mutation closes, investigate the precondition, result constraint, and
whether the relevant claims were exercised before reporting success.

## Gate B — Intent adequacy

Restate the formal domain and postcondition in plain language. Compare them with
the source contract, intended property, examples, and material behaviors of the
intended execution model. Distinguish an execution summary from a theorem that
the summary has the requested meaning. Report implementation/specification
disagreements without rewriting the theorem.

Gate B failure with Gate A passing yields `SOUND-BUT-LIMITED`.
This is an honest theorem-status report, not completion of a request for the
full source contract. In particular, finitely many fixed sizes or examples do
not satisfy an unrestricted input domain. Preserve them as partial progress and
do not report the required target proof complete.

## Gate C — Trust and evidence auditability

List every named assumption and its dependents. Verify that every claimed test
artifact exists and record its exact command, input scope, oracle, and result.
Use concrete or differential tests as finite evidence, not universal proof.

### Differential-test procedure

For every summary or trusted abstraction supported by differential testing:

1. Select an independently implemented executable oracle. It must not reuse the
   proof equations or merely restate the abstraction being checked.
2. Compare the proof-side result with the oracle over boundary values, small
   representative values, stated examples, and a documented broader sample of
   the formal domain.
3. Require zero mismatches in the recorded run. One mismatch invalidates the
   claimed empirical support and must remain visible in Gate C.
4. Record the existing test artifact, exact command, complete input scope,
   oracle construction, output, and mismatch count.

These results are evidence about the tested inputs. They do not establish a
universal equivalence, and they do not replace the Gate A obligation to connect
program execution to any abstraction used by the proof.

Gate C failure after Gates A and B pass yields
`FORMALLY-SOUND-UNVALIDATED`.

## Decide and report the status

Record PASS or FAIL for every completed gate. Select a final status only after
Gate A passes or repair attempts encounter an evidenced hard blocker. A hard
blocker leaves `Incomplete work`; after Gate A passes, Gate B failure is
`SOUND-BUT-LIMITED`, Gate C failure is `FORMALLY-SOUND-UNVALIDATED`, and all
three gates passing is `VALIDATED`. Never hide later-gate failures.

## Write PROOF.md

Begin with the exact status. Include, in order: what is proven; formal claim;
proof-extension inventory; exact commands and actual outputs; per-gate results;
trust boundary; empirically supported facts; and excluded behavior.

Preserve the commands actually used. A conventional build and proof record has
this form:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
kompile --backend haskell verification.k \
        --main-module VERIFICATION \
        --syntax-module SEMANTICS-SYNTAX \
        --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
# Output: #Top   Exit: 0
```

Do not replace actual outputs with expected outputs. Clearly separate formally
proved facts, conclusions conditional on named assumptions, finite empirical
evidence, and excluded behavior.

## References

- [Running the K tools](../shared/running-k.md) — `#Top` success and stuck-claim
  output needed to interpret proof and mutation runs.
- `proving-spec` — precedes this skill; produces the proof artifacts to audit.
- `writing-spec` — drafts the formal claim; intent adequacy is audited here.
