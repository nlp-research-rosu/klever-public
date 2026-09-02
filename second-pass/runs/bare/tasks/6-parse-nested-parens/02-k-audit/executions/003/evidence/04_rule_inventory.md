# Exhaustive local K declaration and rule inventory

Sources inventoried: `/candidate/semantic.k`, `/candidate/verification.k`,
`/candidate/spec.k`, and `/candidate/mutation-spec.k`. Built-in declarations
from imported K modules are outside this local inventory.

## Attributes and extension classes

- Local `[function]` declarations: `eval`, `lookupPy`, `stringOf`, `truth`,
  `eqPy`, `gtPy`, `addPy`, `subPy`, `appendPy`, `appendVals`, `iterable`,
  `chars`, `splitSpaces`, and `solutionProgram`.
- Local `[total]`, `[functional]`, `[simplification]`, `[priority]`, `[owise]`,
  `[anywhere]`, or `[macro]` attributes: none. In particular, the comment that
  calls `solutionProgram` a “macro” is descriptive; the actual attribute is
  `[function]`.
- Opaque/uninterpreted local symbols: none. Every local function has one or
  more equations. Most are deliberately partial outside the target subset, so
  unsupported uses become visibly stuck.
- Local auxiliary claims or lemmas: none. The only claims are the three ground
  target claims in `spec.k` and the candidate's one ground negative probe in
  `mutation-spec.k`.
- Operational bridges that skip program-defined computation: none.
  `solutionProgram` is a definitional name for the full submitted constructor
  tree; the constructor-level equality is checked in
  `03_program_pinning.log`.

## Syntax declarations

| Source | Local sort | Productions |
|---|---|---|
| `semantic.k:6` | `Program` | `Module(Stmts)` |
| `semantic.k:8` | `Stmts` | empty-separated `List{Stmt,""}` |
| `semantic.k:9` | `Strs` | comma-separated `List{String,","}` |
| `semantic.k:10` | `Exprs` | comma-separated `List{Expr,","}` |
| `semantic.k:11` | `CmpOps` | comma-separated `List{CmpOp,","}` |
| `semantic.k:13` | `Params` | `Params(Strs)` |
| `semantic.k:15-22` | `Stmt` | `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`, `For`, `If`, `Expr`, `Return` |
| `semantic.k:24-30` | `Expr` | `Name`, `Int`, `Str`, `ListExpr`, `Attribute`, `Call`, `Compare` |
| `semantic.k:32` | `CmpOp` | `CmpOp(String,Expr)` |
| `semantic.k:44-47` | `PyVal` | `pyInt`, `pyStr`, `pyBool`, `pyList` |
| `semantic.k:48` | `PyVals` | `.PyVals`, `PyVal :: PyVals` |
| `semantic.k:50` | `Result` | `noResult`, `result(PyVal)` |
| `semantic.k:51` | `Function` | `function(Params,Stmts)` |
| `semantic.k:53-56` | `KItem` | `start`, `invoke`, `forValues`, `choose` |
| `semantic.k:113` | `PyVal` | `eval(Expr,Map) [function]` |
| `semantic.k:114` | `PyVal` | `lookupPy(String,Map) [function]` |
| `semantic.k:128` | `String` | `stringOf(PyVal) [function]` |
| `semantic.k:131` | `Bool` | `truth(PyVal) [function]` |
| `semantic.k:134` | `Bool` | `eqPy(PyVal,PyVal) [function]` |
| `semantic.k:138` | `Bool` | `gtPy(PyVal,PyVal) [function]` |
| `semantic.k:141` | `PyVal` | `addPy(PyVal,PyVal) [function]` |
| `semantic.k:144` | `PyVal` | `subPy(PyVal,PyVal) [function]` |
| `semantic.k:147` | `PyVal` | `appendPy(PyVal,PyVal) [function]` |
| `semantic.k:150` | `PyVals` | `appendVals(PyVals,PyVal) [function]` |
| `semantic.k:154` | `PyVals` | `iterable(PyVal) [function]` |
| `semantic.k:158` | `PyVals` | `chars(String) [function]` |
| `semantic.k:165` | `PyVals` | `splitSpaces(String) [function]` |
| `verification.k:9` | `Program` | `solutionProgram [function]` |

The configuration at `semantic.k:58-65` has exactly five material cells:
`<k>` for control, `<input>` for the external string, `<env>` for local
bindings, `<functions>` for registered definitions, and `<result>` for the
observable return value.

## Ordinary operational rules

| # | Source | Rule role | Static assessment |
|---:|---|---|---|
| 1 | `semantic.k:68` | Expand a module's statement list and schedule `start` afterward. | Faithful for the submitted one-module execution. |
| 2 | `semantic.k:69` | Sequentialize a nonempty `Stmts` list left-to-right. | Faithful evaluation order. |
| 3 | `semantic.k:70` | Remove an empty statement list. | Correct list identity. |
| 4 | `semantic.k:72` | Ignore `ImportFrom`. | Sound for the actual typing-only import after the trusted translator has erased annotations. The pattern is deliberately not a reusable model of effectful Python imports. |
| 5 | `semantic.k:73-74` | Register a function body in `<functions>`. | Correct for the target's top-level definition; map update gives the last binding. |
| 6 | `semantic.k:76-77` | Invoke `parse_nested_parens` on the `<input>` string. | Pins the configured entry point used by this task. |
| 7 | `semantic.k:79-81` | Resolve the registered one-parameter function, replace control with its body, and initialize its local environment. | Correct for the target's sole top-level call; deliberately lacks general call frames, which the submitted program does not exercise. |
| 8 | `semantic.k:84-85` | Evaluate an assignment RHS in the old environment, then update the named binding. | Correct for every target assignment. |
| 9 | `semantic.k:87-88` | Integer `+=`. | Correct and disjoint from rule 10 by operator token. |
| 10 | `semantic.k:90-91` | Integer `-=`. | Correct and disjoint from rule 9. |
| 11 | `semantic.k:93-94` | Evaluate an `If` guard and schedule `choose`. | The guard is pure in the target; evaluation precedes branch execution. |
| 12 | `semantic.k:95` | Select true branch. | Correct. |
| 13 | `semantic.k:96` | Select false branch. | Correct; disjoint from rule 12 by Boolean constructor. |
| 14 | `semantic.k:98-99` | Evaluate a `For` iterable once and create a loop over its values. | Correct for both target loops. |
| 15 | `semantic.k:100` | Finish an empty `forValues`. | Correct zero-iteration boundary. |
| 16 | `semantic.k:101-102` | Bind the next loop value, execute the body, then continue with the tail. | Correct left-to-right loop control and persistent loop binding. |
| 17 | `semantic.k:104-105` | Model `list.append` by replacing the named immutable-list binding. | Correct for `result.append(maximum)`; receiver and argument are pure name lookups. |
| 18 | `semantic.k:107-110` | Evaluate the return expression, terminate remaining function control, clear internal cells, and set the observable result. | Correct in all reachable configurations of this top-level-only target. It is not a general nested-call/stack semantics, but no target operation requires one. |

## Function/equational rules

| # | Source | Equation | Static assessment |
|---:|---|---|---|
| 19 | `semantic.k:115` | `lookupPy` finds a unique map binding. | Correct because K maps have unique keys; missing keys stay stuck. |
| 20 | `semantic.k:117` | Evaluate integer literal. | Correct. |
| 21 | `semantic.k:118` | Evaluate string literal. | Correct. |
| 22 | `semantic.k:119` | Evaluate a name through `lookupPy`. | Correct. |
| 23 | `semantic.k:120` | Evaluate the empty list literal. | Correct; the submitted program has no nonempty list literal. |
| 24 | `semantic.k:121-122` | Evaluate explicit `" "` string split through `splitSpaces`. | Correct for `str.split(" ")`, including empty fields. |
| 25 | `semantic.k:123-124` | Evaluate `==` through `eqPy`. | Correct for the target's string comparison. |
| 26 | `semantic.k:125-126` | Evaluate `>` through `gtPy`. | Correct for the target's integer comparison. |
| 27 | `semantic.k:129` | Extract a string from `pyStr`. | Correct; other value types stay stuck. |
| 28 | `semantic.k:132` | Extract a Boolean from `pyBool`. | Correct but unused by the target. |
| 29 | `semantic.k:135` | String equality. | Correct. |
| 30 | `semantic.k:136` | Integer equality. | Correct but unused; disjoint from rule 29 by constructors. |
| 31 | `semantic.k:139` | Integer greater-than. | Correct. |
| 32 | `semantic.k:142` | Integer addition. | Correct. |
| 33 | `semantic.k:145` | Integer subtraction. | Correct. |
| 34 | `semantic.k:148` | Append a value to a `pyList` through `appendVals`. | Correct. |
| 35 | `semantic.k:151` | Append to empty `PyVals`. | Correct base case. |
| 36 | `semantic.k:152` | Recurse through a nonempty `PyVals` list. | Correct and structurally descending. |
| 37 | `semantic.k:155` | Iterate over a `pyList`. | Correct for the outer loop. |
| 38 | `semantic.k:156` | Iterate over a `pyStr` through `chars`. | Correct for the inner loop; disjoint from rule 37. |
| 39 | `semantic.k:159` | Empty string has no characters. | Correct base case. |
| 40 | `semantic.k:160-162` | Emit the first character and recurse on the suffix when length is positive. | Correct and length-descending on the ASCII parenthesis domain. |
| 41 | `semantic.k:166-167` | If no space is found, split result is the whole string as one field. | Correct for explicit-separator Python split, including `"" -> [""]`. |
| 42 | `semantic.k:168-172` | Emit text before the next space and recurse after it. | Correct; suffix length strictly decreases. Guard is disjoint from and exhaustive with rule 41 because `findString` is negative iff not found. |
| 43 | `verification.k:10-29` | `solutionProgram` expands to the full target constructor tree. | Truthful definitional summary. Mechanical normalized KAST comparison is byte-identical to the trusted regeneration. It does not encode an answer or bypass body execution. |

There are no overlapping right-hand sides requiring priority. Recursive
functions (`appendVals`, `chars`, `splitSpaces`) descend structurally or by
strictly shorter strings. Partial functions have no totality declaration, so
unmodeled sorts or constructs remain stuck instead of acquiring fabricated
values.

## Actual-program construct coverage

| Submitted constructor/form | Declaration | Material behavior |
|---|---|---|
| `Module`, statement lists | `semantic.k:6,8` | rules 1-3 |
| `ImportFrom("typing","List")` | `semantic.k:15` | rule 4 |
| `FuncDef`, `Params` | `semantic.k:13,16` | rules 5-7 |
| `Assign`, `Name`, `Int`, `Str`, empty `ListExpr` | `semantic.k:17,24-27` | rules 8, 19-23 |
| `Attribute`, `Call(...split...)` | `semantic.k:28-29` | rules 24, 27, 41-42 |
| outer and inner `For` | `semantic.k:19` | rules 14-16, 37-40 |
| `If`, `Compare`, `CmpOp("==",...)`, `CmpOp(">",...)` | `semantic.k:20,30,32` | rules 11-13, 25-26, 29, 31 |
| `AugAssign` with `+` and `-` | `semantic.k:18` | rules 9-10, 32-33 |
| `Expr(...append...)` | `semantic.k:21` | rules 17, 34-36 |
| `Return` | `semantic.k:22` | rule 18 |

Every constructor in regenerated `solution.mpy` is covered. The only erased
source details are type annotations and the typing-only import's runtime
binding; neither affects this function's value or control. No local rule
supplies the maximum-depth answer, introduces an oracle, or shortcuts either
loop.
