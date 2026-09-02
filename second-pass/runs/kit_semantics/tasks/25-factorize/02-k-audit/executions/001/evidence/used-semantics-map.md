# Audited execution slice

The exhaustive source inventory is `19-rule-inventory.log` (26 K files, 934
declarations: 228 syntax blocks, 698 rules, 5 contexts, 1 configuration, and 2
claims). This map records every declaration/rule family reachable from the
submitted `factorize` body. Line numbers refer to the trusted scratch copy of
`reference-semantics`.

| Program construct / runtime object | Declaration and rules | Audit disposition |
|---|---|---|
| `Module`, `Stmts` | `syntax.k:56,61`; `core.k:124-127` | Ordered module/statement execution. Concrete probe confirms load to `.K`. |
| `ImportFrom("typing","List")` | `syntax.k:43`; `controls.k:35-44` | The non-`math` `[owise]` rule removes it without state change. This is the only source construct omitted from the entry claim. |
| `FuncDef`, `Params`, `closureVal` | `syntax.k:53,57,60`; `core.k:31`; `functions.k:14-20` | Binds the exact body at module scope 0. |
| Function call and frame | `syntax.k:28`; `core.k:185-191`; `call.k:18-21,69-75`; `functions.k:63-66,78-90` | Callee then arguments evaluate left-to-right, parameter `n` binds in fresh scope 1, return pops the exact frame while the allocated list escapes. |
| `Name` | `syntax.k:12`; `core.k:130-154` | Lookup begins at current environment and follows the parent; the claims pin the module binding and all locals. Cell-specific priority rules are guard-inapplicable because these are plain scopes. |
| `Assign` | `syntax.k:41` (`strict(2)`); `controls.k:9-18` | RHS evaluates first, then the current local map is updated. Cell-priority rule is guard-inapplicable. |
| `Int` | `syntax.k:9`; `core.k:193-196` | Direct K `Int` value. |
| `ListExpr`, `ref`, `list`, allocation | `syntax.k:17`; `core.k:14,18,29,117-121,183-191,213-219`; `list.k:12-20` | Empty literal evaluates elements, creates `list(.ValSeq)` at fresh heap location 0, and returns `ref(0)`. |
| `While`, `#while`, loop control | `syntax.k:46`; `controls.k:65-67,76-85` | Guard evaluates each iteration; true runs the full body and re-enters `#while`, false preserves the continuation. |
| `Compare`, `CmpOp` | `syntax.k:30,32`; `operators.k:14-17`; `int.k:22-27` | Explicit contexts evaluate left then right. Used operators `<=` and `==` have ordinary integer meanings. Reference-deref priority rules are inapplicable to integer operands. |
| `BinOp` | `syntax.k:15` (`seqstrict(2,3)`); `operators.k:10-12`; `int.k:9-20` | Left-to-right evaluation. Used `%`, `//`, and `+` map to `pyMod`, floor division, and addition. The claim domain keeps the divisor at least 2. |
| `If` | `syntax.k:49` (`strict(1)`); `core.k:198-205`; `controls.k:50-54` | Integer comparison yields `Bool`; exactly one branch is selected. Reference priority rules do not match. |
| `Expr` | `syntax.k:52` (`strict`); `controls.k:46-48` | Evaluates the append call for its heap effect, then discards `noneV`. |
| `Attribute`, bound method, call arguments | `syntax.k:28-29`; `core.k:183-191`; `call.k:15-24,52-67` | `factors.append` evaluates to a bound method on `ref(0)`; append is classified as mutating, so the receiver is not dereferenced before dispatch. |
| `append` | `list.k:18-20,52-55` | Priority rule performs the in-place heap update `A -> valSeqConcat(A,vCons(D,.ValSeq))` and yields `noneV`. |
| `Return` | `syntax.k:50` (`strict`); `functions.k:77-90` | Evaluates `factors` to `ref(0)`, sets `retV`, restores caller environment/stack/scope counter, and keeps the heap allocation. |

## Proof-local inventory and dispositions

`verification.k` contains exactly one syntax declaration and three rules:

1. `factorAcc(ValSeq,Int,Int) [function]` is a definitional summary. It is not
   `total`, `functional`, `symbol`, opaque, concrete, prioritized, or a
   simplification.
2. `N < D` returns the accumulator. This is exactly the false-loop-guard case.
3. `D <= N && pyMod(N,D)==0` appends `D`, uses the same supplied floor-division
   formula as `int.k:16`, and keeps `D`.
4. `D <= N && pyMod(N,D)!=0` keeps the accumulator/remainder and increments
   `D`.

On every proof use (`N>=1`, `D>=2`) the guards are exhaustive and pairwise
disjoint. `pyMod` is defined because `D` is nonzero. The recursive definition
descends: a divisible step reduces positive `N` by a factor of at least two;
an indivisible step increases `D` until the base guard holds. No equation
overlap produces differing right-hand sides.

`spec.k` contains the two inventoried claims and no rules. `factor-loop` is an
exact-context circularity over one real loop head; `factorize` is the entry
claim. There are no ellipses in their cells, no arbitrary continuation, and no
proof-local operational bridge.

## Inert declarations and opaque boundaries

All other supplied modules/rules in `19-rule-inventory.log` are unreachable
from this body and do not contribute to claim closure. This includes all 25
supplied `[symbol(...)]` declarations. The 22 explicitly opaque
`[no-evaluators]` symbols are:

`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and
`md5hexCodes`.

The additional symbolic declarations `floorFI`, `toF`, and `ceilF` have
`[symbol]` but not `[no-evaluators]`; their only equations are concrete-side
rules. None can be reached from the integer-only program. The inventory marks
35 `[concrete]` equations; none is reached by the audited proof.
`MPY-CONCRETE` itself is imported only by `MPY-KRUN`, not by `VERIFICATION`.
No opaque value appears in a guard, heap value, return, or postcondition of
either audited claim.

No source declaration has `[functional]`, `[simplification]`, or `[simplify]`.
The 45 priority-bearing source rules are fixed-semantics dispatch/dereference
rules. The only reachable priority rule is `list.k:53-55` for mutating
`append`; its complete heap update is explicitly represented in the loop
claim. The remaining priority rules have constructor- or guard-disjoint left
hand sides for this execution slice.

## Per-file disposition of all supplied rules

This table accounts for every supplied rule in the inventory. “Unreachable”
means that neither the submitted constructor tree nor any active semantic rule
can produce the rule's required constructor/operator/type on this execution
slice; those rules therefore cannot contribute to either `#Top`.

| File | Inventory | Disposition |
|---|---:|---|
| `assert.k` | 3 rules | Unreachable in the proof. The fresh LLVM probe alone uses assertions; both true and false/ref paths have ordinary state effects, and the probe reaches `.K`. |
| `bool.k` | 13 rules, 1 context | Unreachable: no unary `not`, Boolean comparison, or `BoolOp`. Loop/if truthiness uses the reviewed `core.k` Bool equation. |
| `builtins.k` | 137 rules, 38 syntax blocks | Unreachable: no builtin call occurs. None overlaps the user-closure or bound-append dispatch. `md5hexCodes` is opaque but inert. |
| `call.k` | 21 rules, 3 syntax blocks | Plain attribute/callee/argument/closure/append routing is active and individually mapped above. Builtin/type/annotated-closure/ref-read branches are constructor- or guard-disjoint. |
| `comprehension.k` | 7 rules, 3 syntax blocks | Unreachable: no comprehension or generated comprehension continuation. |
| `concrete.k` | 16 rules, 5 syntax blocks | Not imported by `VERIFICATION`; only `MPY-KRUN` imports it. Its sort/deep-equality rules are also absent from the program proper. |
| `controls.k` | 34 rules, 3 syntax blocks | Plain assignment, inert import, `Expr`, `If`, and `While` families are active and mapped. Cell assignment, `IfExp`, `For`, break/continue, and ref-truthiness branches are disjoint/unreachable. |
| `core.k` | 46 rules, 37 syntax blocks, 1 configuration | Configuration, allocation, sequencing, lookup, argument evaluation, integer literal, Bool truthiness, and sequence helpers are active and mapped. Keyword/cell and unrelated truthiness/helper rules cannot match. |
| `dict.k` | 28 rules, 12 syntax blocks | Unreachable: no dict value, entry, method, comparison, or dict continuation. |
| `float.k` | 121 rules, 34 syntax blocks | Unreachable: the constructor tree and all active values are `Int`/`Bool`/list/ref, never `Float`. All float opaque symbols are inert. |
| `functions.k` | 15 rules, 4 syntax blocks | Plain `FuncDef`, parameter binding, return/endcall, and pop are active and mapped. Annotated closure/cell/lambda rules cannot match the pinned closure. |
| `int.k` | 16 rules, 1 syntax block | `%`, `//`, `+`, `<=`, and `==` are active and reviewed. Remaining integer operators are truthful built-in equations and cannot fire under different operator strings. |
| `iter.k` | 1 syntax block, no rules | Iterator protocol declaration only; unreachable because the program has no `For`/iterator consumer. |
| `list.k` | 27 rules, 5 syntax blocks | List literal allocation, `valSeqConcat`, and mutating append are active and reviewed. Iteration, concatenation syntax, equality, deep equality, and membership require absent constructors/operators. |
| `methods.k` | 75 rules, 27 syntax blocks | Its `applyMethod` declaration is part of dispatch, but no methods rule fires: append is intercepted by the higher-priority exact rule in `list.k`. All string/list-count helpers are unreachable. |
| `operators.k` | 10 rules, 2 contexts | Generic binary/compare dispatch and compare contexts are active. `is`/`is not`, unary, and ref-deref paths are operator- or sort-disjoint. |
| `range.k` | 6 rules, 2 syntax blocks | Unreachable: no `rangeObj` or iteration. |
| `set.k` | 12 rules, 6 syntax blocks | Unreachable: no set construction/value/operator. |
| `sort.k` | 19 rules, 6 syntax blocks | Unreachable: no `sorted` or `.sort`; `sortVS`/`sortKeyVS` never influence the proof. |
| `str.k` | 28 rules, 5 syntax blocks | Unreachable: source strings are only identifier/operator tokens in AST constructors, never evaluated Python `Str` values. |
| `subscript.k` | 40 rules, 15 syntax blocks, 2 contexts | Unreachable: no subscript, slice, or assignment target of those forms. |
| `syntax.k` | 16 syntax blocks | Declares the complete MPY grammar. The used alternatives and strictness are mapped above; unused alternatives introduce no rules by themselves except mechanically generated evaluation contexts. |
| `tuple.k` | 21 rules, 4 syntax blocks | Unreachable: no tuple expression/value, membership, tuple target, or unpack. |
| `semantics.k` | assembly only | `MPY` imports the fixed proof modules; `MPY-KRUN` additionally imports `MPY-CONCRETE`. No rules are declared here. |

The only local rules beyond this trusted tree are the three `factorAcc` rules,
already decided individually above. Thus every one of the 698 inventoried
rules has either an active-rule disposition or a constructor/guard
unreachability disposition. No false-conclusion witness was found, so this
audit does not label any rule unsound.
