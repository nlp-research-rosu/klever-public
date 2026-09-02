VALIDATED

## What is proven

For every pair of mathematical integers `A` and `B`, the translated body of
`greatest_common_divisor(A, B)` reaches the non-negative Euclidean greatest
common divisor `gcdEuclid(A, B)` under the supplied MPY semantics.

The K proof is compositional:

1. `SPEC.gcd-entry` proves that calling the exact closure translated from
   `solution.py` creates the expected plain local frame, executes the
   docstring and `remainder = 0`, and reaches the exact internal loop-head
   configuration.
2. `SPEC.gcd-loop` proves that this loop-head configuration reaches
   `gcdEuclid(A, B)`, restores the caller environment, removes the callee
   scope and stack frame, leaves the heap unchanged, clears return control,
   raises no modeled exception, and preserves exit code 0.
3. Reachability transitivity composes those two claims.  The target of
   `gcd-entry` is exactly an instance of the source of `gcd-loop` with
   `GLOBALS` equal to the module map, `_R = 0`, and `CONT = .K`.

The reachability claims establish partial correctness.  Termination is also
justified mathematically: when `b != 0`, Python remainder satisfies
`abs(a % b) < abs(b)`, so the non-negative measure `abs(b)` strictly decreases.

Artifact identity:

```text
dce14f86481ce2d9825f6d3ae7fbb885babff0877b1eaa29061b5ab93bdae2d7  solution.py
61e6b834270cacb40cb008270471d85e98b6495e67b8718c573b65dd53463dc6  solution.mpy
1bee80da287f4118296af2a91287b16d4b0f0adc5a5467aef8fa7b517adeafb6  verification.k
61e80d462f7d988b198a1c6a893156233c348fa34697277a7343ef901132e8ca  spec.k
81cf2c2ac4a8d53bd53124199eae328c46cfd7c06586670d86cbdd85291a7674  prove.sh
```

## Formal claim

The input domain is all `A:Int` and `B:Int`; there is no sign or nonzero
precondition.  The observable result is the value left in `<k>`.  The proof
also observes the environment, scopes, scope allocator, heap, heap allocator,
call stack, return state, exception state, and exit code.

`gcdEuclid` is defined by the exhaustive, disjoint equations:

```text
gcdEuclid(A, 0) = abs(A)
gcdEuclid(A, B) = gcdEuclid(B, pyMod(A, B))  when B != 0
```

These equations characterize the ordinary non-negative GCD.  In the step
case, if `r = pyMod(A, B)`, then `A = q*B + r` for an integer `q`; therefore
the common divisors of `(A, B)` and `(B, r)` are identical.  The base case
has greatest non-negative common divisor `abs(A)`.  The decreasing
`abs(B)` measure makes the characterization well-founded, including for
negative operands.  It assigns `gcdEuclid(0, 0) = 0`.

## Proof-extension inventory

### `gcdEuclid` declaration and base equation

- Extension: `syntax Int ::= gcdEuclid(Int, Int) [function, total]` and
  `gcdEuclid(A, 0) => absInt(A) [simplification]`.
- Class: definitional summary.
- Semantic role: names a mathematical value; it never matches or replaces a
  program computation.
- Domain and matched context: every integer `A` with second argument exactly
  zero; value terms only, with no continuation, binding, or configuration
  cells.
- Justification scope and containment: identical to the equation domain.
- State footprint: none.
- Value influence: fixes the returned result and the loop base obligation.
- Value justification: the non-negative GCD of `(A, 0)` is `abs(A)`.
- Dependents: `SPEC.gcd-loop` and its false-result mutation.
- Control/value validation: the base branch executes the fixed `abs` lookup,
  builtin call, return, and pop rules.  The false-result probe rejects
  `absInt(A) + 1`.

### `gcdEuclid` Euclidean equation

- Extension: `gcdEuclid(A, B) => gcdEuclid(B, pyMod(A, B))` under
  `B =/=Int 0`, marked `[simplification]`.
- Class: definitional summary.
- Semantic role: folds the mathematical loop invariant; it does not rewrite
  Python syntax or any operational K item.
- Domain and matched context: all integer pairs with `B != 0`; value terms
  only.
- Justification scope and containment: exactly the guard.  The zero and
  nonzero guards are disjoint and collectively exhaustive.
- State footprint: none.
- Value influence: fixes the inductive result of `SPEC.gcd-loop`.
- Value justification: the Euclidean common-divisor argument above.
  Recursion descends by `abs(pyMod(A,B)) < abs(B)`.
- Dependents: the inductive branch of `SPEC.gcd-loop`.
- Control/value validation: fixed semantics executes `%`, all three
  assignments, loop control, `abs`, return, and frame pop before the equation
  discharges the value equality.  Replacing the computed remainder by `1`
  makes `spec-body-mutation.k` fail.

### Reachability claims

`SPEC.gcd-entry` and `SPEC.gcd-loop` are the two components of the target
theorem, not trusted semantic rules.  Neither is imported into the compiled
definition or marked trusted.  `gcd-entry` contains the exact closure body and
binding.  `gcd-loop` matches the exact reachable continuation
`Return(...) .Stmts ~> #endcall`, caller frame, environments, local bindings,
empty heap, and control cells.  Both are proved independently with the fixed
MPY operational semantics plus the two definitional equations above.

There are no operational bridge rules, opaque result symbols, priority rules,
trusted claims, or proof-local rewrites that skip a program-defined operation.

## Exact commands and actual outputs

Tool version:

```text
$ kompile --version
K version: v7.1.293
$ kprove --version
K version: v7.1.293
```

The full reproducible command sequence is in `prove.sh`.  It was run as:

```text
$ ./prove.sh
...
differential cases: 11201; mismatches: 0
...
#Top
...
#Top
...
#Top
...
EXPECTED FAILURE: false-result mutation exit 1
...
EXPECTED FAILURE: body mutation exit 1
$ echo $?
0
```

The three positive target-proof commands were:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.gcd-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.gcd-entry

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Each printed `#Top` and exited 0.  The last command proves every claim in
`spec.k` in one invocation.

The Haskell proof definition was built with:

```sh
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0.  Its warnings are only unused variables in the supplied
`reference-semantics/semantics/str.k`.

The required LLVM concrete definition was built with:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0.  The supplied semantics emitted non-exhaustiveness warnings for
unrelated list/float/string helpers; none is reachable in this integer-only
program.

Concrete execution:

```text
$ krun solution.mpy --definition runtime-kompiled
<k> .K </k>
<exit-code> 0 </exit-code>

$ krun concrete.mpy --definition runtime-kompiled
"result_3_5" |-> 1
"result_25_15" |-> 5
"result_zero_neg" |-> 7
"result_both_zero" |-> 0
<exit-code> 0 </exit-code>
```

Translation identity:

```sh
python3 py2mpy.py solution.py | diff -u solution.mpy -
```

This exited 0 with no output.

Negative validation:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

This exited 1.  Its residual contains
`absInt(A) +Int 1` unequal to `absInt(A)` on the satisfiable `B = 0`
branch.

```sh
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

This exited 1.  The mutation changes the loop's remainder assignment from
`a % b` to `1`; the residual cannot equate the resulting summary with the
Euclidean summary.

## Gate results

### Gate A — PASS

- A1: the entry claim embeds the exact closure generated in `solution.mpy`;
  the translation diff is empty.  Every program-defined statement executes
  under the fixed semantics.  The body mutation invalidates the loop proof.
- A2: no operational bridge exists.  The claims explicitly track all active
  MPY state cells and prove frame cleanup, environment restoration, unchanged
  heap/allocator, `noRet`, `NoExc`, and exit code 0.
- A3: argument evaluation, local binding, lookup, statement sequencing, loop
  control, return, and pop all execute.  `notBool ("abs" in_keys(GLOBALS))`
  ensures lookup selects the supplied builtin binding.  The real
  `Return(...) .Stmts` continuation is matched exactly.
- A4: the two summary guards are disjoint and exhaustive.  Both equations are
  valid on their full domains and recursion is well-founded by decreasing
  absolute remainder.
- A5: `(A,B)=(25,15)` with the module map, empty heap, and initial local
  remainder 0 is a realizable witness.  `spec-vacuity.k` changes the result by
  `+1`; kprove rejects it with exit 1.

### Gate B — PASS

- B1: the formal domain is exactly all integer pairs, matching the prompt's
  “two integers”; no unstated positivity restriction was added.
- B2: MPY `Int` and Python integers are unbounded, and the supplied `pyMod`
  models Python's floored remainder.  Division by zero is excluded
  operationally by the loop guard.
- B3: the Euclidean common-divisor derivation connects `gcdEuclid` to the
  human-facing greatest-common-divisor property; this bridge is mathematical,
  not an opaque execution assumption.
- B4: the implementation returns the non-negative convention, agrees with
  both prompt examples, handles signs and zeros, and has no observed
  implementation/specification discrepancy.

### Gate C — PASS

- Every proof-local declaration and equation is inventoried above with domain,
  role, value influence, state footprint, justification, and dependents.
- All evidence artifacts exist and every command is reproduced by `prove.sh`.
- Positive proof, negative mutations, concrete K execution, translation
  identity, and differential testing have recorded outcomes.
- Formal reachability, mathematical justification, finite evidence, and
  excluded behavior are stated separately.

## Trust boundary

- The supplied read-only `reference-semantics/` and K v7.1.293 implementation
  are trusted to implement their documented rewrite and proof behavior.
- The proof exercises only integer literals/comparison/modulo, plain
  assignment, `while`, function call/return, name lookup, and integer `abs`.
- The standard integer fact that Euclidean remainder preserves common
  divisors and strictly decreases the absolute second component is
  mathematically justified above but is not a separate machine-checked
  number-theory theorem.
- CPython's `math.gcd` is used only as an independent finite-test oracle; no K
  claim depends on it.

## Empirically supported facts

`test_solution.py` compares the actual Python implementation against
`math.gcd` for every pair in `[-50,50]²` and 1,000 deterministic random pairs
from `[-10^12,10^12]²`:

```text
$ python3 test_solution.py
differential cases: 11201; mismatches: 0
```

The K concrete smoke program checks `(3,5)`, `(25,15)`, `(0,-7)`, and `(0,0)`
and terminates with exit code 0.  Finite tests support implementation and
model adequacy; they are not used as universal proof evidence.

## Excluded behavior

- Non-integer Python arguments are outside the formal domain.
- Python runtime features absent from the supplied MPY subset are irrelevant
  to this implementation and are not modeled.
- The K reachability result itself is partial correctness.  Termination is
  supplied by the separate decreasing-measure argument above, not by
  `kprove`.
