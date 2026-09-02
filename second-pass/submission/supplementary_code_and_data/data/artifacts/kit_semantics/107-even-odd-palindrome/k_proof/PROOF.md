VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every mathematical integer `N` with
`1 <= N <= 1000`, applying the exact translated
`even_odd_palindrome` closure to `Int(N)` reaches a two-element tuple containing
the number of even and odd positive decimal palindromes not exceeding `N`,
respectively.

This is a partial-correctness result in the Kit sense. The implementation has no
loops or recursion: every call follows at most seven integer comparisons to a
constant return.

## Formal claim

`spec.k` contains 108 disjoint reachability claims. There is one claim for each
interval beginning at a palindrome and ending immediately before the next
palindrome; the last interval is `999..1000`. Their union is exactly
`1..1000`.

Each claim starts with:

```k
<k> Call(solutionClosure(), Int(N)) => EXPECTED-TUPLE </k>
```

It also pins the initial and final environment, scope store, scope allocator,
heap, heap allocator, call stack, return state, exception state, and exit code.
The function call, parameter binding, comparisons, branches, tuple creation,
return, and frame restoration all execute using the unchanged supplied
semantics.

The intended count table follows from the complete characterization, within the
formal domain, of positive decimal palindromes:

- `1..9`;
- `11*a` for `1 <= a <= 9`;
- `100*a + 10*b + a` for `1 <= a <= 9` and `0 <= b <= 9`.

The parity of a two-digit palindrome is the parity of `a`; the parity of a
three-digit palindrome is also the parity of `a`. `1000` is not a palindrome.
Thus the cumulative pair is constant between successive palindrome thresholds,
which is exactly the interval structure stated in `spec.k`.

## Proof-extension inventory

There is exactly one proof-local function/rule in `verification.k`.

| Field | Record |
|---|---|
| Extension | `solutionClosure()` and its single defining rule |
| Class | Definitional summary |
| Semantic role | Names one exact closure value; it does not replace or accelerate any program execution |
| Domain | The single nullary term `solutionClosure()`; `[total]` is justified by its one exhaustive equation |
| Matched context | In every target claim it occurs only as the callee of `Call(solutionClosure(), Int(N))` in the fully pinned configuration shown in `spec.k` |
| Justification scope | The exact parameters, statement tree, and definition location transliterated from `solution.py` into `solution.mpy` |
| Context containment | The equation merely unfolds to that exact closure value; all call routing, parameter binding, body control, return, and frame restoration remain fixed-semantics steps |
| State footprint | The equation itself reads and writes no cells; subsequent fixed execution uses the cells pinned by each claim |
| Value influence | Selects the exact body whose constant tuple leaf becomes the result |
| Value justification | Its exhaustive equation fully fixes the closure value; regeneration from `solution.mpy` and the rejected body mutation validate identity and sensitivity |
| Justification | Mechanical extraction from the exact translator output; no opaque value or oracle occurs in execution |
| Dependents | All 108 claims in `SPEC` |
| Control validation | No operational bridge exists. LLVM smoke execution terminates with `.K`, `NoExc`, and exit code 0 |
| Value validation | Translator identity check passes; changing the `N=1` body leaf from `(0,1)` to `(9,9)` makes the original result claim fail |
| Validation | Gate A body mutation, false-result mutation, concrete smoke cases, exhaustive independent oracle, and direct actual-spec audit all pass |

The 108 reachability claims are theorem statements, not rules used to bypass
execution. There are no proof-local simplification rules, priority rules,
operational bridges, trusted primitives, opaque symbols, or auxiliary
circularities.

## Exact commands and actual outputs

The complete reproducible sequence is in `prove.sh`. The important commands
actually run were:

```bash
python3 generate_artifacts.py solution
python3 py2mpy.py solution.py > solution.mpy
python3 generate_artifacts.py k
```

All exited 0. The translator identity check was:

```bash
python3 py2mpy.py solution.py > /tmp/solution-check.mpy &&
cmp -s solution.mpy /tmp/solution-check.mpy &&
echo 'solution.mpy matches translator output'
```

Actual output and exit:

```text
solution.mpy matches translator output
Exit: 0
```

Concrete definition and execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 generate_artifacts.py smoke
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

All exited 0. `kompile` printed only warnings originating in the supplied
semantics. The final `krun` configuration contained:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The smoke artifact checks inputs
`1, 3, 9, 10, 11, 12, 99, 100, 101, 202, 999, 1000`.

Independent implementation differential:

```bash
python3 validate.py
```

Actual output and exit:

```text
inputs_checked=1000
mismatches=0
Exit: 0
```

`validate.py` uses arithmetic digit reversal and exhaustive enumeration; it
does not use the decision thresholds or K claims.

Direct audit of the actual K claims:

```bash
python3 audit_spec.py
```

Actual output and exit:

```text
claims_checked=108
domain_covered=1..1000
target_mismatches=0
Exit: 0
```

Symbolic definition and positive target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof output and exits:

```text
kompile: Exit 0 (only supplied-semantics unused-variable warnings)
#Top
kprove: Exit 0
```

False-result/non-vacuity mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
Exit: 1
WarnStuckClaimState
actual <k>: tuple(vCons(0, vCons(1, .ValSeq)))
mutated target: tuple(vCons(1, vCons(1, .ValSeq)))
```

Body-sensitivity mutation:

```bash
python3 generate_artifacts.py mutation
kompile --backend haskell verification-mutation.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutation-kompiled
kprove spec-body-mutation.k \
  --definition verification-mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result:

```text
mutation kompile: Exit 0
kprove: Exit 1
WarnStuckClaimState
actual <k>: tuple(vCons(9, vCons(9, .ValSeq)))
original target: tuple(vCons(0, vCons(1, .ValSeq)))
```

## Gate results

### Gate A — PASS

- **A1 program identity/body sensitivity:** `solutionClosure()` contains the
  exact translated body. All body operations execute in fixed semantics. The
  material `N=1` return mutation invalidates the original result claim.
- **A2 operational-state preservation:** no execution is skipped. Every
  operational cell exposed by the active semantics is pinned in the claims.
- **A3 binding/evaluation/control fidelity:** the exact closure, literal
  argument, parameter list, definition location, and empty continuation are
  fixed. The supplied call, branch, return, and frame rules execute normally.
- **A4 consistency/rule validity:** the only equation is a nullary, exhaustive,
  non-overlapping closure definition. No false arithmetic lemma or operational
  rewrite is admitted.
- **A5 result constraint/non-vacuity:** all 108 intervals are satisfiable and
  cover `1..1000`; witness `N=1` executes to `(0,1)`. The deliberately false
  `(1,1)` target is rejected with a stuck residual.

### Gate B — PASS

- **B1 input domain:** the formal domain exactly matches the prompt's
  `1 <= n <= 10^3` integer restriction.
- **B2 language model:** the program uses only integer comparison, `if`,
  function call/return, and integer tuples, all directly modeled by the supplied
  semantics. K integers and CPython integers are exact on this domain.
- **B3 summary/property:** the interval targets follow from the complete
  one-, two-, and three-digit palindrome characterization above. The separate
  numeric-reversal oracle and actual-spec audit exhaust the finite domain.
- **B4 implementation/intent:** examples `3 -> (1,2)` and `12 -> (4,6)` and
  every other permitted input agree with the independent oracle.

### Gate C — PASS

- Every proof-local extension and dependency is inventoried above.
- Every cited test/mutation artifact exists, and its exact command, domain,
  oracle, output, and exit status are recorded.
- Formal closure, mathematical intent reasoning, finite executable evidence,
  and excluded behavior are kept distinct.

## Trust boundary

- The supplied read-only `reference-semantics/` definition and K toolchain are
  trusted as the execution/proof foundation; no file under that directory was
  modified.
- `py2mpy.py` is the supplied syntax translator. The theorem executes the exact
  term recorded in `solution.mpy`; the reproducible comparison links it to
  `solution.py`.
- `generate_artifacts.py` is construction tooling, not an axiom imported into
  the proof. `kprove` checks the generated `verification.k` and `spec.k`
  directly, and `audit_spec.py` independently checks their stated targets.
- No external primitive, opaque result, or unproved operational summary affects
  the returned value.

## Empirically supported facts

- LLVM execution passed the two prompt examples and ten boundary/transition
  cases with no exception.
- An independently implemented arithmetic digit-reversal oracle found zero
  mismatches over all 1,000 permitted inputs.
- An independent parser audit found exactly 108 disjoint claims, exact coverage
  of `1..1000`, and zero target/oracle mismatches.

These executable checks support identity and intent. They are not used as a
substitute for the positive K reachability proof.

## Excluded behavior

- Inputs below 1, above 1000, non-integers, and Python `bool` values are outside
  the formal claim.
- The theorem begins with the exact closure already selected and a literal
  integer argument. Module import/loading, external name rebinding, and
  side-effecting argument expressions are outside its boundary.
- Behavior requiring Python features absent from the supplied subset is not
  claimed.
- The Kit result is stated as partial correctness; no separate liveness theorem
  is claimed.
