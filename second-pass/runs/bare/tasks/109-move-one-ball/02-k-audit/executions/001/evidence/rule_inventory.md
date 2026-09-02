# Exhaustive local K inventory and static decisions

This inventory covers the candidate-authored `mpy-syntax.k`, `semantic.k`,
`verification.k`, and `spec.k`. Imported K standard-library declarations are
listed separately as the trust boundary.

## Syntax, attributes, and configuration

`mpy-syntax.k` declares:

- `Pgm`: `Module(Stmts)` and zero-arity `theSolution`.
- `Stmts`: `List{Stmt, ""}`.
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`, and `For`.
- `Params`: one `String`.
- `Expr`: `Name`, `Int`, `Bool`, `UnaryOp`, `BinOp`, `Compare`, `Call`, and
  `Subscript`.
- `CmpOp`: a string-tagged right operand.
- `IList`: `.IList` and `Int "::" IList`.
- `theSolution` has `[function, total]`. It is zero-arity and has exactly one
  defining equation, so coverage and non-overlap are immediate.

`semantic.k` declares:

- `Value`: `iVal(Int)`, `bVal(Bool)`, and `listVal(IList)`.
- `KItem`: `exec`, `execStmt`, `eval`, `branch`, `assignTo`, `addRight`,
  `addValues`, `compareRight`, `compareValues`, `getLength`, `getLast`,
  `isEmpty`, `startFor`, `loop`, `bind`, and `doReturn`.
- Configuration cells: `<k>` contains `$PGM:Pgm`; `<input>` contains
  `$INPUT:IList`; `<env>` starts as `.Map`. Every cell is read or preserved by
  execution rules.

`verification.k` declares:

- `[function,total]`: `length`, `dropBit`, `dropsFrom`, `cyclicDrops`, and
  `rotationSortable`.
- `[function]` but intentionally not `[total]`: `last`, whose domain is
  nonempty `IList`.

There are no candidate-authored `[functional]`, `[simplification]`,
`[concrete]`, opaque, fresh-symbol, or priority declarations other than the
single `[priority(40)]` rule M30. Rule M13 has `[owise]`. No auxiliary claims
exist; `spec.k` contains exactly the two entry claims C1 and C2.

## Rule-by-rule decisions

All “sound” decisions below are scoped to the submitted program and `IList`
integer inputs, the stated scope of this generated minimal semantics.

| ID | Candidate location | Rule/equation | Static decision |
|---|---|---|---|
| X1 | `mpy-syntax.k:32` | `theSolution` expands to the full constructor tree | Sound and program-pinning. The tree is the submitted `solution.mpy`; trusted regeneration is byte-identical. |
| M1 | `semantic.k:28` | sole unary `Module(FuncDef(...))` starts its body and binds input | Sound for the exact one-function submitted module. It is deliberately not a general Python import/call semantics. |
| M2 | `semantic.k:32` | empty statement sequence finishes | Sound. |
| M3 | `semantic.k:33` | statement head executes before tail | Sound sequential order. |
| M4 | `semantic.k:35` | assignment evaluates RHS before storing | Sound for the used name target. |
| M5 | `semantic.k:36` | assignment updates the named environment key | Sound; K `Map` update is the state change. |
| M6 | `semantic.k:39` | `If` evaluates its guard first | Sound evaluation order. |
| M7 | `semantic.k:40` | true guard selects then-branch | Sound. |
| M8 | `semantic.k:41` | false guard selects else-branch | Sound. |
| M9 | `semantic.k:43` | `For(Name(X), E, BODY)` evaluates iterable first | Sound for the used list iteration. |
| M10 | `semantic.k:45` | list value becomes `loop` | Sound. |
| M11 | `semantic.k:46` | empty list ends a loop | Sound. |
| M12 | `semantic.k:51` | exact submitted loop body folds to `dropsFrom`, final `last`, and final `value` | Sound operational bridge. It matches the entire body, reads `drops`/`previous`, preserves the arbitrary continuation/input/other bindings, and writes exactly `drops`, `previous`, and `value`. Reviewer theorem `loop-connection-spec.k`, proved against M13/M14 plus ordinary statement rules with `#Top`, validates its complete domain. Concrete continuation and body-sensitivity tests also agree. |
| M13 | `semantic.k:66` | other nonempty loops bind head, execute body, recurse | Sound small-step list iteration; `[owise]` makes it complementary to M12. |
| M14 | `semantic.k:69` | loop binding updates the environment | Sound. |
| M15 | `semantic.k:72` | return evaluates its expression | Sound. |
| M16 | `semantic.k:73` | return with a continuation discards the continuation | Sound for the single active function body: Python return exits the function. No call stack is modeled or used. |
| M17 | `semantic.k:74` | final return marker yields the value | Sound. |
| M18 | `semantic.k:76` | integer literal to `iVal` | Sound. |
| M19 | `semantic.k:77` | Boolean literal to `bVal` | Sound. |
| M20 | `semantic.k:78` | name lookup from environment | Sound for bound names; unbound names remain visibly stuck. |
| M21 | `semantic.k:81` | the used unary `-Int(I)` is integer negation | Sound. |
| M22 | `semantic.k:83` | used `+` evaluates left before right | Sound Python order. |
| M23 | `semantic.k:85` | after left integer, evaluate right | Sound. |
| M24 | `semantic.k:86` | add integer values | Sound; K integers match Python arbitrary-precision integers here. |
| M25 | `semantic.k:88` | comparison evaluates left before right | Sound. |
| M26 | `semantic.k:90` | after left value, evaluate right | Sound. |
| M27 | `semantic.k:92` | integer `==` | Sound. |
| M28 | `semantic.k:93` | integer `>` | Sound. |
| M29 | `semantic.k:94` | integer `<=` | Sound. |
| M30 | `semantic.k:97` | exact `len(E) == 0` goes through structural `isEmpty`, priority 40 | Sound and overlapping-but-consistent with M25/M33/M34/M27. The priority is needed for symbolic constructor splitting; both paths agree on every ground `IList`. |
| M31 | `semantic.k:100` | empty `IList` is empty | Sound. |
| M32 | `semantic.k:101` | cons `IList` is nonempty | Sound; disjoint from M31. |
| M33 | `semantic.k:103` | `len(E)` evaluates `E` | Sound for the only used built-in binding. The minimal semantics fixes textual `len`; shadowing is outside the submitted module. |
| M34 | `semantic.k:104` | list length calls `length` | Sound by V1–V2. |
| M35 | `semantic.k:106` | used subscript form `E[-1]` evaluates `E` | Sound for the only used subscript. |
| M36 | `semantic.k:107` | nonempty list `[-1]` yields `last` | Sound on the reachable nonempty branch. Empty use would visibly remain stuck because `last(.IList)` has no rule, rather than fabricate a value. |
| V1 | `verification.k:16` | `length(.IList) = 0` | Sound base case. |
| V2 | `verification.k:17` | cons length is one plus tail length | Sound, disjoint from V1, structurally decreasing; V1–V2 make `length` total. |
| V3 | `verification.k:19` | singleton `last` | Sound. |
| V4 | `verification.k:20` | drop first element when finding `last` | Sound, disjoint from V3 and structurally decreasing. V3–V4 cover exactly nonempty lists; no false totality claim is made. |
| V5 | `verification.k:22` | `dropBit(I,J)=1` when `I>J` | Sound. |
| V6 | `verification.k:23` | `dropBit(I,J)=0` when `I<=J` | Sound; K integer order makes V5/V6 disjoint and exhaustive. |
| V7 | `verification.k:25` | no remaining values means zero further drops | Sound. |
| V8 | `verification.k:26` | count current strict descent then recurse | Sound, disjoint from V7, structurally decreasing; V7–V8 make `dropsFrom` total. |
| V9 | `verification.k:29` | empty list has zero cyclic drops | Sound. |
| V10 | `verification.k:30` | nonempty cyclic count starts from the last element | Sound and disjoint from V9; `last` is used only in its domain. |
| V11 | `verification.k:34` | `rotationSortable(L)` is defined as `cyclicDrops(L) <= 1` | Sound as a transparent mathematical definition, not an oracle. Its equivalence to existence of a sorted right rotation for unique inputs is an informal intent bridge, independently tested but not itself a K theorem. |
| C1 | `spec.k:7` | empty input returns true and binds only `arr` | Result-constraining, satisfiable, and exact. |
| C2 | `spec.k:13` | every nonempty integer list returns `rotationSortable` and fixes final loop bindings | Result- and state-constraining, satisfiable, universal over `I::IS`, and exact. It is stronger than the prompt in allowing duplicates, while remaining sound for the intended unique domain. |

## Submitted-constructor coverage

| `solution.mpy` construct | Declaration | Operational coverage |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `mpy-syntax.k:7,9,14` | M1 |
| statement sequence | `mpy-syntax.k:8` | M2–M3 |
| `If` | `mpy-syntax.k:12` | M6–M8 |
| `Assign(Name, ...)` | `mpy-syntax.k:11,16` | M4–M5 |
| `For(Name, Name, body)` | `mpy-syntax.k:13` | M9–M14 |
| `Return` | `mpy-syntax.k:10` | M15–M17 |
| `Name`, `Int`, `Bool` | `mpy-syntax.k:16-18` | M18–M20 |
| unary `-` in `arr[-1]` | `mpy-syntax.k:19,23` | M21, M35–M36 |
| binary `+` | `mpy-syntax.k:20` | M22–M24 |
| comparisons `==`, `>`, `<=` | `mpy-syntax.k:21,24` | M25–M32 |
| `Call(Name("len"), Name("arr"))` | `mpy-syntax.k:22` | M30–M34 |

Every constructor and string-tagged operator appearing in submitted
`solution.mpy` has a rule path. Unsupported unused constructs are absent, as
permitted for generated minimal semantics.

## Imported trust boundary

The proof relies on K's standard `INT`, `BOOL`, and `MAP` implementations:
arbitrary-precision integer arithmetic/order/equality, Boolean connectives, map
lookup/update and key membership, associative map matching, K sequencing
(`~>`), and reachability/circularity soundness. No candidate-authored opaque
symbol or external oracle exists.

