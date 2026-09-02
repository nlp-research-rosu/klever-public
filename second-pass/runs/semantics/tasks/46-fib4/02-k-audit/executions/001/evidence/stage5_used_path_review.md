# Used-path static review

This review uses the trusted supplied-semantics scratch copy at
`/tmp/audit-work/46-fib4-audit/candidate-src/reference-semantics`. The candidate
tree was recursively byte/type identical to that trusted tree. The complete
line-addressable inventory and per-record disposition is in
`stage5_rule_inventory.md`.

## Construct-to-rule map

| Submitted MPY construct | Declaration | Rules/contexts exercised | Review |
|---|---|---|---|
| `Module` / statement list | `semantics/syntax.k:61`, `semantics/core.k:124` | `core.k:125-127` | Loads and sequences the submitted statements in order. |
| `FuncDef`, `Params` | `syntax.k:53,57`; closure value `core.k:31` | `functions.k:14-16` | Binds the exact body as a closure in the current scope. |
| `Call` | `syntax.k:28` | `call.k:20-21,69-75`; `core.k:185-191` | Callee is resolved first, arguments are evaluated left-to-right, and a fresh frame is pushed. |
| Parameter `n` | `syntax.k:60` | `functions.k:63-66`; `core.k:131-154` | The single actual argument binds to `n`; lookup follows the active scope chain. |
| `Int` | `syntax.k:9` | `core.k:194` | MPY integer literals become unbounded K integers. |
| `Name` | `syntax.k:12` | `core.k:130-154` | Reads current locals; no cell/heap path is used by this program. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:51-54`; `core.k:199-205` | Evaluates each integer comparison and selects exactly one branch. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:22-27` | Left then right evaluation; `==` and `<=` use ordinary integer predicates. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` | Evaluates the value, discards the remaining callee continuation, restores the caller frame, and returns the value. |
| `Assign` | `syntax.k:41 [strict(2)]` | `controls.k:9-18` | Evaluates the RHS first and updates the named local. The higher-priority closure-cell case is guard-disjoint here. |
| `BinOp("+", ...)` | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12`; `int.k:9` | Operands are evaluated left-to-right and added as mathematical integers. |
| `While` | `syntax.k:46` | `controls.k:65-82,85`; `core.k:126-127` | Re-evaluates the guard, executes the body in order when true, and repeats via the loop label. |
| `Assert` (spec only) | `syntax.k:51 [strict]` | `assert.k:6-15` | A true assertion disappears; a false one sets `AssertionError` and exit code 1, which cannot unify with the positive claim target. |

## Configuration and state

The single configuration is `core.k:49-60`: `<k>`, current environment,
scope store/location, heap/location, call stack, return state, exception state,
and exit code. The Fib4 program allocates call frames but no heap objects.
`call.k:69-75` and `functions.k:85-90` push/pop frames, restore the environment,
and remove each completed frame. All positive operational cases pin empty heap
and stack, `NoExc`, and exit code 0 before and after.

## Extension and overlap review

`verification.k` declares no syntax, function, totality assertion, opaque
symbol, priority rule, semantic rule, simplification, or lemma. It imports
`MPY` only. Thus there is no candidate operational bridge or result-bearing
abstraction to validate.

The complete inventory has 227 syntax declarations, 695 rules, 5 contexts, 1
configuration, and 2 claims. It has 145 `[function]` classifiers, 107 `[total]`
classifiers, 22 `[no-evaluators]` opaque symbols, 45 priority rules, and 26
`[owise]` rules. It has zero `[functional]` and zero `[simplification]`
declarations/rules.

The opaque symbols are confined to float, sorting, string comparison, and MD5
subsystems. No term on either Fib4 proof path contains those sorts or symbols,
so none affects control, state, return values, or a postcondition here. Likewise,
the imported list/dict/set/string/range/comprehension/method/builtin rules are
constructor- or callee-disjoint from the submitted Int-only path. No
proof-specific priority overlaps a fixed-semantics rule.

The fresh builds warn that six fixed-baseline `[total]` functions are not
syntactically exhaustive (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`). None occurs in `solution.mpy`, either positive claim, or the
mutation. This is an unused fixed-language evidence gap, not a witnessed false
conclusion for this theorem. No local rule is labeled unsound because the audit
found no concrete or symbolic false-conclusion witness on the intended Fib4
domain.

## Claim-specific review

`loop-step` is an auxiliary execution claim, not a recurrence invariant. It
correctly establishes only the six local updates:

`(a,b,c,d,next_value,i) = (A,B,C,D,E,I)`

becomes

`(B,C,D,A+B+C+D,A+B+C+D,I+1)`.

It has no `n`, no loop guard, no Fib4 relation, and no connection to a returned
value.

`operational-cases` executes an exact copy of the submitted closure body for
thirteen ground calls, `n = 0..12`, and constrains their results through
assertions. It has no symbolic input and says nothing about any `n >= 13`.
