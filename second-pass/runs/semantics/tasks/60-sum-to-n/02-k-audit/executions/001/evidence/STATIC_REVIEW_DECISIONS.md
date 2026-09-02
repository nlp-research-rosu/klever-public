# Static review decisions

This file supplies the decision layer for the exhaustive source listing in
`STATIC_RULE_INVENTORY.md`. “Fixed” means the declaration/rule is byte-identical
to the trusted `/reference/reference-semantics` baseline. It is not a
candidate-authored proof extension. “Inert” means no term with that rule’s head
is reachable from the submitted `solution.mpy` claim.

## Candidate-authored proof layer

| Source group | Inventory | Decision |
|---|---:|---|
| `verification.k` runner syntax | 1 of 2 syntax declarations | Accept. It introduces only `#runSumToN(Int)`. |
| `verification.k` runner rule | 1 of 2 rules | Accept as an exact launch expansion, not a program summary. It rewrites the runner to `#loadAll(EXACT_SUBMITTED_MODULE) ~> Call(Name("sum_to_n"), Int(N), .Exprs)`, preserves any surrounding continuation, touches no cell, and does not return or skip execution. `16_pinning_and_ground_values.log` establishes term identity. |
| `verification.k` `triangular` syntax | 1 of 2 syntax declarations | Accept as a transparent, result-bearing definitional summary. It is `[function,total]`, has one unguarded equation over all `Int`, no overlap, no recursion, and a fixed nonzero divisor 2. |
| `verification.k` `triangular` equation | 1 of 2 rules | Accept. Its RHS is exactly the fixed MPY integer floor-division expression reached by the submitted body. It neither intercepts a program term nor supplies a fresh/oracle value. |
| `spec.k` | 1 reachability claim | Accept for `N >=Int 0`. It consumes the runner, constrains `<k>` to the exact `triangular(N)` result, and pins every state cell. It is neither implication-only nor existential in the result. |

There are no proof-local simplification rules, priority rules, auxiliary
claims, aliases, opaque symbols, `[concrete]` rules, or operational shortcuts.

## Exact used path through the fixed semantics

| Submitted construct | Declaration | Operational rules used | Review decision |
|---|---|---|---|
| `Module(...)` | `semantics/syntax.k` `Module(Stmts)` | `core.k` `#loadAll(Module(SS))`, statement-head sequencing, `.Stmts` completion | Fixed and faithful. The whole one-definition module is loaded before the appended call. |
| `FuncDef("sum_to_n", Params("n"), BODY)` | `syntax.k` `FuncDef`/`Params` | `functions.k` ordinary `FuncDef` rule | Fixed and faithful. The closure stores the exact body and defining module environment 0. |
| `Call(Name("sum_to_n"), Int(N), .Exprs)` | `syntax.k` `Call`, `Name`, `Int`, `Exprs` | `call.k` generic `[owise]` call route; `core.k` name lookup and left-to-right `#evalArgs`; `call.k` ordinary `closureVal` dispatch | Fixed and faithful. No special `Call(Attribute(...))` interceptor matches. Lookup selects the just-stored closure, the argument is evaluated once, and a frame is pushed. |
| Parameter `n` | `syntax.k` `ParamNames` | `functions.k` `#bindP`; `core.k` `#look` | Fixed and faithful. A fresh scope 1 is created with parent 0, then `"n"` maps to `N`; no cell-variable priority rule is enabled. |
| `Return(E)` | `syntax.k` strict `Return` | `functions.k` `Return(V)`, `#pop` | Fixed and faithful. The expression evaluates before return; the frame is removed, caller env 0 and scope allocator 1 are restored, and the value continues to the caller. |
| `BinOp("*", ...)`, `BinOp("+", ...)`, `BinOp("//", ...)` | `syntax.k` `BinOp` `[seqstrict(2,3)]` | `operators.k` `BinOp` dispatch; `int.k` integer `+`, `*`, `//`; `int.k` `pyMod` | Fixed and faithful on the claim domain. Operands evaluate left-to-right. All values remain `Int`; divisor is the literal 2, so no zero-division gap is reached. |
| `Int(1)`, `Int(2)` | `syntax.k` `Int` expression | `core.k` integer literal rule | Fixed and faithful. |

The actual state path is: load exact definition into module scope 0; look up
that binding; allocate scope 1; bind `"n"`; evaluate `n * (n + 1) // 2`; return;
pop scope 1; restore all transient cells. No heap allocation, output, exception,
loop, branch, collection, float, string, sorting, MD5, import, assertion, or
concrete-only rule is reached.

## Exhaustive fixed-semantics module decisions

The table covers every source item enumerated in `STATIC_RULE_INVENTORY.md`;
the rule counts sum to 695 fixed rules, plus the two candidate rules above.

| Module/file | Rules | Decision over all inventoried rules |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import declarations are fixed. The proof imports `MPY`, not `MPY-KRUN`; concrete-only `MPY-CONCRETE` is not in the proof import closure. |
| `syntax.k` | 0 | All 16 AST syntax groups are fixed. The exact used subset is mapped above; all other constructors are inert. |
| `core.k` | 46 | Fixed. The configuration, load/sequence, lookup, literal, argument-evaluation, and value/operator declarations on the used path were checked above. Cell refs, heap allocation, keyword tags, builtins registry entries, truthiness for non-ints, and sequence helpers are inert. |
| `functions.k` | 15 | Fixed. Ordinary definition/call return lifecycle is checked above. Annotated closures, free/cell variables, and lambdas are inert. |
| `call.k` | 21 | Fixed. Ordinary closure dispatch is checked above. Methods, builtins, type calls, heap dereference, and annotated-closure allocation are inert. |
| `operators.k` | 10 | Fixed. Integer `BinOp` dispatch is checked above. unary, comparison, identity, and heap-dereference rules are inert. |
| `int.k` | 16 | Fixed. The `+`, `*`, `//`, and `pyMod` rules are used and have disjoint operator heads/sorts; divisor 2 is safe. Unary, subtraction, remainder as an observable result, exponentiation, and comparisons are inert. |
| `iter.k` | 0 | Fixed declarations only; inert. |
| `range.k` | 6 | Fixed and inert. |
| `bool.k` | 13 | Fixed and inert. |
| `float.k` | 121 | Fixed and inert: no `Float`, float call, or mixed numeric term occurs. Its opaque symbols are accounted below. |
| `str.k` | 28 | Fixed and inert. |
| `set.k` | 12 | Fixed and inert. |
| `list.k` | 27 | Fixed and inert. |
| `tuple.k` | 21 | Fixed and inert. |
| `subscript.k` | 40 | Fixed and inert. |
| `comprehension.k` | 7 | Fixed and inert. |
| `methods.k` | 75 | Fixed and inert. |
| `controls.k` | 34 | Fixed and inert. |
| `builtins.k` | 137 | Fixed and inert; the submitted program performs no builtin call. |
| `sort.k` | 19 | Fixed and inert. |
| `assert.k` | 3 | Fixed and absent from the proof claim. It is used only by the separately regenerated concrete smoke harness. |
| `dict.k` | 28 | Fixed and inert. |
| `concrete.k` | 16 | Fixed and excluded from the proof module import closure. It is used only in the independent LLVM concrete definition. |

For fixed, inert rules this audit found no route by which they can affect a
branch, state cell, result, exception, or proof condition of the target claim.
Consequently no candidate unsoundness is alleged for them. This is a reachability
decision, not a claim that the supplied subset is a complete CPython semantics.

## Attribute, overlap, priority, and totality decisions

- The complete inventory contains 108 `[total]`, 36 `[concrete]`, 45 priority,
  26 `[owise]`, 3 `[macro]`, 1 `[macro-rec]`, 2 `[strict]`, 1 `[seqstrict]`, no
  `[functional]`, and no `[simplification]` blocks. Every exact block is in
  `STATIC_RULE_INVENTORY.md`.
- On the target path, the only candidate total function is `triangular`: one
  exhaustive equation, no overlap, no recursion. Fixed `pyMod` has one equation
  and receives divisor 2. Integer operator equations are separated by literal
  operator and argument sort. The generic call’s `[owise]` case applies only
  after all special syntactic call interceptors fail; `Call(Name(...), ...)`
  matches none of them.
- The LLVM compiler reported non-exhaustive total-function coverage for
  `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. Those are
  general-language evidence gaps, not alleged false equations: the tool gives
  no false equality witness, and none of the heads is reachable in this claim.
  They therefore do not support an unsoundness label under the audit rule.
- None of the 45 fixed priority rules matches the target symbolic path. In
  particular, cell-ref priorities require `"$cells"`, heap priorities require
  `ref`, and special calls require `Attribute` or named builtins; all are absent.

## Opaque and trusted symbols

The 25 fixed `[symbol(...)]` declarations are:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

Twenty-two also carry `[no-evaluators]`; the three remaining symbols are
`floorFI`, `toF`, and `ceilF`, which have concrete equations. All 25 are inert
for the target program. No candidate extension introduces an opaque symbol, and
the claim result contains none.

The active primitive boundary is limited to K’s trusted unbounded `Int`,
integer arithmetic/comparison, Boolean conditions, maps/lists used as
configuration storage, K sequencing, and the Haskell backend’s rewriting/SMT
reasoning, plus the byte-identical supplied MPY rules listed in the exact path.
