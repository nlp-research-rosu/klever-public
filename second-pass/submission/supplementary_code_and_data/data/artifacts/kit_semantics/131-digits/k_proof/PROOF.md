VALIDATED

## What is proven

Under the supplied `MPY` semantics, both claims in `spec.k` are proved as
partial-correctness reachability claims:

- `SPEC.digits-loop` proves the loop invariant for every `N >= 0`, every
  integer accumulator `P`, and presence bit `F` in `{0, 1}`.
- `SPEC.digits-entry` proves that, for every K integer `N > 0`, loading the
  exact translated function, resolving and calling `digits(N)`, executing its
  body, and returning normally produces
  `oddDigitsProduct(N) *Int oddDigitSeen(N)`.

`oddDigitsProduct` is the product of odd decimal digits with empty product `1`;
`oddDigitSeen` is `1` exactly when an odd decimal digit occurs and `0`
otherwise. Their product is therefore the requested odd-digit product, or `0`
when all digits are even.

This is a partial-correctness result. It does not separately prove termination.

## Formal claim and scope

- Program boundary: the entry computation includes `#loadAll`, the exact
  `FuncDef` body from `solution.mpy`, name lookup, argument evaluation, function
  frame creation, the complete function body, return, and frame pop.
- Input domain: unbounded mathematical integers satisfying `N >Int 0`, exactly
  matching the prompt's positive-integer domain.
- Observable final state: the returned integer, normal `NoExc`/zero-exit
  behavior, and preservation of the initially empty heap, stack, and allocation
  counters. The final module-scope map is existential because the function
  binding left by module loading is not part of the HumanEval result.
- Intended property: the product of all odd base-10 digits, or zero if there
  are no odd digits.

The loop invariant transforms

```text
n       = N  -> 0
product = P  -> P * oddDigitsProduct(N)
found   = F  -> F + oddDigitSeen(N) - F * oddDigitSeen(N)
```

under `N >= 0` and `F in {0,1}`.

## Proof-extension inventory

There are no operational bridges, priority shortcuts, result-bearing oracles,
or added trusted primitives. Program-defined code always executes under the
fixed semantics.

### `oddDigitsProduct`

- Extension/class: the declaration and three rules at
  `verification.k:9,19-29`; definitional summary.
- Semantic role: names a mathematical value and never replaces a program
  computation.
- Domain: every `Int`. `N <= 0` is the base case. For `N > 0`,
  `pyMod(N,2)` is exactly `0` or `1`, so the even and odd guards are exhaustive
  and disjoint.
- Matched context: only a pure `oddDigitsProduct(N)` term during
  simplification; no continuation, stack, binding, or configuration cell is
  matched.
- Justification scope and containment: the defining equations apply to exactly
  the declared domain. For positive `N`, `pyMod(N,10)` is the last decimal
  digit and `(N - pyMod(N,10)) / 10` removes it. The recursive argument is
  nonnegative and strictly smaller, so recursion descends.
- State footprint: none.
- Value influence: the loop's final `product` and the entry claim's return
  value.
- Value justification: exhaustive, disjoint, terminating equations for the
  empty, odd-last-digit, and even-last-digit cases.
- Dependents: `SPEC.digits-loop` and `SPEC.digits-entry`.
- Validation: the positive proof closed; `test_summary.py` found zero
  mismatches against an independent string-based oracle on 10,003 inputs.

### `oddDigitSeen`

- Extension/class: the declaration and three rules at
  `verification.k:10,31-39`; definitional summary.
- Semantic role and matched context: pure mathematical summary only; it does
  not replace execution and matches no operational cells or control context.
- Domain: every `Int`, with the same exhaustive, disjoint, descending
  partition as `oddDigitsProduct`.
- State footprint: none.
- Value influence: the loop's final `found` bit and the entry result.
- Value justification: the base case is `0`, an odd last digit yields `1`, and
  an even last digit recurses on the remaining decimal prefix.
- Dependents: both positive claims.
- Validation: the positive proof and the same 10,003-input independent oracle
  comparison.

### Integer normalization rules

- Extension/class: the four exact rules at `verification.k:43-46`; derived
  lemmas:

  ```k
  rule 1 *Int X => X [simplification]
  rule X *Int 1 => X [simplification]
  rule X +Int 1 -Int X => 1 [simplification]
  rule (X *Int Y) *Int Z => X *Int (Y *Int Z) [simplification]
  ```

- Semantic role/domain: universally valid integer equalities used to normalize
  the inductive post-state. They replace no Python execution.
- Matched context and justification scope: arbitrary pure integer subterms;
  the identities are true for every mathematical integer, so the match and
  justification domains coincide.
- State footprint/control effect: none.
- Value influence: normalization of `product` and `found` after applying the
  loop circularity.
- Dependents: `SPEC.digits-loop`, and transitively `SPEC.digits-entry`.
- Validation: the loop and entry claims close together; the false-result and
  body mutations remain rejected.

### `SPEC.digits-loop`

- Extension/class: machine-checked auxiliary reachability claim used as a
  circularity; derived lemma.
- Semantic role: executes the exact fixed-semantics `#while` computation and
  characterizes its final local state. It is not an operational rewrite added
  to `verification.k`.
- Domain/matched context: the exact loop body, any preserved continuation,
  current environment `L`, a local scope containing exactly `n`, `product`,
  and `found`, `N >= 0`, and `F` in `{0,1}`. Other scopes and unrelated cells
  are framed and preserved.
- Justification scope/containment: identical to the claim's match domain; the
  standalone loop obligation is included in the successful combined proof.
- State footprint: reads and writes the three named locals. It does not alter
  heap, stack, return state, exception state, or the continuation.
- Value influence: supplies the accumulator and presence-bit values used by the
  entry result.
- Dependents: `SPEC.digits-entry`.
- Control/value validation: `kprove spec.k ...` proves the loop base and
  inductive cases and the entry discharge in one run. The ground body mutation
  is rejected.

## Exact commands and actual results

Tool version:

```text
$ kompile --version
K version: v7.1.293
```

The complete reproducible run is `./prove.sh`; it exited `0`. Its substantive
commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit 0; regenerated solution.mpy.

kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit 0.

krun smoke.mpy --definition runtime-kompiled
# Exit 0; final <k> .K, <exc> NoExc, <exit-code> 0.
# result_1=1, result_4=0, result_235=15,
# result_2468=0, result_97531=945.

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit 0.

kprove spec.k --definition verification-kompiled --spec-module SPEC
# Output: #Top
# Exit: 0

python3 test_solution.py
# Output: checked=10003 mismatches=0
# Exit: 0

python3 test_summary.py
# Output: checked=10003 mismatches=0
# Exit: 0

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Expected exit: 1
# Residual <k>: 1 ~> .K, which does not match the deliberately false result 2.

kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Expected exit: 1
# Residual <k>: 0 ~> .K, which does not match the unchanged expected result 1.
```

Compilation emitted warnings in unexercised supplied-semantics modules
(`float`, list/string helpers, and unused variables in `str.k`). No warning
identified a construct used by this program, and all commands had the recorded
exit statuses.

## Gate results

### Gate A — PASS

- A1: the exact program body, binding, call setup, loop, return, and frame pop
  execute under fixed semantics. Changing `found = 1` to `found = 0` makes the
  ground connection fail with result `0` instead of `1`.
- A2: no operational bridge exists. The loop claim explicitly constrains its
  three modified locals and frames the cells the fixed loop does not touch.
- A3: normal lookup, left-to-right argument evaluation, integer operations,
  branch control, looping, return, and frame restoration remain in the entry
  computation. No fresh value influences a branch or result.
- A4: both summary functions have disjoint, exhaustive, descending equations.
  All four simplification rules are universal integer identities; where the
  multiplication identities overlap, they normalize to the same value.
- A5: `N=1` is a realizable witness. The false postcondition `1 => 2` is
  rejected with exit `1`; concrete witnesses also include `4` and `235`.

### Gate B — PASS

- B1: `N > 0` exactly matches “positive integer”; no hidden upper bound or
  digit-count restriction is introduced.
- B2: the relevant model uses arbitrary-precision mathematical integers.
  For positive inputs its `//` and `%` behavior agrees with Python, and all
  exercised syntax is modeled by the supplied semantics.
- B3: the summaries directly recurse over the base-10 last digit and remaining
  prefix. Since 10 is even, `N` and its last digit have the same parity. The
  all-even case is converted from empty product `1` to required result `0` by
  `oddDigitSeen`.
- B4: implementation and theorem agree with the stated examples and all
  concrete/differential evidence.

### Gate C — PASS

Every stated test has an existing artifact, exact command, input scope, oracle,
and observed result. Negative probes report their expected nonzero status.
Finite testing is used only as corroborating evidence, not as a universal
proof or an operational-bridge justification.

## Trust boundary

- Supplied `reference-semantics/`: trusted as the Python-subset model. It
  affects value, state, and control for both claims. LLVM smoke execution and
  the positive/negative Haskell runs provide task-local evidence.
- K v7.1.293, the Haskell backend, its SMT reasoning, and the LLVM backend:
  trusted tooling. All machine-checked conclusions depend on them.
- `py2mpy.py` and CPython AST parsing: trusted for source-to-constructor
  translation. `prove.sh` regenerates `solution.mpy`, and the entry claim embeds
  the same constructor body.
- The definitional equations and four derived integer identities in
  `verification.k`: proof-local mathematical theory, audited above. They affect
  values but not execution or control.
- The natural-language interpretation of “decimal digit”: connected to the
  formal quotient/remainder definition by ordinary base-10 arithmetic and
  corroborated by `test_summary.py`.

## Empirical evidence

- `smoke.py`/`smoke.mpy`: LLVM execution of the three prompt examples plus an
  all-even multi-digit input and a five-odd-digit input; all assertions pass.
- `test_solution.py`: compares the Python implementation with an independently
  written string-digit oracle for integers `1..10000` and
  `111111, 246802468, 975319753`; 10,003 checks, zero mismatches.
- `test_summary.py`: evaluates the proof equations and compares them with a
  separate string-digit oracle over the same scope; 10,003 checks, zero
  mismatches.
- `spec-vacuity.k`: false-result mutation rejected.
- `spec-body-mutation.k`: material source-body mutation rejected.

## Excluded behavior

- Inputs that are zero, negative, non-integer, or otherwise outside the
  prompt's positive-integer domain.
- Termination/liveness as a separate theorem.
- CPython behavior outside the constructs and state modeled by the supplied
  reference semantics.
- The exact final module-scope map, which is not observable in the HumanEval
  return-value contract.
