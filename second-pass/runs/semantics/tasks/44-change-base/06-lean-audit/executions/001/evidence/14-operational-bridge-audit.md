# Stage 4/5 operational-bridge audit

## Decisive generated-sort defect

Frozen `reference-semantics/semantics/core.k` line 37 declares:

```k
syntax Scope ::= scope(Map, Parent)
```

It also constructs such values in the initial configuration and call rules.
The deterministic Stage 4 output instead declares at `Sorts.lean` line 7:

```lean
inductive SortScope : Type
```

with no constructors.  Thus generated `SortScope` is empty although the
operational K sort is inhabited.  Target conjuncts 2 and 3 universally
quantify `V : SortScope`; both are therefore vacuous.  This is a mathematical
translation failure despite the exact hashes and bijection.

`Adversarial.lean` was compiled successfully.  In particular:

- `sortScopeIsEmpty` proves `False` from any generated `SortScope`;
- `constantDefinitionsStillProveTarget` proves the exact fixed target using
  constant definitions for all seven target parameters;
- `candidateFreshAcceptsNonScopeValue` exhibits the candidate
  `freshScopes` returning `true` on a map whose value is an integer rather
  than a `Scope`; and
- `candidateConcatAcceptsOverlap` exhibits the candidate `_Map_` accepting
  two bindings with the same key.

The successful compiler result is in
`09-adversarial-vacuity-and-bridge.log`.

## Parameter-by-parameter comparison

| Target parameter | Candidate definition | Frozen operational meaning | Judgment |
|---|---|---|---|
| `_Map_` | Association-list append | K `Map` concatenation is AC disjoint union and is not defined for overlapping keys | Agrees only on a restricted well-formed/disjoint representation; the total overlapping-key behavior is extra and order-sensitive. |
| `_in_keys…` | `List.any` using classical equality | K `MAP.in_keys` membership | Plausible on well-formed association-list encodings, but the target supplies no representation invariant. |
| `_[_<-undef]` | Filter every matching key | K map deletion | Plausible on unique-key encodings; filters duplicates too, which generated `SortMap` permits. |
| `_|->_` | One-entry association list | K singleton map binding | Direct representation is plausible. |
| `Map:update` | Delete key, then prepend binding | K map update | Plausible on well-formed association-list encodings. |
| `freshScopes` | Every integer key is less than `next`; values are ignored | Only the empty equation and exact predecessor recurrence over `(L:Int |-> _:Scope) S`, requiring `next = L + 1` and recursive `freshScopes(L,S)` | Not the frozen definition.  It accepts gaps, arbitrary lower integer keys, and non-`Scope` values.  The compiled non-`Scope` counterexample is direct. |
| `notBool_` | `Bool.not` | K Boolean negation | Exact. |

The direct `freshScopes` counterexample is enough to reject the operational
bridge.  Independently, the compiled constant-definition proof shows that the
generated target cannot enforce any honest implementation of its parameters.
The empty `SortScope` also removes precisely the value witnesses needed by the
two map obligations.
