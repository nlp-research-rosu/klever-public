SOUND-BUT-LIMITED

## What is proven

Under the supplied `MPY` semantics, for every finite `ValSeq` containing at
least two `Float` values and only `Float` values thereafter,
`find_closest_elements` executes its real translated body and returns the exact
two-component scan summary stated in `spec.k`.

The summary enumerates every pair of distinct positions (`i < j`), replaces the
accumulator only when the candidate's opaque float distance is strictly
smaller, and normalizes a selected pair through the same opaque float ordering
used by the program. The entry claim also constrains module binding, the two
list allocations, heap counter, stack, return cell, exception cell, and exit
code. This is a partial-correctness result; termination is not a theorem of the
reachability claims.

## Formal claim

Let:

- `VS = vCons(F0, vCons(F1, REST))`;
- `E = enumVS(VS, 0)`;
- `A0 = orderedFirst(F0, F1)`;
- `B0 = orderedSecond(F0, F1)`.

The `SPEC.find-closest` claim proves that the exact invocation loaded from
`solutionModule` reaches:

```k
tuple(vCons(
  outerFirst(E, E, A0, B0),
  vCons(outerSecond(E, E, A0, B0), .ValSeq)))
```

when `allFloatVS(REST)` holds. `SPEC.inner-loop` and `SPEC.outer-loop` are the
two loop circularities. `CONNECTION-SPEC.inner-loop-connection` proves the
inner-loop summary without importing the operational bridge.

## Proof-extension inventory

| Extension | Class and domain | Context/state/value justification | Dependents and validation |
|---|---|---|---|
| `innerBody`, `outerBody`, `findBody`, `solutionModule` | Definitional syntax summaries over their fixed, argument-free forms | Macro expansion only; no execution is replaced. The expanded `solutionModule` matches `solution.mpy`. | All claims. `python3 py2mpy.py solution.py \| diff -u solution.mpy -` produced no output and exited 0. |
| `allFloatVS`, `floatProjection`, `allFloatItems`, `itemIndex`, `itemFloat` | Definitional domain/projection functions | `allFloatVS` requires every value to equal a `Float` projection. `allFloatItems` requires every value to equal a canonical `(Int, Float)` tuple. Projection values are fixed by equations on those guarded domains; off-domain values do not reach a result-bearing use. | Preconditions, index lemmas, scan summaries. Base/cons cases are exhaustive; recursion descends structurally. |
| `allFloatItems(enumVS(VS, I)) => true requires allFloatVS(VS)` | Derived simplification lemma | Guard is exactly the homogeneous-float domain. Structural induction on `VS` gives canonical `(index, float)` entries. It neither rewrites a `<k>` computation nor changes state. | Entry-to-outer-loop handoff. The rule was narrowed during Gate A audit; no off-domain equation is asserted. |
| Guarded `applyIndex(V, 0/1)` simplifications | Derived lemmas | Guard requires `V ==K tuple(vCons(itemIndex(V), vCons(itemFloat(V), .ValSeq)))`; fixed `applyIndex` therefore returns those exact components. No continuation or state is skipped. | Loop execution. `PROJECTION-SPEC` imports only `MPY`; both fixed-semantics claims returned `#Top`. |
| `orderedFirst`, `orderedSecond`, `candidateWins`, `stepFirst`, `stepSecond` | Definitional summaries | The true/false `floatLt` guards and winner/non-winner cases are exhaustive and disjoint. Equations mirror the three nested source `if` statements. | Both loop summaries and the entry result. Values affect branches and the result, and are fixed by these exhaustive equations plus the named reference float primitives. |
| `innerFirst`, `innerSecond`, `outerFirst`, `outerSecond`, `lastItem` | Definitional structural folds | Empty/cons equations are exhaustive, disjoint, and strictly descend through `ValSeq`. They summarize values after fixed loop execution and do not rewrite program terms. | Loop claims, entry claim, and bridge connection theorem. |
| Priority-40 inner `#loop` rule in `VERIFICATION` | Operational bridge | Complete match pins the exact body, target, environment `1`, builtins frame, module binding/body, local bindings, canonical outer item, float-item remainder, and arbitrary continuation frame. It reads those cells, writes only `item2` and `closest`, and preserves all omitted/framed cells and the continuation. | Outer and entry claims. The identical-domain connection theorem is proved in `VERIFICATION-BASE`, which has no bridge. The empty-body mutation is rejected with `WarnStuckClaimState`, exit 1. |

There are no proof-local trusted primitives and no result-bearing program
oracle. `floatProjection`, `itemIndex`, and `itemFloat` are arbitrary only
outside their canonical equality guards; no target conclusion depends on an
off-domain interpretation.

## Commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final
end-to-end run was:

```bash
./prove.sh
```

It exited 0. Its positive proof commands and actual success outputs were:

```text
kprove projection-spec.k --definition fixed-kompiled --spec-module PROJECTION-SPEC
#Top
exit 0

kprove connection-spec.k --definition connection-kompiled --spec-module CONNECTION-SPEC
#Top
exit 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
#Top
exit 0
```

The projection run also printed `WarnTrivialClaim`, because fixed-semantics
function simplification establishes both equations before a reachability step.
Compiler warnings came only from supplied reference files or unused framed
variables; no compiler command failed.

Concrete execution used the required LLVM build:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual final cells included:

```text
<k>
  .K
</k>
<exit-code>
  0
</exit-code>
```

Both negative probes behaved as expected:

```text
kprove connection-mutation-spec.k ... --spec-module CONNECTION-MUTATION-SPEC
WarnStuckClaimState
exit 1
EXPECTED FAILURE: the inner-body mutation was rejected

kprove spec-vacuity.k ... --spec-module SPEC-VACUITY
WarnStuckClaimState
exit 1
EXPECTED FAILURE: the false result-shape mutation was rejected
```

The second mutation requires a three-element result from a real length-two
invocation; the actual residual is a two-element tuple.

## Gate results

### Gate A — PASS

- A1: The entry claim loads the exact generated body and resolves the actual
  module binding. The only operational bridge has a bridge-free universal
  connection theorem. Replacing its body with `.Stmts` makes that theorem fail.
- A2: The bridge's connection theorem covers `item2`, `closest`, continuation,
  bindings, and every framed configuration cell. No exception, heap, stack,
  output, return, or control effect is discarded.
- A3: The complete environment, builtins namespace, closure binding/body,
  target, loop body, continuation, and local scope are pinned. The bridge and
  connection theorem accept the same context.
- A4: Total functions have exhaustive constructor or complementary Boolean
  cases. Recursive equations descend. The only off-domain recognizer lemma was
  removed and replaced with the guarded true direction.
- A5: Length-two float lists realize the entry precondition. The false
  three-element result mutation fails with a stuck result residual.

### Gate B — FAIL

- B1: The formal domain aligns with `List[float]` of length at least two.
- B2/B3: Symbolic `subF`, `absF`, and `floatLt` are intentionally opaque in the
  supplied Haskell semantics. K proves the exact exhaustive scan in terms of
  those primitives, but `spec.k` does not separately formalize and prove an
  order-theoretic global-minimum predicate or Python/K equivalence for special
  IEEE values such as NaN. The human-facing "closest" conclusion is therefore
  conditional on the named float contracts and empirically supported, not a
  fully formal consequence inside K.
- B4: For ordinary finite floats, the implementation, examples, and independent
  oracle agree. No implementation/specification discrepancy was observed.

This Gate B limitation determines the `SOUND-BUT-LIMITED` headline.

### Gate C — PASS

Every unproved primitive and all evidence are listed below with artifacts,
commands, scope, oracle, and actual outcome. Formal, conditional, empirical,
and excluded conclusions are separated in this report.

## Trust boundary

| Component | Effect and dependents | Status/evidence |
|---|---|---|
| Reference `subF(Float, Float)` | Produces candidate/current distances; affects `candidateWins`, both folds, and final result | Fixed external primitive, opaque to Haskell and concrete under LLVM. Covered on finite witnesses by `smoke.py`/`krun` and the CPython differential suite. |
| Reference `absF(Float)` | Produces absolute distances; affects the same claims | Same conditional trust boundary and evidence. |
| Reference `floatLt(Float, Float)` | Selects smaller-first order and winning candidates; affects control and result | Same conditional trust boundary and evidence. No total-order law for NaN is assumed in K. |
| Supplied `MPY` rules, K backend, and SMT engine | Defines and checks all execution/proof steps | Foundational toolchain/semantics trust. The reference files were not modified. |

The inner-loop operational bridge is not a trust assumption: its complete
domain is connected to fixed execution by a separate `#Top` theorem.

## Empirical evidence

`smoke.py` contains the two prompt examples plus negative/unsorted and
descending two-element cases. The command:

```bash
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

uses the supplied LLVM semantics as the executable oracle; all assertions were
consumed, final `<k>` was `.K`, and `<exit-code>` was `0`.

`differential_test.py` uses `itertools.combinations`, independently computes
the minimum absolute pair distance, checks multiplicity through distinct
positions, and checks smaller-first ordering. It covers six fixed boundary and
prompt cases plus 1000 seeded random finite lists of lengths 2 through 8:

```text
python3 differential_test.py
cases=1006 mismatches=0
```

Finite evidence supports the float-contract adequacy bridge; it is not used as
a universal proof.

## Excluded behavior

- Lists shorter than two and lists containing non-`Float` values.
- Exceptions and out-of-bounds behavior outside the stated precondition.
- A formal total-correctness/termination theorem.
- A K-internal theorem that the fold result minimizes mathematical distance
  independently of the supplied opaque float contracts.
- A Python/K adequacy claim for NaN or other special IEEE edge behavior.
