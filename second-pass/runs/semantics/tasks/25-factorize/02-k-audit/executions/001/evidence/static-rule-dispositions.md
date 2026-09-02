# Static rule dispositions

This is the reviewer-authored disposition index for the complete inventory in
`16-rule-inventory.txt`. A row applies to every declaration and rule in the
named file. “Outside cone” means its left-hand side cannot be reached from the
submitted program or either target claim; the file was still checked for a
generic/overlapping rule that could rewrite an in-cone term.

The inventory contains 706 rules, 233 syntax declarations, five contexts, one
configuration, two claims, 107 records carrying `total`, 149 carrying
`function`, 25 carrying `symbol`, 22 carrying `no-evaluators`, 46 carrying
`priority`, 26 carrying `owise`, no `functional`, and no `simplification`.

| Source | Rules | Disposition applying to all rules in source |
|---|---:|---|
| `reference-semantics/semantics.k` | 0 | Assembly only; `MPY` is the proof semantics and `MPY-KRUN` adds `MPY-CONCRETE` only for concrete runs. |
| `semantics/syntax.k` | 0 | All 16 declarations inspected. Every submitted constructor has the required sort/production; strictness is consistent with the used expression order. |
| `semantics/core.k` | 46 | In cone. Configuration, load/sequencing, allocation, lookup, integer literal, truthiness, left-to-right argument evaluation, and list-conversion helpers preserve the used cells. Cell/keyword/string/positional-update cases are outside cone and do not overlap the used plain-frame terms. |
| `semantics/controls.k` | 34 | In cone for plain `Assign`, integer `AugAssign`, the non-math `ImportFrom` no-op, `Expr`, `If`, and `While`. Guards and priorities are disjoint on the concrete used values. For/IfExp/break/continue/ref-truthiness cases are outside cone. |
| `semantics/functions.k` | 15 | In cone for plain `FuncDef`, parameter binding, `Return`, `#endcall`, and `#pop`. They create/pop scope 1, restore scopeLoc 1, preserve heap allocations, and return the list reference. Closure-cell variants are outside cone. |
| `semantics/call.k` | 21 | In cone for `Attribute`, callee/argument evaluation, the mutating append route, and plain `closureVal` invocation. The append priority keeps its receiver as `ref(H)`; parameter binding and continuation/frame state agree with the entry claim. Other builtins/types/annotated closures are outside cone. |
| `semantics/operators.k` | 10 | In cone for generic integer `BinOp` and `Compare`. Reference dereference rules do not overlap these integer operands. Unary/identity/membership cases are outside cone. |
| `semantics/int.k` | 16 | In cone for `+`, `%`, `//`, `>`, and `==`. `D>=2` makes every used divisor nonzero; `pyMod` and floor division agree with positive-divisor Python integer arithmetic. Remaining integer operations are truthful and outside the submitted path. |
| `semantics/list.k` | 27 | In cone for empty-list allocation, `valSeqConcat`, and the priority-40 in-place `append`. Equality/assertion support is used only by the reviewer’s concrete harness. Iteration/membership/deep equality are outside the proof path. |
| `semantics/assert.k` | 3 | Runtime-test cone only. True assertions disappear; false assertions set the modeled exception/exit code and discard the continuation. No assertion appears in either target claim. |
| `semantics/concrete.k` | 16 | LLVM-only and absent from both proof definitions. Reviewed concrete deep equality and keyed-sort rules do not rewrite the submitted program’s ordinary execution before the reviewer assertions. |
| `semantics/bool.k` | 13 | Outside cone: the program uses comparison-produced K booleans only through `truthy` in `core.k`, not `BoolOp` or boolean operators. No generic rule overlaps the used heads. |
| `semantics/builtins.k` | 137 | Outside cone: `typing.List` is an ignored type-only import and no builtin is called. Registry values are created by `builtinsScope` in `core.k`, but none influences the result. Opaque MD5 and evaluator helpers are unreachable. |
| `semantics/comprehension.k` | 7 | Outside cone; no comprehension constructor occurs. Macro expansions do not overlap any submitted term. |
| `semantics/dict.k` | 28 | Outside cone; no dict syntax/value occurs. Index/assignment priority rules have disjoint heads. |
| `semantics/float.k` | 121 | Outside cone; no float, math import, true division, float builtin, or intercepted math call occurs. All float opaque/total symbols are therefore value-, control-, and result-inert here. Duplicate mixed arithmetic rules have identical right-hand sides. |
| `semantics/iter.k` | 0 | Iterator protocol declarations only; no used iterator term occurs. |
| `semantics/methods.k` | 75 | The `applyMethod` declaration is imported, but the used `append` call is handled directly by `list.k`; every method rule is outside cone. No generic method equation can consume the append reference call first. |
| `semantics/range.k` | 6 | Outside cone; no range or iterator term occurs. |
| `semantics/set.k` | 12 | Outside cone; no set term occurs. |
| `semantics/sort.k` | 19 | Outside cone; no `sorted` or `.sort` call occurs. `sortVS` and `sortKeyVS` cannot influence the target. |
| `semantics/str.k` | 28 | Outside operational cone except compiler parsing of String tokens. No runtime `Str` value or string operation occurs; `strLt` cannot influence the proof. |
| `semantics/subscript.k` | 40 | Outside cone; no subscript/slice occurs. Its underspecified `total` positional access cannot influence a result because no term calls it. |
| `semantics/tuple.k` | 21 | Outside cone; no tuple, unpacking, or for-target binding occurs. Importing its `#bindTgt` declaration through controls creates no rewrite on used terms. |
| `verification.k` | 11 | All proof-local rules are in cone or directly related. The three macro rules reproduce the submitted body; three `factorLoop` equations and three `factorDivisor` equations have disjoint, exhaustive guards on `N>=1,D>=2`; `primeFactors` is a definition, not an oracle. The priority-40 loop rule is an operational bridge exactly equal to the separately proved arbitrary-continuation claim. |
| `spec.k` | 0 | Two reachability claims. Preconditions are satisfiable and result cells are constrained. |

## Used-constructor mapping

| Submitted construct | Declaration | Dynamic rules |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`, `syntax.k:56` | `core.k:124-127` |
| `ImportFrom("typing","List")` | `syntax.k:43` | `controls.k:35-44` (non-math no-op) |
| `FuncDef`, `Params`, closure | `syntax.k:53,57`, `core.k:31` | `functions.k:14-16`, `call.k:69-74` |
| `Assign(Name, ...)` | `syntax.k:41` | `controls.k:9-18` |
| `ListExpr()` and list reference | `syntax.k:17`, `core.k:18,29` | `list.k:13-20`, `core.k:117-121` |
| `Int`, `Name` | `syntax.k:9,12` | `core.k:130-154,193-196` |
| `While` | `syntax.k:46` | `controls.k:65-82`; exact proved acceleration `verification.k:67-94` |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17`, `int.k:22-27` |
| `If` | `syntax.k:49` | `controls.k:50-54` |
| `%`, `//`, `+` integer `BinOp` | `syntax.k:15` | `operators.k:12`, `int.k:9-20` |
| `Attribute`, `Call`, argument list | `syntax.k:28-29,37` | `call.k:15-24`, `core.k:183-191` |
| `factors.append(divisor)` | same call declarations | `list.k:52-55` |
| `Expr(call)` | `syntax.k:52` | `controls.k:46-48` |
| `AugAssign(divisor,"+",1)` | `syntax.k:44` | `controls.k:20-31`, `int.k:9` |
| `Return(factors)` | `syntax.k:50` | `functions.k:77-90` |

## Proof-local rule decisions

- `factorizeStep`, `factorizeBody`, and `factorizeDef` are macros only. The
  fresh module-loading claim in `pinning-spec.k` closes from the complete
  literal submitted module to the exact `factorizeBody` closure used by the
  entry theorem.
- `factorLoop`’s base rule is correct for `N<=1`. On the intended domain, its
  divisible and non-divisible guards are complementary; division uses
  `N/D` because `pyMod(N,D)=0`, and only the divisible case appends `D`.
- `factorDivisor` has the identical state recurrence without the list
  accumulator. Its guards are likewise complementary on the claim domain.
- `primeFactors(N) => factorLoop(N,2,.ValSeq)` is a transparent definition.
- `factorize-loop-lemma` is the only proof-local operational bridge. Its
  matched continuation is the same arbitrary `KONT` quantified by the
  bridge-free `factorize-loop` claim; all matched scope and heap fragments,
  guards, and frame variables are identical. The fixed and accelerated
  continuation probes both close. A ground body mutation reaches `[3]`
  instead of `[2]` and is rejected.

## Opaque and total-symbol ledger

The supplied semantics declares the following proof-opaque symbols:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`,
and `md5hexCodes`. `floorFI`, `toF`, and `ceilF` are also `symbol`/`total`
with concrete equations but no `no-evaluators` attribute. None is reachable
from the submitted program, summary functions, target claims, or promoted
lemma. The `total` underspecification in `valSeqAt` and the LLVM exhaustiveness
warnings for `mapStrVS`, `joinCodes`, `floorFI`, `toF`, `ceilF`, and
`valSeqAt` are likewise outside the execution cone. They neither justify nor
affect the factorization conclusion.
