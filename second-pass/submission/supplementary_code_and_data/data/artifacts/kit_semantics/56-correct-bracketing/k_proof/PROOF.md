VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every finite `IntSeq` `CODES` such that
`bracketChars(CODES)` is true, calling the exact translated
`correct_bracketing` closure with `str(CODES)` reaches a Boolean `RESULT` such
that:

```k
RESULT ==Bool bracketCorrect(CODES)
```

`bracketCorrect(CODES)` is true exactly when every consumed prefix has
nonnegative balance and the final balance is zero.  The call starts in the
module environment shown in `spec.k` and restores the environment, scopes,
scope allocator, heap, heap allocator, call stack, return cell, exception cell,
and exit code shown there.  This is a partial-correctness reachability theorem;
it does not separately assert liveness.

## Formal claims

- `SPEC.loop-inv` executes the real `#loop` over a symbolic string suffix.  It
  proves that final `balance` is `BAL +Int bracketDelta(CODES)` and final
  `valid` is
  `VALID andBool bracketPrefixOK(CODES, BAL)`.  The loop variable may change;
  the original argument and parent scope are preserved.
- `SPEC.correct-bracketing` performs real name lookup, argument evaluation,
  frame allocation, parameter binding, all source statements, return, and
  frame pop for the exact closure body in `solution.mpy`.  It constrains the
  returned Boolean to `bracketCorrect(CODES)`.

The loop obligations are:

1. Base: an empty suffix changes neither balance nor validity.
2. Step: string iteration yields one character; the real branch, assignment,
   validity check, and loop continuation agree with the constructor equations.
3. Entry discharge: the loop invariant is instantiated with `BAL = 0` and
   `VALID = true`, after which the real `and` return expression reduces to
   `bracketCorrect(CODES)`.

## Proof-extension inventory

The inventory below was rebuilt from `verification.k` and `spec.k`.

### `bracketDelta`

- Class: definitional summary.
- Semantic role: names the net balance change; it does not rewrite a program
  term or replace execution.
- Domain: every finite `IntSeq`; `[total]` is justified by the disjoint empty
  and `iCons` constructor cases.
- Matched context and justification scope: only the pure term
  `bracketDelta(CODES)`; the equations cover exactly that complete domain.
- State footprint: none.
- Value influence: loop final balance and the entry postcondition.
- Value justification: empty gives `0`; an `iCons` adds `1` when its code is
  `60` and `-1` otherwise, exactly matching the source `if/else`.  Structural
  recursion terminates on the tail.  `SPEC.loop-inv` is the machine-checked
  connection from fixed loop execution to this value.
- Dependents: both positive claims.
- Control/value validation: no control is abstracted.  Concrete K tests cover
  both character branches; the universal loop claim supplies the value
  connection.

### `bracketPrefixOK`

- Class: definitional summary.
- Semantic role: names whether every post-character balance in a suffix is
  nonnegative; it does not replace execution.
- Domain: every finite `IntSeq` and every `Int`; empty and `iCons` cases are
  exhaustive and non-overlapping.
- Matched context and justification scope: only
  `bracketPrefixOK(CODES, BAL)` over its declared complete domain.
- State footprint: none.
- Value influence: final `valid`, the returned Boolean, and the postcondition.
- Value justification: the step equation selects `+1` for code `60`, `-1`
  otherwise, checks that new balance against zero, and recursively checks the
  tail.  This exactly mirrors both source `if` statements.
  `SPEC.loop-inv` executes those statements and universally connects the
  resulting local binding to the summary.
- Dependents: both positive claims.
- Control/value validation: no control is abstracted.  The initial failed
  construction exposed and repaired the negative-mid-balance case; the final
  exhaustive conditional equation covers it.

### `bracketChars`

- Class: definitional summary used as a domain predicate.
- Semantic role: constrains inputs; it replaces no execution.
- Domain: every finite `IntSeq`; empty and `iCons` cases are exhaustive.
- Matched context and justification scope: only `bracketChars(CODES)`.
- State footprint: none.
- Value influence: the `requires` clauses only.
- Value justification: it is true exactly when every code is `60` (`<`) or
  `62` (`>`), matching the prompt's stated input domain.
- Dependents: both positive claims.
- Validation: the formal domain is compared with the prompt and all enumerated
  differential samples use precisely this alphabet.

### `bracketCorrect`

- Class: definitional summary.
- Semantic role: names the intended result; it replaces no execution.
- Domain: every finite `IntSeq`; its single equation is total.
- Matched context and justification scope: only `bracketCorrect(CODES)`.
- State footprint: none.
- Value influence: the target postcondition.
- Value justification: it is the conjunction of prefix safety from initial
  balance zero and final delta zero.  The loop claim connects both components
  to real execution, and the entry claim connects the real return expression
  to their conjunction.
- Dependents: `SPEC.correct-bracketing`.
- Value validation: K concrete executions include both true and false results;
  `SPEC-VACUITY.false-result-empty` attempts the opposite value on `""` and is
  rejected.

### `SPEC.loop-inv`

- Class: derived reachability lemma/circularity.
- Semantic role: summarizes, through coinductive reachability, repeated
  fixed-semantics execution of the exact `#loop`; it is not an ordinary
  operational rewrite.
- Domain: every suffix satisfying `bracketChars`, every integer `BAL`, every
  Boolean `VALID`, and the exact four-binding local scope shape in the claim.
- Matched context: the exact loop target and body, current local environment,
  exact local map, arbitrary preserved continuation, disjoint surrounding
  scopes, and all other framed configuration cells.
- Justification scope and containment: the claim itself is universal over the
  framed continuation and cells.  The body has no return, break, continue,
  exception, call, allocation, or heap action, so fixed execution consumes
  only the loop and preserves the continuation.  It reads/writes only the
  named local bindings and preserves all framed cells.
- State footprint: reads `balance` and `valid`; writes `balance`, `valid`, and
  `bracket`; preserves `brackets`, the parent, surrounding scopes, and every
  omitted operational cell.
- Value influence: supplies both values used by the entry result.
- Justification: base and constructor step are proved by fixed symbolic
  execution; recursive application is the circularity.
- Dependents: `SPEC.correct-bracketing`.
- Control validation: the entry proof uses the lemma with the real trailing
  `Return(...) ~> #endcall`, demonstrating preservation of an observable
  continuation.
- Value validation: the universal entry connection, eight concrete K
  assertions, and 511 independent CPython comparisons.

There are no proof-local operational bridges, trusted primitives, opaque
result-bearing symbols, priority rules, or simplification axioms.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`.  Running:

```bash
./prove.sh
```

exited `0`.  Its component results were:

```text
python3 py2mpy.py solution.py > solution.mpy
Exit: 0

python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
Exit: 0

python3 concrete_tests.py
Output: (none)
Exit: 0

python3 differential_test.py
Output: checked=511 mismatches=0
Exit: 0

kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
Exit: 0
Output: compiler warnings in supplied semantics; no error

krun concrete_tests.mpy --definition runtime-kompiled
Output: final <k> .K </k>, <exit-code> 0 </exit-code>, empty stack/heap
Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
Exit: 0
Output: supplied-semantics unused-variable warnings; no error

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv
Output: #Top
Exit: 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
Output: #Top
Exit: 0

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
Output: WarnStuckClaimState with actual <k> true ~> .K </k>
Exit: 1 (expected)

kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
Output: WarnStuckClaimState with actual <k> false ~> .K </k>
Exit: 1 (expected)
```

The regenerated `solution.mpy` was also byte-compared with translator output
during construction.  Its final SHA-256 is
`bf1cca1c9f6ca6e8178453bc46114854d97627930072093c07e01618cf9cb1b0`.

## Gate results

### Gate A — PASS

- A1: the exact closure body from `solution.mpy` is present in the entry claim
  and executes under fixed semantics.  Changing `balance = 0` to `balance = 1`
  makes the empty-input theorem fail with actual result `false`.
- A2: no operational bridge skips state.  The entry claim pins and restores
  every active configuration cell; the loop claim records all changed local
  bindings.
- A3: lookup is pinned to the exact `"correct_bracketing"` module binding;
  argument evaluation, parameter binding, character comparison, branch order,
  return, and frame pop all execute.  The loop body has no abrupt control.
- A4: every proof-local total function has exhaustive constructor coverage,
  disjoint cases, truthful conditionals, and structural recursive descent.
- A5: `CODES = .IntSeq` is a realizable witness.  The real result is `true`;
  the false-result mutation is rejected with exit `1` and a residual showing
  that `true`.

### Gate B — PASS

- B1: the precondition exactly formalizes the prompt's strings of `<` and `>`.
  Empty strings are included.
- B2: on this domain the supplied semantics' finite ASCII code sequences,
  mathematical integers, Booleans, string iteration, and equality match the
  relevant Python behavior.  No unsupported exceptions or external state are
  involved.
- B3: prefix nonnegativity rules out unmatched closing brackets; zero final
  balance rules out unmatched opening brackets.  Their conjunction is the
  requested bracketing property, and the execution-to-summary connection is
  formally proved.
- B4: the implementation agrees with all prompt examples and the independently
  checked finite sample.

### Gate C — PASS

- C1: the only theorem-level trust boundary is the supplied `MPY` semantics
  plus the K compiler, Haskell prover/backend, LLVM executor, and their integer
  and Boolean hooks.  No proof-local unproved value or control primitive is
  used.
- C2: all claimed evidence has an existing artifact and exact command in
  `prove.sh`; both negative probes expose their contrary concrete results.
- C3: the positive result is reported as a partial-correctness theorem under
  the supplied semantics.  Finite tests are identified as evidence rather than
  a universal proof.

## Trust ledger

- Supplied `MPY` reference semantics: fixed theorem base; affects value,
  binding, control, state, and modeled exceptions for both claims.  Evidence:
  required LLVM build, eight concrete K assertions, and direct inspection of
  the relevant iteration/call/control rules.
- K v7.1.293 Haskell backend and solver: trusted to implement reachability and
  report `#Top`; affects both symbolic claims.  Evidence: positive proofs plus
  rejecting result and body mutations.
- K LLVM backend: used only for finite concrete evidence, not universal proof.
- `py2mpy.py`: supplied translation boundary.  The committed `solution.mpy` is
  regenerated from `solution.py` by `prove.sh`; neither file contains a proof
  shortcut.
- CPython stack oracle in `differential_test.py`: finite independent adequacy
  evidence only; it does not contribute axioms to the K proof.

## Empirically supported facts

- `concrete_tests.mpy` executes eight assertions: the four prompt examples,
  empty input, nested input, sequential pairs, and multiple leading closers.
  LLVM execution ends at `.K` with exit code `0`.
- `differential_test.py` compares the implementation with an independently
  structured stack oracle for all 511 strings over `<` and `>` of lengths
  zero through eight.  It reports zero mismatches.

## Excluded behavior

- Values that are not strings and strings containing characters other than
  `<` or `>` are outside the formal precondition.
- The theorem is about the supplied `MPY` model, not all of CPython, Unicode,
  resource exhaustion, or implementation-specific behavior.
- Liveness, time complexity, and memory complexity are not formalized.
- Configurations with a different module binding, extra local bindings, a
  non-clean call state, or a different function body are outside the entry
  claim.
