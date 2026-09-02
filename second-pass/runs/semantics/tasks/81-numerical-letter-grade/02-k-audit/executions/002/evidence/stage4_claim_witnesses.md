# Entry claims, preconditions, and satisfying witnesses

This is reviewer-authored accounting; it does not treat the candidate prose as
authority.

| Claim | Plain-language precondition | Plain-language postcondition | Satisfying witness and concrete comparison |
|---|---|---|---|
| `empty` | Exact fresh module state; `runGrades` receives the real empty `ValSeq`. | Returns fresh `ref(0)` whose heap value is the empty list. | `grades=[]`. Trusted canonical and candidate Python both return `[]`; the Stage 6 witness records this. |
| `a-plus` | Exact fresh module state; one real Float element `F`; path condition `eqFour(F)`. | Returns `["A+"]`. | Model/witness `F=4.0`, `gpaEqFour(4.0)=true`. Both Python functions return `["A+"]`. The interpretation is satisfiable but candidate-local; the proof does not establish that it is actual float equality. |
| `a` | Exact fresh module state; one real Float element `F`; `not eqFour(F)` and `above(F,3.7)`. | Returns `["A"]`. | Model/witness `F=3.9`, `gpaEqFour(3.9)=false`, `gtF(3.9,3.7)=true`. Both Python functions return `["A"]`. |
| `function-maps-all-numeric-grades` | Exact fresh module state; input is the proof-local `list(numericValues(GS))` for an arbitrary inductive `NumericGrades`. | Returns a fresh list whose elements are `mappedAppend(.ValSeq,GS)`. | `GS=.NumericGrades` is an immediate ground witness and yields `[]`. `GS=fGrade(3.9,iGrade(3,.NumericGrades))`, with the intended primitive interpretation, summarizes `["A","B"]`, equal to both Python functions on `[3.9,3]`; however its K input is not the fixed-semantics real list term `vCons(3.9,vCons(3,.ValSeq))`. |
| `loop-maps-all-numeric-grades` | A live real loop control configuration over proof-local `numericValues(GS)`, scope 1 with the required bindings, heap accumulator `list(PREFIX)`, and `0` absent from framed `HP`. | Preserves the continuation, updates the accumulator with `mappedAppend(PREFIX,GS)`, and updates `grade` to the final converted element (or retains `OLD` for empty input). | `GS=.NumericGrades`, `PREFIX=.ValSeq`, `HP=.Map`, `OLD=0.0`, `INPUT=list(.ValSeq)`, `CONT=.K` satisfies it. A nonempty model with prefix `["E"]` and `GS=fGrade(4.0,.NumericGrades)` summarizes `["E","A+"]`, matching one real loop iteration under the intended equality interpretation. |

The first three preconditions use actual fixed-semantics `ValSeq` constructors.
The arbitrary-length entry and loop preconditions instead use a new candidate
constructor, `numericValues`; no bridge-free reachability theorem relates that
constructor to the real recursive `vCons` representation.
