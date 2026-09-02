# Exhaustive local declaration and rule inventory

Source under review: scratch copies of `semantic.k`, `verification.k`, and
`spec.k` from `/candidate`. Imported K built-ins are listed as trust
boundaries, not re-inventoried here.

## Syntax, attributes, and configuration

`MPY-SYNTAX`:

1. `Pgm`: `Module(Stmts)` and the proof-readable nullary
   `correctProgram()`.
2. `Stmts`: generated empty-separator statement list plus
   `targetLoopBody()` and `targetTail()`. The latter two are both
   `[function, total]`.
3. `Strings`: generated comma-separated `String` list.
4. `Params`: `Params(Strings)`.
5. `Stmt`: `FuncDef`, `Assign`, `For`, `If`, and `Return`.
6. `Expr`: `Name`, `Int`, `Bool`, `Str`, `BinOp`, and `Compare`.
7. `CmpOp`: a string operator and right expression.

`MPY`:

1. `Value`: `IVal`, `BVal`, `SVal`, and the proof-only surrogate
   `SeqVal(BracketSeq)`.
2. `Function`: parameter/body pair.
3. `Store`: `emptyStore` or shadowing `bind`.
4. `lookup(String, Store)`: partial `[function]`.
5. `KItem`: `invoke`, `functionBoundary`, `assignName`, `binopLeft`,
   `binopRight`, `compareLeft`, `compareRight`, `ifKont`, `forStart`,
   `forString`, `forBracketSeq`, `returnKont`, and `finish`.
6. Configuration: `<k>` initially receives `$PGM` followed by a top-level
   invocation with `SVal($INPUT:String)`; `<functions>` is a `Map`, `<env>` a
   `Store`, and `<result>` a `Result`.
7. `Result`: `noResult` or `result(Value)`.

`VERIFICATION`:

1. Four `[function, total]` Boolean symbols: `bracketSpec`,
   `bracketEmpty`, `bracketOpen`, and `bracketNegative`.
2. `BracketSeq`: `noBrackets`, `openBracket(BracketSeq)`, and
   `closeBracket(BracketSeq)`.
3. `bracketSeqSpec(BracketSeq, Int)`: `[function, total]`.

There are no local priority declarations, `[simplification]` attributes,
opaque symbols, or trusted claims. K generates list constructors/functions
for `Stmts` and `Strings`.

## `semantic.k`: all 39 local rules

| # | Lines | Rule / role | Audit decision |
|---|---:|---|---|
| 1 | 47 | `lookup` at the newest same-name binding | Sound shadowing lookup. |
| 2 | 48–49 | recurse past a different-name binding | Sound; the guard is disjoint from rule 1. Lookup is intentionally partial on `emptyStore`. |
| 3 | 75 | execute a `Module` as its statements | Sound for the one-function module. |
| 4 | 76–82 | expand `targetLoopBody()` | Exact constructor subtree from regenerated `solution.mpy`; definitional summary. |
| 5 | 83–84 | expand `targetTail()` | Exact final-return subtree; definitional summary. |
| 6 | 88–94 | expand `correctProgram()` | Exact function/module term after rules 4–5 simplify. The mechanical KORE comparison is in `stage4-pinning-witnesses.log`. |
| 7 | 95 | schedule statement-list head before tail | Sound source-order sequencing. |
| 8 | 96 | empty statement list becomes empty computation | Sound. |
| 9 | 98–99 | bind a function definition in `<functions>` | Sound for module-level definition; later definitions overwrite earlier ones as expected. |
| 10 | 101–103 | invoke a one-argument function and replace the environment | Sound for this top-level, single-argument program. It omits caller frames/environment restoration, which are unused by the submitted body. |
| 11 | 105 | integer literal to `IVal` | Sound. |
| 12 | 106 | Boolean literal to `BVal` | Sound. |
| 13 | 107 | string literal to `SVal` | Sound. |
| 14 | 108–109 | name evaluation by current-store lookup | Sound for all used, bound names. |
| 15 | 111 | evaluate assignment RHS before committing | Sound for the used `Name` target. |
| 16 | 112–113 | prepend the evaluated name binding | Sound shadowing assignment. |
| 17 | 115 | evaluate binary left operand first | Sound Python order. |
| 18 | 116 | then evaluate binary right operand | Sound Python order. |
| 19 | 117 | integer addition | Sound; saved `I` is left and current `J` right. |
| 20 | 118 | integer subtraction | Sound; computes left `I - J`. |
| 21 | 120 | evaluate comparison left operand first | Sound. |
| 22 | 121–122 | then evaluate comparison right operand | Sound. |
| 23 | 123–124 | string equality | Sound and symmetric. |
| 24 | 125–126 | integer equality | Sound and symmetric. |
| 25 | 127–128 | integer less-than | Sound; computes saved-left `L < R`. |
| 26 | 130 | evaluate `If` guard first | Sound. |
| 27 | 131 | select true branch | Sound. |
| 28 | 132 | select false branch | Sound; disjoint from rule 27. |
| 29 | 134–135 | evaluate `For` iterable before iteration | Sound. |
| 30 | 136–137 | dispatch a real `SVal` to `forString` | Sound concrete string route. |
| 31 | 138–139 | dispatch proof-only `SeqVal` to `forBracketSeq` | Coherent for the new surrogate datatype, but this is the material representation bridge: no theorem connects this route to rule 30 on corresponding real strings. |
| 32 | 140–141 | terminate `forString` on empty string | Sound. |
| 33 | 142–145 | bind first character, run body, recurse on suffix | Sound for the promised ASCII alphabet; guard is disjoint from rule 32 and the body precedes recursion. |
| 34 | 146 | terminate `forBracketSeq(noBrackets)` | Sound within the surrogate representation. |
| 35 | 147–149 | bind `<`, run body, recurse on open tail | Sound within the surrogate representation. |
| 36 | 150–152 | bind `>`, run body, recurse on close tail | Sound within the surrogate representation. Rules 34–36 are constructor-disjoint and exhaustive for `BracketSeq`. |
| 37 | 154 | evaluate return expression | Sound. |
| 38 | 155–156 | discard the remaining computation and schedule `finish` | Correct for every reachable return in this top-level program: early return discards loop/tail/boundary, final return discards the boundary. It is over-broad for hypothetical nested calls because it ignores `functionBoundary`; no such call construct or intended-domain state is reachable, so this is recorded as a reuse limitation rather than labeled unsound. |
| 39 | 157–158 | write returned value to `<result>` and stop | Sound for top-level invocation. |

## `verification.k`: all 11 local rules

| # | Lines | Rule / role | Audit decision |
|---|---:|---|---|
| 1 | 14 | `bracketSpec` tests for empty string | Truthful start of a recursive checker; unused by every submitted claim. |
| 2 | 15 | empty string returns `D == 0` | Truthful. |
| 3 | 16–17 | nonempty route tests first character for `<` | Truthful when reached from rule 1. |
| 4 | 18–19 | consume `<` and increment | Truthful. |
| 5 | 20–21 | otherwise test whether decrement is negative | Truthful for the prompt alphabet (and matches the Python `else` branch more broadly). |
| 6 | 22 | negative prefix returns false | Truthful and suffix-independent. |
| 7 | 23–24 | nonnegative close consumes a character and decrements | Truthful when reached from rule 5. |
| 8 | 31 | empty `BracketSeq` returns `D == 0` | Truthful. |
| 9 | 32 | open constructor increments and recurses | Truthful. |
| 10 | 33–34 | a close causing negative depth returns false | Truthful; guard is disjoint from rule 11. |
| 11 | 35–36 | otherwise close decrements and recurses | Truthful; the two integer guards are exhaustive. |

The string helper equations decrease string length on every recursive path
reached from `bracketSpec`; the constructor equations decrease `BracketSeq`.
The Boolean-dispatch helper equations are exhaustive in their Boolean
argument. No same-symbol overlaps have disagreeing right-hand sides.

## Construct-to-rule coverage for `solution.mpy`

| Used constructor | Declaration | Operational coverage |
|---|---|---|
| `Module` | `Pgm` | rule 3 |
| `FuncDef`, `Params` | `Stmt`, `Params` | rules 7, 9 |
| `Assign(Name, ...)` | `Stmt`, `Expr` | rules 7, 14–16 |
| `For(Name, Name, body)` | `Stmt` | rules 7, 14, 29–33 for real strings; rules 31 and 34–36 only for the proof surrogate |
| `If` | `Stmt` | rules 7, 26–28 |
| `Return` | `Stmt` | rules 7, 37–39 |
| `Int`, `Bool`, `Str`, `Name` | `Expr` | rules 11–14 |
| `BinOp` with `+`/`-` | `Expr` | rules 17–20 |
| `Compare` with string/int `==` and int `<` | `Expr`, `CmpOp` | rules 21–25 |

All constructors in the submitted `solution.mpy` are declared and covered.
Missing semantics for other translator constructs are irrelevant in
`GENERATED_SEMANTICS` mode.

## All seven reachability claims

1. `loop-zero`: from the symbolic `forBracketSeq` loop head with depth exactly
   zero, no result, and arbitrary function/store tails, completion returns
   `bracketSeqSpec(BS, 0)`.
2. `loop-positive`: the same surrogate loop at any `D > 0` returns
   `bracketSeqSpec(BS, D)`.
3. `universal-correctness`: load the exact submitted function body and invoke
   it with `SeqVal(BS)`; return `bracketSeqSpec(BS, 0)`.
4. Concrete real-string `"<"` returns false.
5. Concrete real-string `"<>"` returns true.
6. Concrete real-string `"<<><>>"` returns true.
7. Concrete real-string `"><<>"` returns false.

Claims 1–3 are result-constraining and satisfiable, but all universal reasoning
is over `SeqVal/forBracketSeq`. Claims 4–7 execute `SVal/forString` but are only
four fixed examples. The unused `bracketSpec(String, Int)` equations do not
connect the universal result to real-string execution.

## Imported trust boundary

The local theory trusts K's `INT`, `BOOL`, `STRING`, and `MAP` built-ins,
including integer arithmetic/comparison, string equality/length/substrings,
map update/lookup matching, generated lists, cell plumbing, and the
Haskell/LLVM backends. These primitives do not encode the task answer.
