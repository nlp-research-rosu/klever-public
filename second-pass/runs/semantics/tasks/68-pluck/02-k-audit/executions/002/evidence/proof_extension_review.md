# Proof-extension review

## `asInt` and the iterator specialization

- `asInt(Val) : Int [function,total]` has the sole equation
  `asInt(I:Int) => I`. It is the identity on every source-contract element.
  The `total` declaration is broader than its equations; a non-Int argument
  may remain irreducible, but `allNonNegative` excludes every ground non-Int
  list element.
- The sole operational extension matches
  `#iterNext(list(vCons(V,REST)))` under `isInt(V)`, preserves an arbitrary
  continuation and every omitted cell, and yields
  `#iterYield(asInt(V),list(REST))`.
- It overlaps the fixed `list.k:10` rule. Priority 40 makes the extension win;
  the fixed rule otherwise yields `V` with the identical remainder and state
  footprint.
- The bridge-free typed connection theorem
  `AUDIT-ITER-CONNECTION-SPEC.fixed-list-iter-int-domain` imports only `MPY`
  plus a separate identity cast and proves `#Top` for arbitrary `I:Int`,
  `REST`, and continuation `K`.
- The broader syntactic theorem with `V:Val requires isInt(V)` does not close:
  the K backend does not derive `V = auditAsInt(V)` merely from its generated
  sort predicate. This is an auditability limitation in the symbolic encoding,
  not a concrete false witness: every ground value satisfying `isInt` on the
  source-contract domain is an `Int`, and the typed universal theorem closes.
- The cast is result-bearing and appears in both execution and `scanPluck`.
  Ground opposite interpretations are unavailable because `asInt(I)` rewrites
  to `I` for every intended element. The fresh false-postcondition test checks
  separately that this shared symbol does not make an incorrect concrete
  result provable.

State footprint: only `<k>` is rewritten. No scopes, environment, heap,
allocation counter, stack, return state, exception, or exit cell is read or
changed.

## Definitional summaries

| Extension | Domain / coverage | Overlap and descent | Decision |
|---|---|---|---|
| `pluckTake(V,B)` | All Int pairs | One unconditional mathematical equation; unused by claims | Truthful but unused |
| `nextBest(V,B)` | All Int pairs relevant to divisor 2 | Four disjoint cases: odd; even/sentinel; even/non-sentinel/smaller; even/non-sentinel/not-smaller. Integer parity and order make them exhaustive. | Truthful |
| `nextBestIndex(V,B,BI,I)` | Same | Guards partition identically to `nextBest`; update cases return `I`, others preserve `BI`. | Truthful |
| `pstate`, `scanPluck` | Finite `ValSeq`; intended uses have Int elements | Empty base; nonempty rule removes one constructor and applies the two state transitions, increments index, records last value. | Truthful structural fold on formal domain |
| `stateBest`, `stateBestIndex`, `stateIndex`, `stateLast` | Constructed `pstate` values | Constructor projections are disjoint by symbol and total after `scanPluck` reaches its base. | Truthful |
| `pluckResult(VS)` | `allNonNegative(VS)` entry domain | `best == -1` and `best != -1` are disjoint/exhaustive. Nonnegativity makes `-1` an unambiguous “no even” sentinel. | Truthful |
| `allNonNegative(VS)` | All finite `ValSeq` | Empty base and one-constructor descent. It requires both K Int sort membership and value `>= 0` for each element. | Exact source-contract domain predicate |

There are no proof-local simplification rules, `functional` declarations,
opaque/no-evaluator symbols, claims masquerading as rules, call interceptions,
return shortcuts, allocation shortcuts, or task-answer axioms.

## Claim dependencies

- `pluck-loop` executes the exact real loop head for an arbitrary current
  state and tail, then equates every modified local to the structural fold.
  It depends on the fixed semantics, the iterator specialization, and the
  definitional summaries.
- `pluck-correct` executes module loading, exact function lookup/binding, the
  exact submitted body, output allocation, and call return. Its modular proof
  trusts only `pluck-loop`, which was separately proved in a command that did
  not trust it.
- `pluckResult` constrains both the returned list contents and the heap object
  referenced by the return value; it is not a free result variable or a
  one-way implication.
