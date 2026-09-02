# Static soundness review notes

## Inventory scope and dispositions

The exhaustive mechanical inventory is `05_rule_inventory.md`: 25 supplied
source files plus `verification.k`, `spec.k`, `connection-verification.k`, and
`connection-spec.k`; no compiled artifacts. It records 232 syntax declarations,
705 rules, five contexts, one configuration, and four claims. No `functional`
declaration occurs. There is one `[simplification]` rule, in
`verification.k:21`.

The 705 supplied rules are launcher-trusted fixed semantics, not candidate
extensions. The exact candidate tree is byte/type identical to that baseline.
Forty-three of those fixed rules are on the submitted program/connection route;
they are mapped below. The other 662 have syntactically nonmatching heads
(dicts, sets, strings, ranges, comprehensions, indexing, methods, sorting,
unrelated builtins, heap references, exceptions, and so on) and are unreachable
from the exact entry configuration and empty heap. They therefore cannot help
close this theorem. Their individual source locations and complete guards remain
enumerated in `05_rule_inventory.md`.

The fixed source has 22 `no-evaluators` declarations. Only `subF`, `absF`, and
`floatLt` are reachable here. The other 19 are inert. These three are explicitly
supplied trusted primitives with LLVM `[concrete]` twins; the Haskell proof is
parametric in them and never asserts a particular symbolic comparison outcome.

## Material fixed-semantics route

| Program operation | Declarations and rules | Review |
|---|---|---|
| Module and statement sequencing | `syntax.k:41-61`; `core.k:49-60,124-127` | Exact initial configuration; `#loadAll` exposes the module statements in order. |
| Typing import | `syntax.k:43`; `controls.k:35-36` | The `typing.List` import is discarded. This is inert because translated annotations contain no runtime `List` use. |
| Function definition/binding | `syntax.k:53,57,60`; `functions.k:14-16` | Binds the exact translated parameter list/body as `closureVal` in module scope 0. |
| Name lookup and builtins | `core.k:130-181` (rules at 131, 132, 152, 158) | Local → module → builtins lookup selects the loaded closure and the fixed `abs` builtin. Exact scopes rule out shadowing. |
| Call evaluation and frame creation | `syntax.k:28`; `core.k:185-191,213-215`; `call.k:19-21,31,69-74`; `functions.k:63-66` | Callee and two arguments evaluate left-to-right, parameters bind in a fresh exact frame, then the submitted body executes. |
| Literals | `core.k:194-195`; `float.k:20-21` | Int, Bool, and Float constructors evaluate to their corresponding values. |
| Assignment | `syntax.k:41`; `controls.k:9-11` | Writes only the current plain local scope. Cell-write and reference alternatives cannot match the exact frame/empty heap. |
| `for` control | `syntax.k:45`; `controls.k:65,69,71-74`; `list.k:9-10` | The input is an unboxed read-only `list(ValSeq)`; each loop yields its head, executes the exact body, and recurs on the tail. Empty and cons iterator rules are disjoint. |
| `if` control | `syntax.k:49`; `core.k:199-205` (Bool case 200); `controls.k:51-54` | Conditions evaluate first and the selected branch alone executes. Inputs to each branch are Bool. |
| Integer index arithmetic | `syntax.k:15,30,32`; `operators.k:12,15-17`; `int.k:9,22` | `j + 1`, `i + 1`, and `i < j` use unbounded K Int, matching Python integer behavior here. |
| Float distance atom | `operators.k:12,15-17`; `float.k:50-56,103-105` | Fixed dispatch produces `subF`, then `absF`, then `floatLt`. All are pure and total in the supplied proof model; their LLVM twins use K float hooks. |
| Return and frame pop | `syntax.k:50`; `functions.k:78-90` | The returned `found` becomes the call value, the callee frame is removed, and all explicitly constrained observable cells are restored. |

The strict/seqstrict syntax on assignment, `For`, `If`, `Return`, and `BinOp`,
plus the two explicit `Compare` contexts, preserves the program's evaluation
order. No used operation allocates, mutates the heap, emits output, or raises an
exception on the `allFloats` domain. The entry fixes empty heap/stack, `noRet`,
`NoExc`, and exit code 0 on both sides.

## Proof-local syntax and rules, one by one

| Extension | Class | Complete domain / overlap / descent | Soundness disposition |
|---|---|---|---|
| `allFloats` declaration | Pure total function | All finite `ValSeq` | Legitimate definitional summary. |
| `allFloats(.ValSeq) => true` | Equation | Empty constructor only | True base case. |
| `allFloats(vCons(V,R)) => isFloat(V) andBool allFloats(R)` | Equation | Cons constructor only; structural descent | True recursive definition. Empty/cons rules are disjoint and exhaustive. |
| `pairNear` declaration | Pure total function | Three `Float` arguments | Legitimate abbreviation; it is not actually opaque locally. |
| `pairNear(A,B,T) => floatLt(absF(subF(A,B)),T)` | Equation | Entire declared domain | Exact spelling of the fixed distance comparison; no overlap. |
| `asFloat` declaration | Pure total function | All `Val` | Legitimate sort projection with explicit off-domain totalization. |
| `asFloat(F:Float) => F` | Equation | Float subsort | Identity, true. |
| `asFloat(V:Val) => 0.0 requires notBool isFloat(V)` | Equation | Non-Float values | Arbitrary but truthful definition of a new helper outside the theorem domain. Guard is disjoint from identity case and makes coverage exhaustive. |
| Guarded `applyBin` simplification | Operational bridge | `applyBin("-",A:Val,B:Val)` under `isFloat(A) andBool isFloat(B)`; any pure term context; no cells | Sound sort-elimination bridge. Generated `isFloat` makes every ground valuation a pair of actual Float values; then both `asFloat` calls are identities and fixed `float.k:105` yields the same `subF`. The bridge-free `CONNECTION-SPEC.float-subtraction` theorem imports only MPY, frames an arbitrary continuation with `...`, closes `#Top`, and has no state footprint. No non-Float witness satisfies its guard. |
| `rowAcc` declaration | Pure total function | Bool × Float × Float × Int × Int × finite `ValSeq` | Legitimate mathematical summary. |
| `rowAcc(...,.ValSeq) => B` | Equation | Empty constructor | Exact final accumulator. |
| `rowAcc(...,vCons(V,R)) => ...` | Equation | Cons constructor; descends to `R` | Exact one-step inner-loop update: test only `I < J`, OR the fixed distance atom into `found`, increment `J`. Empty/cons rules are disjoint and exhaustive. |
| `outerAcc` declaration | Pure total function | Bool × finite `ValSeq` × Float × Int × finite `ValSeq` | Legitimate mathematical summary. |
| `outerAcc(...,.ValSeq) => B` | Equation | Empty remaining sequence | Exact final accumulator. |
| `outerAcc(...,vCons(A,R)) => ...` | Equation | Cons constructor; descends to `R` | Exact one-step outer-loop update: reset `j=0`, scan full `VS` with `rowAcc`, increment `i`. Empty/cons rules are disjoint and exhaustive. |

There are no proof-local priority rules, macros, `functional` declarations,
`no-evaluators` symbols, fresh/oracle values, or answer-encoding operational
rewrites. `pairNear`, `rowAcc`, and `outerAcc` influence the postcondition but
are completely equational and structurally recursive.

## Claims

- `inner-loop` executes the exact reachable inner `#loop`. Its precondition says
  `VS` and `REM` contain only floats, `A` is a float, and `I,J ≥ 0`. It
  constrains final `found` to `rowAcc(...)`; final `j`/`number2` are existential
  because they are not the result. The exact plain scope and empty heap rule out
  cell, allocation, and shadowing alternatives.
- `outer-loop` executes the exact reachable outer `#loop`. It constrains final
  `found` to `outerAcc(...)` and final `i` to `I + vsLen(REM)`; only irrelevant
  final loop temporaries are existential. It uses the exact inner claim.
- `has-close-elements` loads the 244-token translated module, calls its loaded
  binding, and constrains the returned `<k>` value to
  `outerAcc(false,VS,T,0,VS)`. It also constrains the installed closure and all
  material configuration cells.
- `float-subtraction` is bridge-free and universally connects typed fixed
  dispatch to `subF` while framing the continuation. Its `WarnTrivialClaim`
  reflects that the fixed equation normalizes the two sides before symbolic
  search, not an imported candidate bridge.

All claim preconditions have explicit satisfying states in
`04_pinning_and_witnesses.log`. The submitted function contains no abrupt
control inside either loop, so the claims' framed trailing continuation does
not hide return/break/continue/exception cleanup.

## Narrow evidence limitations, not unsoundness

- The Haskell proof treats `subF`, `absF`, and `floatLt` as supplied opaque,
  total primitives. It proves the program builds and folds exactly these terms;
  the bridge to CPython/IEEE behavior is the fixed LLVM concrete rules plus
  finite differential evidence, not a universal K/Haskell theorem.
- The final recurrence-to-English existential equivalence is a straightforward
  finite-sequence induction, but there is no separate K claim stating that
  equivalence.

No rule is labeled unsound, so no false-conclusion witness is asserted.
