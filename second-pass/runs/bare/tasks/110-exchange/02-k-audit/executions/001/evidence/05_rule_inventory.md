# Independent rule and declaration inventory

Line numbers refer to the copied candidate sources in
`/tmp/audit-work/110-exchange`, which are byte copies of the submitted K source.

## Local syntax declarations

`semantic.k` declares:

1. `Ids ::= List{String, ","}` (line 8) and `Params(String-list)` (line 9).
2. `Exprs ::= List{Expr, ","}` (line 11), `CmpOp(String, Expr)` (line 12),
   and `CmpOps ::= List{CmpOp, ","}` (line 13).
3. `Expr` constructors `Int`, `Str`, `Name`, `BinOp`, `Compare`, and `Call`
   (lines 15–20).
4. `Stmts ::= List{Stmt, ""}` (line 22) and `Stmt` constructors `Module`,
   `FuncDef`, `Assign`, `If`, `For`, and `Return` (lines 23–28).
5. `PyList` constructors `Nil` and `Cons(Int, PyList)` (lines 30–31).
6. `Val ::= Int | String | Bool | PyList` (line 32).
7. `Result ::= noResult | Val` (line 33).
8. The control `KItem` constructors `init`, `exec`, `eval`, `write`,
   `binRight`, `applyBin`, `cmpRight`, `applyCmp`, `doLen`, `branch`,
   `startFor`, `loop`, and `finish` (lines 43–55).
9. `length(PyList):Int [function,total]` (line 57).

`verification.k` declares:

1. `countBody:Stmts [macro]` (line 6).
2. `solutionProgram:Stmt [macro]` (line 12).
3. `evenBit(Int):Int [function,total]` (line 24).
4. `countEven(PyList):Int [function,total]` (line 28).
5. `lastValue(PyList,Int):Int [function,total]` (line 32).

There are no local `[functional]`, `[simplification]`, `[opaque]`, or
uninterpreted declarations. The only local priority attribute is
`[priority(40)]` on semantic rule S10 below.

## Ordinary semantic rules

| ID | Source | Rule | Independent decision |
|---|---|---|---|
| S01 | `semantic.k:58` | `length(Nil) => 0` | Sound base equation. |
| S02 | `semantic.k:59` | `length(Cons(_,REST)) => 1 + length(REST)` | Sound, structurally decreasing equation. S01/S02 are disjoint and exhaustive for `PyList`. |
| S03 | `semantic.k:68–75` | Exact `exchange(lst1,lst2)` initialization | Sound external-call wrapper for this one submitted function. It pins the function name and parameter names, binds the two argument lists, and starts the real body. It eagerly creates `even` and `value`; the latter differs from an unbound Python local on a zero-iteration loop but cannot affect this program's result. |
| S04 | `semantic.k:77` | Empty statement list finishes | Sound sequencing base case. |
| S05 | `semantic.k:78–79` | Assignment evaluates RHS, writes target, then continues | Sound left-to-right assignment for the only supported target form used here (`Name`). |
| S06 | `semantic.k:80–81` | `write` updates the named map entry | Sound state update; all other bindings and cells are preserved. |
| S07 | `semantic.k:83–84` | `If` evaluates guard, branches, then continues | Sound evaluation/control order. |
| S08 | `semantic.k:85` | True branch executes `THEN` | Sound. |
| S09 | `semantic.k:86` | False branch executes `ELSE` | Sound; S08/S09 are disjoint and exhaustive for the Boolean guards produced by this program. |
| S10 | `semantic.k:91–99` | Prioritized parity-counting shortcut | Operational bridge. For integer bindings it has the same environment, result, and continuation effect as S07–S09 plus S05/S06: add one iff `I % 2 == 0`, otherwise preserve `N`. `evenBit` is fully defined, not opaque. The auditor removed S10 and proved both exhaustive branches in the exact reachable identifier/state context with arbitrary `REST` and `CONT` (`05-kprove-parity-bridge-actual-context.log`, `#Top`). All original claims also close without S10 (`05-kprove-all-without-parity-bridge.log`). A broader symbolic connection attempt stopped only on K Map normalization, not on a false value/control witness (`05-kprove-parity-bridge-connection.log` and `05-kprove-parity-bridge-generic-execution.log`). No false-conclusion witness exists: the equation is ordinary parity arithmetic wherever the rule matches. |
| S11 | `semantic.k:101–102` | `For` evaluates iterable, then starts loop, then continues | Sound evaluation/control order for the list iterables used here. |
| S12 | `semantic.k:103–104` | A `PyList` starts `loop` | Sound type bridge. |
| S13 | `semantic.k:105` | Loop on `Nil` terminates | Sound base case. |
| S14 | `semantic.k:106–107` | Loop on `Cons` writes element, executes body, recurs | Sound Python-list iteration order and persistent final loop variable. |
| S15 | `semantic.k:109–110` | `Return` drops later statements and evaluates return expression | Sound abrupt return scheduling. |
| S16 | `semantic.k:111–112` | `finish` stores value and clears the remaining function computation | Sound for this function-level model; it prevents the following `Return("NO")` after the `YES` return. |
| S17 | `semantic.k:114` | Integer literal evaluates to its integer | Sound. |
| S18 | `semantic.k:115` | String literal evaluates to its string | Sound. |
| S19 | `semantic.k:116–117` | Name lookup reads the environment | Sound for bound names. An unbound used name visibly sticks rather than fabricating a value. |
| S20 | `semantic.k:119–120` | Binary operation evaluates left first | Sound Python evaluation order. |
| S21 | `semantic.k:121–122` | Then evaluate binary RHS | Sound. |
| S22 | `semantic.k:123–124` | Integer `+` | Sound; K and Python integers are unbounded here. |
| S23 | `semantic.k:125–126` | Integer `%` | Sound on the submitted divisor `2`; a zero divisor is outside the used construct instances and would not fabricate a result. Checking equality with zero also agrees for negative even/odd integers. |
| S24 | `semantic.k:128–129` | Comparison evaluates left first | Sound. |
| S25 | `semantic.k:130–131` | Then evaluate comparison RHS | Sound. |
| S26 | `semantic.k:132–133` | Integer equality | Sound. |
| S27 | `semantic.k:134–135` | Integer greater-than-or-equal | Sound. |
| S28 | `semantic.k:137–138` | Exact built-in `len` call evaluates its argument | Sound for the one used built-in/binding. Other calls remain visibly unmodeled. |
| S29 | `semantic.k:139` | `len(PyList)` uses `length` | Sound. |

## Verification equations and macros

| ID | Source | Rule | Independent decision |
|---|---|---|---|
| V01 | `verification.k:7–10` | `countBody` macro expansion | Exact textual abstraction of both submitted loop bodies. |
| V02 | `verification.k:13–22` | `solutionProgram` macro expansion | Exact complete AST; fresh `kast --expand-macros` comparison with submitted and trusted-regenerated `solution.mpy` has identical SHA-256. A body mutation is rejected by this pin. |
| V03 | `verification.k:25` | `evenBit(I)=1` when remainder is zero | True parity branch. |
| V04 | `verification.k:26` | `evenBit(I)=0` otherwise | True complementary branch. V03/V04 are disjoint and exhaustive for every K `Int`. |
| V05 | `verification.k:29` | `countEven(Nil)=0` | Sound base equation. |
| V06 | `verification.k:30` | `countEven(Cons(I,R))=evenBit(I)+countEven(R)` | Sound, structurally decreasing equation. V05/V06 are disjoint and exhaustive. |
| V07 | `verification.k:33` | `lastValue(Nil,D)=D` | Sound base equation. |
| V08 | `verification.k:34` | `lastValue(Cons(I,R),_)=lastValue(R,I)` | Sound, structurally decreasing equation. V07/V08 are disjoint and exhaustive. |

## Claim/circularity inventory

1. `SPEC.loop-counts-even` (`spec.k:6–21`) is the loop circularity. It consumes
   the exact real loop body, preserves arbitrary `CONT`, adds exactly
   `countEven(L)` to `even`, and leaves `value` at the last iterated element
   (or its old value for `Nil`).
2. `SPEC.exchange-yes` (`spec.k:23–35`) executes `solutionProgram` from the
   initial configuration and constrains both final state and result to `"YES"`
   when the total even count is at least `length(L1)`.
3. `SPEC.exchange-no` (`spec.k:37–49`) has the complementary strict
   precondition and constrains the final result to `"NO"`.

## Submitted-program construct coverage

Every constructor in `solution.mpy` is mapped:

| Used construct | Declaration | Execution |
|---|---|---|
| `Module(FuncDef(...))`, `Params` | `semantic.k:9,23–24` | S03 |
| statement list | `semantic.k:22` | S04 plus sequencing in S05/S07/S11/S15 |
| `Assign(Name(...),...)` | `semantic.k:17,25` | S05/S06 |
| `For(Name(...),Name(...),...)` | `semantic.k:27` | S11–S14 |
| `If` | `semantic.k:26` | S07–S10 |
| `Return` | `semantic.k:28` | S15/S16 |
| `Int`, `Str`, `Name` | `semantic.k:15–17` | S17–S19 |
| `BinOp("+",...)`, `BinOp("%",...)` | `semantic.k:18` | S20–S23 |
| `Compare`/`CmpOp("==",...)`/`CmpOp(">=",...)` | `semantic.k:12–13,19` | S24–S27 |
| `Call(Name("len"),...)` | `semantic.k:20` | S28/S29 |

The configuration contains only `<k>`, `<env>`, and `<result>`, exactly the
control, local state, and observable return result needed by this program.
There is no heap, allocation, I/O, exception state, or external call other than
the exact modeled `len`.
