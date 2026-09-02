# Exhaustive local K inventory and disposition

This inventory covers every local K source artifact in `/candidate`: `semantic.k`,
`verification.k`, and `spec.k`. There are no other candidate `.k` files.

## Syntax, configuration, and attributes

| ID | File:lines | Declaration | Use and disposition |
|---|---|---|---|
| S01 | `semantic.k:12-13` | `IntList ::= nil \| cons(Int,IntList)` | Inductive finite integer-list model; used by all inputs and summaries; sound. |
| S02 | `semantic.k:14-18` | `Value ::= pyInt \| pyBool \| pyList \| funref \| builtin` | Exactly the immutable runtime values needed by this program; sound minimal model. |
| S03 | `semantic.k:19` | comma-separated `Values` | Holds the single entry argument and call arguments; sound. |
| S04 | `semantic.k:20` | comma-separated `Strings` | Holds the one parameter; sound. |
| S05 | `semantic.k:21` | `Depth ::= z \| s(Depth)` | Structural call-depth bookkeeping used in frames and claims; sound. |
| S06 | `semantic.k:24` | `Program ::= Module(Stmts)` | Matches the trusted translator's outer constructor. |
| S07 | `semantic.k:25` | `Params ::= Params(Strings)` | Matches both one-parameter functions. |
| S08 | `semantic.k:26` | juxtaposed `Stmts` list | Matches translated sequential bodies and their empty branches. |
| S09 | `semantic.k:27-30` | `Stmt ::= FuncDef \| If \| Assign \| Return` | Exactly all submitted statement constructors. |
| S10 | `semantic.k:31` | comma-separated `Exprs` | Supports one- and two-argument calls used by the program. |
| S11 | `semantic.k:32-37` | `Expr ::= Int \| Name \| Call \| BinOp \| Compare \| Subscript` | Exactly all submitted expression constructors. |
| S12 | `semantic.k:38` | juxtaposed `CmpOps` | Submitted program uses one comparison operand. |
| S13 | `semantic.k:39` | `CmpOp(String,Expr)` | Submitted program uses only `==`. |
| S14 | `semantic.k:40` | `Index ::= Expr \| Slice` | Submitted program uses literal `0` and one slice. |
| S15 | `semantic.k:41` | `Slice(Bound,Bound,Bound)` | Submitted program uses `[1:]`. |
| S16 | `semantic.k:42` | `Bound ::= Expr \| NoBound` | Represents the literal lower bound and omitted upper/step. |
| S17 | `semantic.k:53` | `Function ::= closure(Params,Stmts)` | Program-defined function representation; bodies remain executable. |
| S18 | `semantic.k:54` | `Frame ::= frame(Map,K)` | Saves caller locals and exact caller continuation. |
| S19 | `semantic.k:56-75` | 20 internal `KItem` constructors | Scheduling, calls, returns, binary/comparison evaluation, singleton test, head, and tail controls; each is consumed by R01-R41 below. |
| CFG | `semantic.k:77-86` | `<py>` containing `<k>`, `<entry>`, `<args>`, `<functions>`, `<env>`, `<callStack>`, `<callDepth>` | All cells are read or written. The model needs no heap, I/O, exceptions, or mutable aggregate state for this program. |
| F01 | `semantic.k:173` | `length(IntList) [function]` | Equations R42-R43 are disjoint, exhaustive, and structurally descending. |
| F02 | `semantic.k:174` | `intMin(Int,Int) [function]` | Equations R44-R45 have disjoint/exhaustive guards over mathematical integers. |
| F03 | `verification.k:11` | `minPrefix(IntList) [function]` | V01-V02 cover all and only non-empty lists and descend structurally. Partial on `nil`, which is never used by a claim. |
| F04 | `verification.k:12` | `minSubarray(IntList) [function]` | V03-V04 cover all and only non-empty lists and descend structurally. Partial on `nil`, which is never used by a claim. |
| F05 | `verification.k:24` | constant `solutionFunctions : Map [function]` | Single equation V05; constructor-identical to the two submitted `FuncDef` bodies. |
| F06 | `verification.k:47` | constant `solutionProgram : Program [function]` | Single equation V06; KAST-identical to submitted `solution.mpy`. |

There are exactly six local `[function]` declarations. There are no local
`[total]`, `[functional]`, `[simplification]`, `[concrete]`, `context`, or
`alias` declarations, and no opaque local function without defining equations.
There is exactly one priority attribute: R35 has `[priority(40)]`.

## `semantic.k` rules

| ID | Lines | Rule role | Static disposition |
|---|---:|---|---|
| R01 | 89-91 | Load `Module`, schedule all definitions, then invoke configured entry/args. | Sound; guarantees definitions execute before invocation. |
| R02 | 93 | `exec(.Stmts) => .K`. | Sound empty-sequence identity. |
| R03 | 94 | Schedule head statement then remaining statements. | Sound left-to-right statement order. |
| R04 | 96-97 | Store a `FuncDef` closure in `<functions>`. | Sound for module-level capture-free functions used here. |
| R05 | 99 | Convert configured `invoke(F,V)` to user-function application. | Sound for the single-argument target. |
| R06 | 102 | Evaluate `If` guard before selecting a branch. | Sound evaluation order. |
| R07 | 103 | True selects `THEN`. | Sound and disjoint from R08. |
| R08 | 104 | False selects `ELSE`. | Sound and disjoint from R07. |
| R09 | 106 | Evaluate assignment RHS before store. | Sound evaluation order for a `Name` target. |
| R10 | 107-108 | Update the current local map with evaluated value. | Sound for `tail_min` and `prefix_min`. |
| R11 | 110 | Evaluate return expression before abrupt return. | Sound. |
| R12 | 111-114 | Discard the current function continuation, restore caller locals/continuation from top frame, decrement depth, and emit `returned`. | Sound abrupt-return behavior for every reachable call frame; all affected cells are explicit. |
| R13 | 115 | Make a `returned` marker transparent as its value when caller evaluation resumes. | Sound internal marker elimination. |
| R14 | 118 | Translate `Int(I)` to `pyInt(I)`. | Sound; K `Int` is arbitrary precision like Python integers. |
| R15 | 119-120 | Resolve a name from current locals. | Sound on reachable states. Potential overlap with R16-R18 requires a colliding binding, which the submitted bodies never create. |
| R16 | 121-122 | Resolve a name from the function map. | Sound on reachable states; the map contains only the two submitted function names. |
| R17 | 123 | Resolve `len` as a builtin. | Sound on reachable states; neither locals nor function map binds `len`. |
| R18 | 124 | Resolve `min` as a builtin. | Sound on reachable states; neither locals nor function map binds `min`. |
| R19 | 128 | Start one-argument call by evaluating callee. | Sound left-to-right order. |
| R20 | 129 | After callee, evaluate its sole argument. | Sound. |
| R21 | 130 | Apply callee to evaluated sole argument. | Sound. |
| R22 | 132 | Start two-argument call by evaluating callee. | Sound left-to-right order. |
| R23 | 133 | Evaluate first argument after callee. | Sound. |
| R24 | 134 | Evaluate second argument after first. | Sound. |
| R25 | 135 | Apply callee after both arguments. | Sound. |
| R26 | 139-143 | Enter a one-parameter closure, install parameter local, save caller locals/exact continuation, increment depth. | Sound for both submitted functions; bodies execute rather than being replaced by an oracle. |
| R27 | 145 | Builtin `len(pyList(L)) = pyInt(length(L))`. | Sound trusted primitive over modeled lists. |
| R28 | 146 | Binary integer `min = intMin`. | Sound trusted primitive over modeled integers. |
| R29 | 149 | Start binary expression by evaluating left operand. | Sound. |
| R30 | 150 | Evaluate right operand after left. | Sound. |
| R31 | 151 | Integer `+` uses K integer addition. | Sound. |
| R32 | 153 | Start single comparison by evaluating left operand. | Sound. |
| R33 | 154 | Evaluate comparison RHS after left. | Sound. |
| R34 | 155 | Integer equality returns modeled Boolean. | Sound. |
| R35 | 160-161 | Priority-40 fused `len(E) == 1`: evaluate `E` once, then `singletonTest`. | Operational acceleration. For every reachable program state, `E` is `Name("nums")` bound to a non-empty `IntList`; R36-R37 equal generic R27/R42-R43/R34 behavior. On an out-of-domain empty list the fused path sticks where the generic path would produce `false`; this is incompleteness, not a false conclusion on the intended domain. A bridge-free rebuild agreed on all eight recorded intended-domain cases, but no candidate universal connection claim exists. |
| R36 | 162 | Singleton non-empty list tests true. | Sound and disjoint from R37. |
| R37 | 163 | List with at least two elements tests false. | Sound and disjoint from R36; exhaustive for non-empty `IntList`. |
| R38 | 166 | Evaluate base of literal index `0`. | Sound; skipped index literal evaluation is inert. |
| R39 | 167 | Head of non-empty integer list. | Sound on all reachable uses; intentionally undefined on empty. |
| R40 | 169-170 | Evaluate base of exact slice `[1:]`. | Sound; skipped literal/omitted-bound evaluation is inert. |
| R41 | 171 | Tail result for a non-empty modeled list. | Sound on all reachable uses; Python slice of empty would be empty, but no intended execution slices empty. |
| R42 | 175 | `length(nil) = 0`. | Sound. |
| R43 | 176 | `length(cons(_,T)) = 1 + length(T)`. | Sound structural recursion. |
| R44 | 177 | `intMin(I,J)=I` when `I <= J`. | Sound. |
| R45 | 178 | `intMin(I,J)=J` when `I > J`. | Sound; disjoint from and exhaustive with R44. |

## `verification.k` equations

| ID | Lines | Equation | Static disposition |
|---|---:|---|---|
| V01 | 13 | `minPrefix([H]) = H`. | Correct base case. |
| V02 | 14-15 | `minPrefix(H::J::T) = min(H, H + minPrefix(J::T))`. | Correct exhaustive decomposition of non-empty prefixes and structurally descending. |
| V03 | 16 | `minSubarray([H]) = H`. | Correct base case. |
| V04 | 17-19 | `minSubarray(H::J::T) = min(minSubarray(J::T), minPrefix(H::J::T))`. | Correct exhaustive decomposition: a subarray either starts at `H` or lies wholly in the tail; structurally descending through the first operand and V02. |
| V05 | 25-45 | `solutionFunctions` map. | Definitional program constant, not an oracle. K parser comparison proves names, parameters, and both bodies match submitted `FuncDef`s. |
| V06 | 48-69 | `solutionProgram` module term. | Definitional program constant. After normalizing concrete empty statement lists to `.Stmts`, KAST is identical to trusted regeneration of `solution.mpy`. |

V01-V04 state ordinary mathematics and never rewrite an executing source term.
V05-V06 name exact submitted syntax; source-body sensitivity is demonstrated by
the separate mutation that changed V06's executed singleton branch and caused
the proof to get stuck at `pyInt(1)`.

## `spec.k` claims

| ID | Lines | Plain-language pre/postcondition and disposition |
|---|---:|---|
| C01 | 8-18 | For every integer `H`, finite `T`, caller continuation, environment, stack, and depth, calling the exact `min_prefix_sum` closure on non-empty `H::T` returns `minPrefix(H::T)` and restores caller state. This is the helper circularity. |
| C02 | 21-31 | Under the same universal caller framing, calling the exact target closure on non-empty `H::T` returns `minSubarray(H::T)`. It uses C01 and itself as circularities. |
| C03 | 35-45 | From empty loader state, execute `solutionProgram` with target entry and one non-empty integer-list argument; consume computation and end with exactly `pyInt(minSubarray(H::T))`, the exact two-function map, empty environment/stack, and depth `z`. It uses C01-C02. |

All three preconditions are satisfiable. Recorded ground instances include
`[4,-5]` for C01/C02 and `[5,-2,-3,7,-10,4]` for C03.

## Submitted-constructor coverage map

| Submitted constructor | Declaration | Operational rules |
|---|---|---|
| `Module` | S06 | R01 |
| `FuncDef`, `Params`, statement sequence | S07-S09 | R02-R04 |
| `If` | S09 | R06-R08 |
| `Assign(Name,...)` | S09/S11 | R09-R10 |
| `Return` | S09 | R11-R13 |
| `Int`, `Name` | S11 | R14-R18 |
| unary/binary `Call` | S10-S11 | R19-R28 |
| `BinOp("+",...)` | S11 | R29-R31 |
| `Compare(...,CmpOp("==",...))` | S11-S13 | R32-R37 |
| `Subscript(...,Int(0))` | S11/S14 | R38-R39 |
| `Subscript(...,Slice(Int(1),NoBound,NoBound))` | S11/S14-S16 | R40-R41 |

Every constructor in submitted `solution.mpy` is declared and has a reachable
behavioral path. No answer-encoding rule, fresh result-bearing oracle,
simplification axiom, or unmodeled used constructor was found.
