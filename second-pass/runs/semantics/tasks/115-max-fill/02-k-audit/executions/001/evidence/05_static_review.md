# Static review notes

The exhaustive mechanical inventory is `rule_inventory.md`: 967 declarations
from all 24 supplied-semantics source files plus `verification.k` and `spec.k`
(718 rules, 236 syntax declarations, 7 claims, 5 contexts, and 1
configuration). No local declaration uses `functional`, `simplification`, or
`opaque`. There are 111 `total`, 150 `function`, 31 `priority`, 32 `concrete`,
25 `symbol`, 22 `no-evaluators`, 26 `owise`, 5 `macro`, 2 `strict`, and 1
`seqstrict` attribute-bearing declarations.

## Selected semantics boundary

All 935 declarations under `reference-semantics/` are byte-identical to the
trusted supplied tree. They are therefore the fixed selected semantics, not
candidate proof extensions. The program's reachable path uses:

- `syntax.k`: `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Int`, `For`,
  `Call`, `AugAssign`, `BinOp`, and `Return`; `strict`/`seqstrict` supply the
  stated evaluation order.
- `core.k`: configuration, module load/sequencing, integer literals, scope
  lookup and the builtins scope, and left-to-right argument evaluation.
- `functions.k` and `call.k`: definition loading, closure invocation, argument
  binding, frame push/pop, return, and builtin dispatch.
- `controls.k`: name assignment/update and iterator-based `for`.
- `list.k`, `iter.k`, and `builtins.k`: list iteration and the integer/bool
  `sum` fold.
- `operators.k` and `int.k`: left-to-right binary dispatch, integer `+`, `-`,
  Python-style `//`, and `pyMod`.

The other fixed-semantics declarations have no reachable redex on this
program/input representation. The LLVM example run and the positive Haskell
proof runs exercise the listed path. Fixed-semantics compiler warnings concern
unrelated broad-domain total functions in `builtins.k`, `float.k`,
`methods.k`, and `subscript.k`; none can match this program's reachable terms.

## Complete proof-local declaration disposition

The following covers all 32 declarations in `verification.k` and all 7 claims
in `spec.k`.

| Lines | Declaration(s) | Class and disposition |
|---|---|---|
| verification.k:8-9 | `GridRows` constructors | Pure inductive input representation. Covers empty/nonempty row lists. |
| 11-19 | `rowVals`, `gridVals` and four equations | Total definitional conversion. Base/step guards are constructor-disjoint, exhaustive, and structurally descending. Values are exactly the nested integer lists represented by `GridRows`. |
| 24-28 | `rowSum`, `rowTotal`, `ceilDiv`, `fillTotal`, `maxFillSpec` declarations | Result-bearing mathematical summaries. All except the zero-divisor corner of `ceilDiv` have exhaustive constructor equations. |
| 30-33 | `rowSum`/`rowTotal` equations | Ordinary integer fold; base/step are disjoint and recursion descends. |
| 35-36 | `ceilDiv` equation | For `C>0`, exactly Python `(N+C-1)//C`, using the supplied `pyMod` definition. The `[total]` declaration is over-broad at `C=0`: `ceilDiv(0,0)` reaches modulo/division by zero rather than an integer normal form. Every dependent claim requires `C>0`; this is a declaration-scope evidence gap, not a false conclusion on the theorem domain. |
| 38-41 | `fillTotal`/`maxFillSpec` equations | Empty/nonempty cases are disjoint, exhaustive, and descending. They sum the row results starting at zero. |
| 44-57 | `MAX_FILL_LOOP_BODY` macro and expansion | Exact AST subtree from regenerated `solution.mpy`; macro expansion neither summarizes nor bypasses execution. |
| 70-74 | `symRow`, `symGrid`, `#typedSum`, `#typedLoop` | Free constructor representation and typed iterator control markers. No value oracle is introduced. |
| 79-83 | `#sumAcc(list(symRow(...))) => #typedSum` | Operational representation bridge, priority 40. Reads/writes only `<k>`, preserves every suffix/cell, and is followed by exhaustive typed cases. |
| 85-93 | Two `#typedSum` rules | Constructor-disjoint/exhaustive. Empty yields the supplied list-iterator empty state; step yields exactly head `I` and related tail `symRow(IS)`. This determines, rather than guesses, every value reaching `sum`. |
| 95-102 | `#loop(list(symGrid(...))) => #typedLoop` | Operational representation bridge, priority 40. Reads/writes only `<k>` and preserves arbitrary target/body/continuation and all cells. |
| 104-117 | Two `#typedLoop` rules | Constructor-disjoint/exhaustive. Empty and step exactly mirror supplied list iteration; the step yields `list(symRow(IS))` and related tail `symGrid(GS)`. |
| 119-128 | `finalRow`, `finalWater` and four equations | Total post-loop summaries of the two observable locals. Empty/nonempty cases are disjoint/exhaustive and descend over `GridRows`. These do not affect control or `result`. |
| 137-154 | `#runMaxFill` syntax/rule | Closed driver loads the exact submitted function AST, invokes its real closure, and passes the typed representation of `GS`. It does not replace the function body. All subsequent calls, assignments, arithmetic, loop control, and return use supplied semantics. |
| spec.k:8-44 | Four `bridge-*` claims | Bridge-free, machine-checked one-step connection cases built against `MAX-FILL-DATA` (which imports supplied MPY but not `MAX-FILL-BRIDGES`). They quantify over arbitrary tails, bodies, targets, accumulators, and continuations. Together they exhaust the two constructors of `IntSeq` and `GridRows`; their right sides syntactically match the typed bridge cases under `rowVals`/`gridVals` versus `symRow`/`symGrid`. |
| 51-54 | `sum-fold` | Inductive/circular exact-execution claim. It consumes the real supplied `sum` fold over the typed sequence and constrains its returned integer to `rowTotal(A,IS)`. |
| 58-88 | `fill-loop` | Inductive/circular exact-loop claim. Preconditions fix a real call frame and require `C>0`; post-state fixes `result` to `fillTotal`, plus the actual last `row`/`water` locals. Arbitrary continuation `K` is preserved. |
| 91-109 | `max-fill-correct` | Entry claim. Preconditions are satisfiable and pin every control/resource cell. The right-hand `<k>` value is `maxFillSpec(GS,C)`, not an existential/free result. Only the final scope map is existential because module/function loading changes and deallocates scopes. |

## Bridge context, value, and sensitivity

Representation relation used in the review:

- `symRow(IS)` corresponds to `rowVals(IS)`;
- `symGrid(GS)` corresponds to `gridVals(GS)`.

The four bridge claims prove the supplied-semantics transition for each
constructor case without importing a proposed bridge. Their complete match
domain is covered by the two free-algebra constructors for each sort. The
bridge rules have no guard, binding, environment, heap, stack, return,
exception, output, or allocation effect. Their ellipsis admits arbitrary
continuations, and the bridge claims quantify an arbitrary `K`, so context
containment holds. No bridge creates an abrupt effect.

The bridge-free whole-program experiment in `05_fixed_representation.k` built
but got stuck on K's loss of the element type after symbolic `rowVals(IS)`;
the residual admitted an arbitrary non-int/non-bool `V`. This is a prover
precision limitation, not a counterexample: all ground `IntSeq` constructors
reduce to integer-only `rowVals`, and the candidate's universal constructor
connection claims exist specifically to retain that fact.

Value sensitivity is non-circular: `rowTotal` is defined independently of the
bridge. Mutating the typed head from `I` to `I+1` makes `sum-fold` stick on the
false equality `rowTotal(A+I+1,IS)=rowTotal(A+I,IS)`. Mutating the submitted
body's numerator offset from 1 to 2 makes `fill-loop` stick on the two distinct
`fillTotal` expressions. See `05_bridge_mutation.log` and
`05_body_mutation.log`.

## Construct-to-rule map

| Submitted construct | Declaration/evaluation rules |
|---|---|
| `Module(...)` | syntax.k:61; core.k:124-127 |
| `FuncDef`, `Params` | syntax.k:53,57; functions.k:14-16 |
| `Assign(Name,... )` | syntax.k:41; controls.k:9-18 |
| `Name` / `Int` | syntax.k:9,12; core.k:129-181,193-196 |
| `For` | syntax.k:45; controls.k:62-75,104-108; list.k:9-10; proof typed-loop cases |
| `Call(Name("sum"),row)` | syntax.k:28; call.k:18-32; core.k:183-191; builtins.k:46-56; proof typed-sum cases |
| `AugAssign(Name("result"),"+",...)` | syntax.k:44; controls.k:20-31 |
| nested `BinOp("+","-","//")` | syntax.k:15; operators.k:10-17; int.k:9-20 |
| `Return(Name("result"))` | syntax.k:50; functions.k:77-90 |

No used construct is fabricated or left to an unconstrained oracle.
