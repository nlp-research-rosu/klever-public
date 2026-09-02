VALIDATED

# What is proven

Under the supplied MPY semantics, `will_it_fly` is partially correct for every
finite modeled list on which the stated computation returns:

- Any non-palindromic `ValSeq`, with any modeled `w:Val`, returns `false`
  before evaluating `sum(q) <= w`.
- A palindromic list containing only the model's mutually exclusive `Int` and
  `Bool` values, with `w:Int`, returns whether its mathematical integer sum is
  at most `w`.
- A palindromic numeric list containing at least one model `Float`, with
  `w:Float`, returns the fixed semantics' float comparison result. The proof
  is parametric in the supplied opaque float primitives.

The domain is symbolic and unbounded: `VS:ValSeq` denotes every finite
constructor sequence, not a finite set of sizes or examples.

The exact call binding and translated function body execute through
`MPY-CALL` and `MPY-FUNCTIONS`. At completion, the result is constrained, the
function frame is removed, the module and builtins scopes are restored, the
stack and return cells are clear, no exception is present, the exit code is
zero, and the one temporary reverse slice occupies heap location 0.

This is a reachability/partial-correctness result. It does not separately claim
a liveness theorem outside the executions closed by these reachability claims.

# Formal claims

Let:

- `Rev(VS) = reverseSlice(VS)`, definitionally equal to
  `buildVS(VS, vsLen(VS) +Int -1, -1, -1)`;
- `SumI(VS) = sumInts(0, VS)`;
- `SumF(VS) = sumToFloat(0, VS)`.

`spec.k` proves:

1. `SPEC.will-it-fly-balanced`:
   `allIntegral(VS) ∧ ¬hasFloat(VS) ∧ VS ==K Rev(VS)` implies the exact call
   returns `SumI(VS) <=Int W`.
2. `SPEC.will-it-fly-unbalanced`: the same integral domain with
   `VS =/=K Rev(VS)` returns `false`.
3. `SPEC.will-it-fly-float-balanced`:
   `allNumeric(VS) ∧ hasFloat(VS) ∧ ¬allIntegral(VS) ∧ VS ==K Rev(VS)`
   implies the exact call returns `notBool gtF(SumF(VS), W)`, which is the
   supplied rule for float `<=`.
4. `SPEC.will-it-fly-any-unbalanced`: for arbitrary `VS:ValSeq` and `W:Val`,
   `VS =/=K Rev(VS)` implies the exact call returns `false`.

The supporting universal claims are:

- `SUM-CONNECTION.sum-fold`: fixed integer/Boolean `sum` fold equals
  `sumInts`.
- `SUM-CONNECTION.float-rest-fold`: the fixed float-accumulator phase equals
  `sumFloatRest`.
- `SUM-CONNECTION.reverse-summary`: `reverseSlice` names the exact frozen
  `buildVS` term.
- `SUM-CONNECTION.reverse-slice`: the exact fixed slice continuation reaches
  allocation of `reverseSlice`, with an arbitrary continuation.
- `FLOAT-SUM-CONNECTION.float-sum-fold`: the fixed initial integer accumulator,
  including its transition at the first float, equals `sumToFloat`.

# Proof-extension inventory

| Extension | Class and semantic role | Domain, context, and state footprint | Value justification and dependents | Validation |
|---|---|---|---|---|
| `willItFlyClosure()` | Definitional summary of syntax; it does not replace function execution | Nullary, exhaustive equation to the exact `closureVal` body copied from `solution.mpy`; no cells read or written | The target claims bind this value under `"will_it_fly"`; lookup, argument evaluation, frame creation, parameter binding, return, and frame pop remain fixed-semantics steps | `spec-body-mutation.k` changes the body to `return False`; proof exits 1 with residual `false` against required `true` |
| `integralV`, `floatV` | Definitional classifiers | Total equations over `Val`; classifiers explicitly make the K `Int`/`Bool` and `Float` alternatives mutually exclusive | Guard the domain predicates, projections, and sum definitions; they assert only generated-sort membership facts | All universal connection claims close; concrete Int, Bool, and Float tests pass |
| `allIntegral`, `allNumeric`, `hasFloat` | Definitional sequence predicates | Empty/cons equations are exhaustive, disjoint by constructor, and recurse on the strict tail | Define the exact guards of target and connection claims | Target has identical `[concrete, simplification]` equations; `SUMMARY-DEFINITION` adds same-RHS symbolic twins. No overlapping equations disagree |
| `projectIntTotal`, `projectBoolTotal`, `projectFloatTotal`, `intLikeTotal`, cast `#Ceil`/orientation rules, and guarded `intOf` twin | Derived sort-refinement lemmas and guarded total projections | Every projection use is guarded by the exact exclusive value class; orientation rules preserve definedness. Off-domain total values cannot affect a target branch or result | Collapse rules return the original statically sorted value. The `intOf` twin is the union of the supplied `intOf(Int)` and `intOf(Bool)` equations | Integer, Boolean, float-rest, and full-float connection claims all print `#Top` |
| `sumInts` | Definitional accumulator summary | Empty/cons equations cover every `ValSeq` and strictly recurse on the tail; target uses the integral guard | `SUM-CONNECTION.sum-fold` proves the exact fixed recurrent configuration universally | Wrong interpretation `sumInts(_,_) => 0` is rejected on `[1,2]`; residual result is `3` |
| `sumFloatRest`, `sumToFloat` | Definitional accumulator summaries | Exhaustive empty, exclusive integral, exclusive float, and unsupported-value cases; each recursive equation consumes one constructor | `float-rest-fold` is bridge-free. `float-sum-fold` uses only that independently proved lower bridge and the fixed semantics. Values contain the exact supplied `addF`/`intToF` terms | Wrong one-float interpretation is rejected; residual is `addF(intToF(ACC), F)`, not `projectFloatTotal(F)` |
| `noFloatSum` | Off-domain totalizer | Used only by `sumToFloat` on a sequence with no float | Every float target and bridge requires `hasFloat(VS)`, so this symbol has no target value influence | Dependency audit finds no target path to it |
| `reverseSlice` | Definitional reverse-slice summary | Exhaustive equation for every `ValSeq` to the exact supplied `buildVS` call | `reverse-summary` fixes the name; `reverse-slice` executes the fixed slice continuation bridge-free | Wrong interpretation as `.ValSeq` is rejected on `[1,2]`; the residual contains allocation of `[2,1]` |
| `someB(-1) ~> #slStep(list(VS), noB, noB) => #alloc(list(reverseSlice(VS)))` | Operational bridge | Exact active continuation for `q[::-1]`, arbitrary suffix, and the same omitted/framed cells as `reverse-slice`; no binding or control change. It reads/writes no state itself. The subsequent fixed `#alloc` performs the heap and heap-location writes | `SUM-CONNECTION.reverse-slice` proves the same complete match domain without importing this bridge | Universal connection `#Top`; concrete reverse witness `[1,2] -> [2,1]`; wrong-summary mutation rejected |
| `#iterNext(list(VS)) ~> #sumCont(ACC) => sumInts(ACC,VS)` | Operational bridge | Guard `allIntegral(VS) ∧ ¬hasFloat(VS)`; arbitrary suffix and all other cells framed identically. The fixed fold has no external state effects | `sum-fold` proves the broader `allIntegral(VS)` domain bridge-free | Universal connection `#Top`; ground sums `1+2=3` and `-2+1=-1`; wrong interpretation rejected |
| `#iterNext(list(VS)) ~> #sumContF(ACC) => sumFloatRest(ACC,VS)` | Intermediate operational bridge | Guard `allNumeric(VS)`; exact recurrent float continuation, arbitrary suffix, and no state effects | `float-rest-fold` proves the identical domain without this bridge | Bridge-free universal claim `#Top` |
| `#iterNext(list(VS)) ~> #sumCont(ACC) => sumToFloat(ACC,VS)` | Operational bridge | Guard `allNumeric(VS) ∧ hasFloat(VS) ∧ ¬allIntegral(VS)`; exact initial fold continuation, arbitrary suffix, and no state effects | `float-sum-fold` proves the broader numeric/has-float domain using only the independently connected float-rest bridge | Universal connection `#Top`; wrong float-summary mutation rejected; LLVM float cases pass |

The `[concrete, simplification]` summary equations in `VERIFICATION-BASE` fix
their ground interpretation in the target theory without causing unbounded
symbolic unfolding. `SUMMARY-DEFINITION` supplies same-right-hand-side
symbolic twins only for the bridge-free connection builds. Pairwise overlaps
therefore agree.

# Exact commands and actual outputs

The complete recorded runner is:

```bash
./prove.sh
```

Actual result: exit 0.

The positive proof commands executed by that script were:

```bash
kompile --backend haskell verification.k \
  --main-module SUMMARY-DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module SUM-CONNECTION
# Output: #Top
# Exit: 0

kprove connection-witness.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-WITNESS
# Output: #Top
# Exit: 0

kompile --backend haskell verification.k \
  --main-module FLOAT-REST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition float-connection-kompiled
kprove float-connection-spec.k \
  --definition float-connection-kompiled \
  --spec-module FLOAT-SUM-CONNECTION
# Output: #Top
# Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0
```

`SUM-CONNECTION.reverse-summary` emitted `WarnTrivialClaim` because the RHS
normalizes by its exhaustive defining equation. The operational
`reverse-slice` theorem separately executes the fixed slice continuation and
is the bridge justification.

Concrete execution used the required LLVM modules:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual result: exit 0, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The compiler printed only warnings originating
in the supplied read-only semantics.

The validation probes produced:

| Probe | Actual result |
|---|---|
| `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY` | Exit 1; `WarnStuckClaimState`; final result is `true` while mutation requires `false` |
| `kprove spec-body-mutation.k --definition verification-kompiled --spec-module SPEC-BODY-MUTATION` | Exit 1; changed body produces `false` while claim requires `true` |
| `wrong-sum` claim in `spec-summary-mutation.k` | Exit 1; residual fixed result `3` |
| `wrong-float-sum` claim in `spec-summary-mutation.k` | Exit 1; residual fixed result `addF(intToF(ACC), F)` |
| `wrong-reverse` claim in `spec-summary-mutation.k` | Exit 1; residual fixed allocation contains `[2,1]` |

# Gate results

## Gate A — PASS

- A1: the exact binding and exact translated body are present in the initial
  scope and execute under fixed lookup/call/frame/return semantics. The body
  mutation fails.
- A2/A3: every operational bridge has an exact bridge-free connection theorem
  over the same or a broader guard, arbitrary continuation, and identical
  omitted cells. Sum bridges have no external state effects. The reverse
  bridge leaves allocation to the fixed semantics.
- A4: summary equations are exhaustive, recursively descending, and
  pairwise-consistent. Guarded projections are used only on their exact class.
  The three deliberately wrong value interpretations are rejected.
- A5: `q=[3], w=5` realizes the precondition. The false-result mutation exits
  1 with a final `true` result, demonstrating that the target constrains the
  returned Boolean.

## Gate B — PASS

The claims cover unbounded finite sequences, not bounded examples. They cover:

- every modeled non-palindromic list and every modeled capacity value via
  short-circuiting;
- every modeled integral/Boolean palindromic numeric list with an integer
  capacity;
- every modeled float-containing palindromic numeric list with a float
  capacity.

Balanced nonsummable lists are outside the natural contract because the stated
`sum(q) <= w` computation itself is undefined. Mixed-capacity comparisons and
cross-constructor numeric equality are supplied-model boundaries, not
candidate restrictions; they are recorded below with executable witnesses.
Opaque float arithmetic is supplied-primitive opacity, not domain narrowing.

## Gate C — PASS

Every proof-local result-bearing summary has a universal connection theorem,
and every operational bridge is justified before it is imported by a higher
proof layer. Positive, mutation, differential, concrete, and model-boundary
artifacts all exist and are run by `prove.sh`. Formal results, conditional
float facts, finite evidence, and excluded/model-boundary behavior are
separated here.

# Trust boundary

| Trusted component | Influence and dependents | Evidence |
|---|---|---|
| Supplied read-only MPY semantics | Defines Python execution, heap/frame behavior, slicing, list equality, builtins, and calls for all claims | LLVM smoke execution; connection witnesses; source hash `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97` |
| K toolchain and Haskell/LLVM backends | Executes and proves every K artifact | K v7.1.293; all positive commands exit 0 and print `#Top` |
| Supplied opaque float primitives `intToF`, `addF`, and `gtF` | Affect `sumFloatRest`, `sumToFloat`, and the float target result. The K theorem preserves their exact terms and is conditional on their supplied contracts | LLVM float smoke cases and Python differential tests; no proof-local rule assigns their values |

There are no unproved program-derived oracles. `noFloatSum` is an unreachable
off-domain totalizer and does not influence a target result.

# Empirical evidence

```bash
python3 differential_test.py
```

Actual output:

```text
differential: 56971 cases, 0 mismatches
```

The independent oracle checks palindrome by symmetric indexing and computes
the sum with an explicit loop; it does not reuse K summaries. Scope:

- all integer lists of lengths 0 through 5 over `[-2,2]`, with every integer
  capacity from -5 through 5 (42,966 cases);
- all numeric lists of lengths 0 through 4 over
  `[False, True, -1, 0, 1, -0.5, 0.5]`, with capacities
  `[-2, -0.5, 0, 0.5, 2]` (14,005 cases).

`concrete-tests.py` adds all prompt examples, the empty list, negative
integers, Booleans, and homogeneous float cases under LLVM. All nine assertions
pass.

# Model boundaries and excluded behavior

The supplied model intentionally differs from CPython in two relevant places:

1. It compares list element constructors structurally, so `Int(1)` and
   `Bool(true)` are unequal. `python3 model-boundary.py` exits 0, while
   `krun model-boundary.mpy --definition runtime-kompiled` exits 1 with
   `AssertionError` for `[1, True]`.
2. It has no mixed `Int <= Float`, `Float <= Int`, or Boolean-capacity dispatch.
   `python3 model-boundary-comparison.py` exits 0, while the MPY run exits 113
   stuck at `applyCmp("<=", 1, 1.0)`.

These are explicit language-model adequacy boundaries under Gate B2. The
formal theorem covers every value/behavior the fixed semantics supplies and
does not silently assert the missing CPython behavior.

Also excluded are external state, custom user numeric classes, and exception
behavior outside the supplied semantics. Balanced lists whose elements cannot
be summed are outside the contract's defined-return domain; non-palindromic
lists remain covered because the program short-circuits before summation.

Artifact hashes for program identity:

```text
solution.py   4d18ff8e7d6f7f348d0c4d53dbe15aece164952dec1b3d2df00b8205434e42ac
solution.mpy  7c0e0763451ba64ad5a942a7e0cf477e9755446d733bd21ae8221636efd7efa0
```
