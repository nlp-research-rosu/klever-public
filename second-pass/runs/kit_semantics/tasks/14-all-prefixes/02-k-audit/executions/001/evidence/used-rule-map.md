# Material constructor and rule map

The exhaustive lexical inventory is `stage5-rule-inventory.log` (939 items:
230 syntax declarations, 701 rules, five contexts, one configuration, and two
claims). This map identifies the subset reached by the submitted program and
the target claim.

| Submitted constructor / internal term | Declaration or operational rules | Audit decision |
|---|---|---|
| `Module`, statement and expression constructors | `semantics/syntax.k:9-61` | Constructor declarations only; the regenerated term parses to these exact labels. |
| Initial configuration / `#loadAll` / sequencing | `semantics/core.k:49-60,124-127` | Standard initial module scope, empty heap/control cells, and left-to-right statement sequencing. |
| `ImportFrom("typing","List")` | `semantics/controls.k:33-44` | The `owise` import rule makes the typing-only import a runtime no-op; no material operation is skipped. |
| `FuncDef` | `semantics/functions.k:13-20` | Binds the exact parameter list and exact submitted body in `closureVal`, capturing module environment 0. |
| `ListExpr(.Exprs)` / allocation | `semantics/list.k:12-15`; `semantics/core.k:117-121,183-191,213-219` | Evaluates elements left-to-right, constructs `list(.ValSeq)`, and allocates at the fresh heap counter. |
| `Str("")` | `semantics/str.k:12-17` | Empty literal maps to `.IntSeq`; the ASCII restriction is satisfied by this literal. |
| `Assign(Name(...),V)` | `semantics/controls.k:8-18` | Writes the current local frame; the higher-priority cell case is inapplicable because this ordinary frame has no `$cells`. |
| `Name(...)` lookup | `semantics/core.k:129-154` | Resolves the current frame before parent scopes. The guarded higher-priority cell rule is inapplicable to the ordinary frame. |
| `For(Name("char"),Name("string"),BODY)` | strictness in `semantics/syntax.k:45`; `semantics/controls.k:62-74`; string iterator at `semantics/str.k:7-10`; target binding at `semantics/tuple.k:30-41` | Evaluates the iterable once, yields one-character strings left-to-right, writes `char`, executes the exact body, and loops on the strict tail. |
| `BinOp("+",prefix,char)` | strictness in `semantics/syntax.k:15`; dispatch at `semantics/operators.k:10-17`; string case and concatenation at `semantics/str.k:19-26` | Left then right evaluation; exact string concatenation over `IntSeq`. Ref-dereference priorities are inapplicable. |
| `Attribute(prefixes,"append")` / `Call` | `semantics/call.k:15-24`; argument evaluation at `semantics/core.k:183-191`; mutator at `semantics/list.k:52-55` | Receiver lookup yields `ref(H)`; `append` is retained as a mutating bound method, arguments evaluate left-to-right, heap list at `H` gains exactly one value, and call returns `noneV`. |
| `Expr(Call(...))` | `semantics/controls.k:46-48` | Discards only the `noneV` expression result after the heap effect. |
| Function call | `semantics/call.k:18-32,69-74`; parameter binding and frame lifecycle at `semantics/functions.k:62-90` | Looks up the exact closure, evaluates the input argument, allocates one local scope, binds `string`, executes the exact body, and restores module control/environment on return. |
| `Return(Name("prefixes"))` | strictness at `semantics/syntax.k:50`; `semantics/functions.k:77-90` | Looks up the result reference, records it, discards the remaining callee continuation as Python return requires, pops precisely one saved frame, and resumes the caller assignment. |
| Target result binding | assignment rule at `semantics/controls.k:8-18` | Binds `result` to returned `ref(0)` in module scope. |
| `prefixesAcc` | `verification.k:8-16` | Pure definitional summary; exhaustive/disjoint `.IntSeq` and `iCons` equations; strict structural descent; does not rewrite `<k>`. |
| `finishPrefix` | `verification.k:20-23` | Pure exhaustive/disjoint structurally recursive definition of the final local prefix. |
| `finishChar` | `verification.k:25-28` | Pure exhaustive/disjoint structurally recursive definition of the retained loop variable. |
| `SPEC.loop-invariant` | `spec.k:6-37` | Reachability circularity over the exact internal `#loop`, exact body, modified bindings/heap entry, arbitrary continuation, and framed untouched state. |
| `SPEC.all-prefixes` | `spec.k:39-112` | Entry theorem over every `INPUT:IntSeq`; exact parsed program prefix plus `result = all_prefixes(input)`; constrains final heap to `list(prefixesAcc(.IntSeq,INPUT,.ValSeq))`. |

The fixed tree also contains unused language features. All their declarations
and rules remain visible in `stage5-rule-inventory.log`; none contains
`all_prefixes`, `prefixesAcc`, `finishPrefix`, or `finishChar`, and none is
reachable from the material term above. Opaque fixed-semantics primitives
(float operations, sorting, and MD5) are inventoried in
`stage5-attribute-inventory.log`; no target or auxiliary claim depends on them.
