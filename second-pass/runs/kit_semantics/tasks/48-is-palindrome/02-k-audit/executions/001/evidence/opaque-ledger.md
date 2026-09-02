# Opaque and under-specified fixed-semantics symbols

This ledger is reconstructed from the immutable supplied semantics, not from
candidate prose. None of these symbols occurs in `solution.mpy`, the target
claim's executed function body, or its result expression unless explicitly
noted.

## Explicit `[no-evaluators]` symbols

Every declaration below is a fixed-semantics opaque symbol in the Haskell proof
domain. Each is classified `NOT REACHED / NOT RELIED UPON` for HumanEval 48:

| File | Symbol |
|---|---|
| `semantics/float.k` | `intFloatDiv` |
| `semantics/float.k` | `divII` |
| `semantics/float.k` | `floatMod` |
| `semantics/float.k` | `floatLt` |
| `semantics/float.k` | `absF` |
| `semantics/float.k` | `subF` |
| `semantics/float.k` | `divF` |
| `semantics/float.k` | `addF` |
| `semantics/float.k` | `mulF` |
| `semantics/float.k` | `powF` |
| `semantics/float.k` | `gtF` |
| `semantics/float.k` | `eqF` |
| `semantics/float.k` | `decStrToF` |
| `semantics/float.k` | `divFloatIntV` |
| `semantics/float.k` | `intToF` |
| `semantics/float.k` | `truncF` |
| `semantics/float.k` | `roundF` |
| `semantics/float.k` | `roundFN` |
| `semantics/float.k` | `sqrtF` |
| `semantics/sort.k` | `sortVS` |
| `semantics/sort.k` | `sortKeyVS` |
| `semantics/builtins.k` | `md5hexCodes` |

## Constructor-equational symbols that can remain abstract

| Symbol | Static decision |
|---|---|
| `strLt` | Constructor equations implement lexicographic order, but an unconstrained symbolic sequence can remain an abstract total term. Not reached by this program, which uses equality only. |
| `valSeqAt` | Marked total although only nonnegative in-bounds constructor cases have equations; the compiler reports non-exhaustiveness. Not reached because the target slices `IntSeq`, not `ValSeq`. |
| `mapStrVS`, `joinCodes` | Marked total with compiler-reported uncovered internal `cellsMark` cases. Not reached. |
| `floorFI`, `toF`, `ceilF` | Marked total with compiler-reported uncovered internal `cellsMark` cases and concrete-only equations. Not reached. |

## Target-reached partial dispatch

`applyUn`, `applyCmp`, `doSlice`, `slStart`, `slStop`, `intSeqAt`, and
`buildIS` are not unconstrained result oracles on the target path. Their exact
target cases are selected by the constructors/operators `("-", Int)`,
`("==", str, str)`, `(str, noB, noB, someB(-1))`, and the in-bounds indices
generated from `isLen(S)-1` down to zero. The applicable equations are
disjoint, descending, and determine the result.

## Proof-local result

`verification.k` adds no symbol or rule at all. Therefore no opaque result
introduced by the candidate can influence control, state, or the
postcondition.
