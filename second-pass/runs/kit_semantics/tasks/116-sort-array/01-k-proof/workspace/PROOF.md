VALIDATED

## What is proven

`solution.py` implements `sort_array` as two stable sorts: numeric ascending
first, then ascending by `bin(value).count("1")`.  Consequently, subject to the
supplied semantics' documented contracts for `sortVS` and `sortKeyVS`, the
result is ordered lexicographically by:

1. the number of one bits in the magnitude of the integer; and
2. the integer's decimal value.

The K entry theorem covers every arbitrary finite list of K `Int` values,
including the empty list and negative integers.  It is not a collection of
fixed-size claims.  It also proves that the caller-owned input list is
unchanged, that two fresh output lists are allocated, that the second is
returned, and that the modeled execution finishes with `NoExc`, an empty call
stack, and the expected scopes.

The prose in `prompt.py` says "non-negative integers", but an example supplies
negative integers.  The theorem covers both.  The displayed example outputs
are ordinary numeric sorts and conflict with the stated popcount ordering
(for example, the prose requires `[1, 2, 4, 3, 5]`, not
`[1, 2, 3, 4, 5]`).  The implementation and theorem follow the stated
popcount property; the inconsistent displayed outputs are not claimed.

This is a partial-correctness result.  It does not separately prove a resource
bound or CPython termination.

## Formal claims

`SPEC.sort-array` starts with the exact translated `sort_array` definition and
an arbitrary `VS:ValSeq` at caller-owned heap location 0, under
`allIntVS(VS)`.  Its post-state is:

```k
<k> ref(2) </k>
<heap>
  0 |-> list(VS)
  1 |-> list(sortVS(VS))
  2 |-> list(sortKeyVS(sortVS(VS), EXACT-KEY-CLOSURE))
</heap>
<heapLoc> 3 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
```

`EXACT-KEY-CLOSURE` in `spec.k` is the complete K closure value for the source
lambda `lambda value: bin(value).count("1")`; it is not a fresh oracle.

`SPEC.key-nonnegative` and `SPEC.key-negative` execute that exact lambda from
its exact call expression and fixed builtin environment.  Their guards
`I >=Int 0` and `I <Int 0` are disjoint and exhaustive over `Int`.  Both prove
that the result is `popcountAbs(I)`, which is defined from the supplied
`binCodes` and `cntSub` functions.

## Proof-extension inventory

### `allIntVS`

- **Class:** Definitional summary.
- **Semantic role:** States the input domain; it does not replace a program
  step.
- **Domain and guards:** Every `ValSeq`.  The `.ValSeq` and `vCons` equations
  are structurally disjoint and exhaustive.
- **Matched context / justification scope / containment:** Only pure terms
  `allIntVS(VS)` are matched, exactly over the equation domain.  No
  continuation, binding, control stack, or state cell is matched or omitted.
- **State footprint:** None.
- **Value influence:** It restricts `SPEC.sort-array` to integer elements.
- **Value justification:** Structural recursion using K's generated
  `isInt`; recursion strictly descends to the tail.
- **Dependents:** `SPEC.sort-array`.
- **Control and value validation:** The ground witness
  `vCons(3, .ValSeq)` satisfies it; the full symbolic claim closes.

### `popcountAbs`

- **Class:** Definitional summary.
- **Semantic role:** Names the fixed semantics' value for counting code point
  49 in the magnitude's binary digits; it never rewrites source execution.
- **Domain and guards:** Every `Int`, split into `I >=Int 0` and `I <Int 0`.
  The guards are disjoint and exhaustive, and both right-hand sides are true
  on their complete guards.
- **Matched context / justification scope / containment:** Only pure
  `popcountAbs(I)` terms.  There is no continuation or operational cell.
- **State footprint:** None.
- **Value influence:** It constrains the auxiliary key claims and supplies the
  execution-to-intent connection for the sort key.
- **Value justification:** The nonnegative equation is
  `cntSub(binCodes(I), "1")`; the negative equation uses `binCodes(0 -Int I)`.
  These are exactly the fixed `bin` rules after their sign prefixes, which
  contain no `1`.
- **Dependents:** `SPEC.key-nonnegative`, `SPEC.key-negative`, and the
  conditional intent argument for `SPEC.sort-array`.
- **Control and value validation:** Both universal connection claims print
  `#Top`.  The arithmetic differential oracle independently checks the value
  computation on all tested inputs.

### `SPEC.key-nonnegative` and `SPEC.key-negative`

- **Class:** Derived lemmas and exact auxiliary execution theorems.
- **Semantic role:** Execute the program-defined lambda; they are claims, not
  rewrite rules and do not accelerate the target execution.
- **Domain:** All integers, by the two exhaustive sign guards.
- **Matched context:** The complete `Call(Lambda(...), Int(I))` computation,
  environment 0, exact module and builtin scopes, scope location 1, empty
  heap and stack, `noRet`, `NoExc`, and exit code 0.
- **Justification scope / containment:** The claims establish precisely the
  contexts they state; no wildcard continuation or framed cell broadens them.
- **State footprint:** The fixed call rules create and pop a temporary call
  frame.  The stated final environment, scopes, scope location, heap, stack,
  return state, exception, and exit code equal their initial values.
- **Value influence:** They prove the exact key value passed by the program to
  the supplied keyed-sort contract.
- **Value justification:** Symbolic execution of the exact lambda body through
  fixed lookup, call, `bin`, attribute binding, and string `count` rules.
- **Dependents:** The Gate B interpretation of `SPEC.sort-array`.
- **Validation:** Each focused run and the all-claims run print `#Top`.

There are no proof-local operational bridges, simplification rules, priority
rules, opaque fresh functions, or trusted axioms in `verification.k`.
`SPEC.sort-array` is the target theorem rather than an extension used to close
it.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

It exited 0.  `prove.sh` contains the following material commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual positive results:

- Both translator commands exited 0.
- `python3 differential_test.py` exited 0 and printed:

  ```text
  DIFFERENTIAL_CASES=9389
  MISMATCHES=0
  ```

- LLVM `kompile` exited 0.  It printed only warnings originating in the
  supplied semantics.
- `krun` exited 0.  Its final configuration had `.K`, `NoExc`, and exit code
  0; all 20 assertions in `smoke.py` were therefore discharged.
- Haskell `kompile` exited 0.  Its warnings were the supplied `str.k` unused
  variables `As` and `Bs`.
- The all-claims `kprove` command exited 0 and printed:

  ```text
  #Top
  ```

Focused construction runs also produced `#Top` with exit 0 for
`SPEC.key-nonnegative`, `SPEC.key-negative`, and `SPEC.sort-array`.

The A5 false-result probe is:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`; the residual had `ref(2)` while the
mutated destination required `ref(1)`.  `prove.sh` recorded:

```text
EXPECTED_FAILURE: false result mutation was rejected
```

The body-sensitivity probe is:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited 1 with `WarnStuckClaimState`; after changing the body to
`return arr`, the residual had `ref(0)` while the original destination required
`ref(2)`.  `prove.sh` recorded:

```text
EXPECTED_FAILURE: changed function body invalidated the target result
```

## Gate results

### Gate A — PASS

- The exact module, function body, argument, lambda body, bindings, evaluation
  order, allocation, return, scope cleanup, heap, control stack, exception
  cell, and exit code are present in the claims.
- The program-defined `sort_array` body executes under the fixed semantics.
- The program-defined key lambda has bridge-free universal execution claims
  for all integers.
- The only proof-local functions are truthful, guarded, terminating
  definitional summaries.  No proof-local rule skips execution.
- The precondition has concrete witnesses.  The false result and changed-body
  mutations both fail with the expected residuals.

### Gate B — PASS

- The theorem covers arbitrary finite integer lists, not bounded sizes.
- This contains the prompt's stated nonnegative domain and also covers its
  negative example.
- The exact key computation is universally connected to the fixed semantics.
- The remaining ordering/permutation conclusion is precisely the contract of
  the named `sortVS` and `sortKeyVS` primitives intentionally supplied as
  opaque to symbolic proof.  Under the shared contract, supplied-primitive
  opacity is a trust boundary, not domain narrowing.
- The inconsistent displayed outputs in `prompt.py` are explicitly reported;
  the theorem follows the unambiguous popcount prose.

### Gate C — PASS

- Every proof-local extension and every imported opaque primitive influencing
  the result is listed below.
- Every claimed command, mutation, and differential test has an existing
  artifact, exact command, scope, oracle, and observed result.
- Formal facts, conditional conclusions, finite evidence, and excluded
  behavior are separated.

## Trust boundary

| Component | Status and effect | Dependents | Evidence |
|---|---|---|---|
| Supplied MPY semantics | Fixed trusted execution model for Python AST constructors, lookup, calls, integers, strings, heaps, and control. It affects all formal conclusions. | All claims | Exact LLVM/Haskell builds and concrete/symbolic runs in `prove.sh`. |
| `sortVS` in `reference-semantics/semantics/sort.k` | Supplied trusted primitive. Symbolically opaque; its documented contract is a new ascending numeric permutation. It affects the result value and assumes normal sort control/termination. Its target domain here is exactly integer sequences, guarded by `allIntVS`. | `SPEC.sort-array` and the human ordering conclusion | 20 concrete K cases plus 9,389 CPython/oracle cases. |
| `sortKeyVS` in `reference-semantics/semantics/sort.k` | Supplied trusted primitive. Symbolically opaque; its documented contract is a stable ascending sort by real calls to the exact key closure. It affects result value and assumes the key calls and sort complete normally. | `SPEC.sort-array` and the human ordering conclusion | Universal key execution claims, 20 concrete K cases, and 9,389 CPython/oracle cases. |
| `binCodes` and `cntSub` | Executed fixed-semantics functions, not opaque proof extensions. Their correspondence to Python binary formatting and string counting is part of the fixed-model trust boundary. | The key claims and `popcountAbs` interpretation | Both universal key claims, concrete K cases, and the independent arithmetic oracle. |

The unconditional machine-checked statement is that execution returns the
exact `sortKeyVS(sortVS(VS), EXACT-KEY-CLOSURE)` term and the stated final
configuration.  The statement that this term is the correctly ordered
permutation is conditional on the two supplied sort contracts above.

## Empirically supported facts

`differential_test.py` uses an independent oracle: it counts bits by repeated
`divmod(abs(value), 2)` and manually insertion-sorts by
`(arithmetic_popcount(value), value)`.  It does not use `bin`, string `count`,
the solution's two-pass sort, or the K summary equations.

Its 9,389 cases comprise:

- 8 boundary and task-shaped cases;
- every list of length 0 through 4 over
  `{-4,-3,-2,-1,0,1,2,3,4}` (7,381 cases); and
- 2,000 deterministic random lists of length 0 through 20 with values from
  `-10^12` through `10^12`.

It found zero mismatches.  `smoke.py` separately exercises 20 concrete K cases,
including empty, duplicate, zero, positive, negative, power-of-two, mixed-sign,
and large-integer inputs.  These finite results support the trust boundary;
they do not replace the universal K claims or prove the supplied opaque sort
contracts.

## Excluded behavior

- Lists containing non-integer elements and non-list arguments are outside the
  HumanEval integer-array contract and the formal precondition.
- The erroneous ordinary-sort outputs displayed in `prompt.py` are not the
  selected property because they contradict its popcount prose.
- CPython resource exhaustion, implementation complexity, and total
  termination are not established by this partial-correctness proof.
- Correctness of the supplied opaque sort primitives is conditional as stated
  in the trust ledger; it is not re-proved by K in this task.
