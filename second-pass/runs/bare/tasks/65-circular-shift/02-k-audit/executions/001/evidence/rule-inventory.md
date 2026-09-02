# Reviewer rule inventory

This inventory is reconstructed from the copied source files, not from a
candidate-provided compiled definition. Line numbers refer to the source
listing in `04-source-listings.log`.

## Local syntax and configuration

`semantic.k` declares these AST/data constructors:

- `Program`: `Module(Stmts)`; `Stmts`: empty-separated `Stmt` list.
- `Stmt`: `FuncDef`, `Assign`, `If`, and `Return`.
- `Params` and comma-separated `ParamNames`.
- `Expr`: `Name`, `Int`, `BinOp`, `UnaryOp`, `Compare`, `Call`, and
  `Subscript`.
- `Exprs`, `CmpOp`, `Slice`, and `Bound` (`Expr` or `NoBound`).
- `Val`: `VInt`, `VString`, `VBool`, and `VNone`; comma-separated `Vals`.
- `ExecResult`: `returned(Val)` and `normal(Map)`.

The only configuration is `<mpy>` with `<k>`, `<entry>`, `<args>`, and
`<result>` cells. There is no heap, stack, output, exception, or allocation
cell.

`semantic.k` declares 19 local function symbols:

1. `runProgram`
2. `bind`
3. `exec`
4. `branch`
5. `continue`
6. `resultOf`
7. `eval`
8. `lookupVal`
9. `pyStr`
10. `pyLen`
11. `unary`
12. `binary`
13. `compare`
14. `sliceFrom`
15. `sliceTo`
16. `reverseValue`
17. `clipIndex` (`[function, total]`)
18. `reverseString`
19. `reverseFrom`

`verification.k` additionally declares:

- `solutionProgram`, a `Program` macro.
- `runSolution`, a `Val` function that is unused by the claims.
- `normalCircularShift`, a `String` function used by the normal-branch
  postcondition.

There are no local `[functional]` symbols, simplification rules, priority
rules, fresh or opaque symbols, proof-local axioms, or imported helper K files.
The only local `[total]` declaration is `clipIndex`.

## Rule decisions

| ID | Source | Rule | Decision and reason |
|---|---|---|---|
| S01 | semantic.k:46 | Consume the input `Program` and set `result` to `runProgram` | Sound for this pure-interpreter configuration; all observable cells are explicit and `entry`/`args` are preserved. |
| S02 | :53 | Select a matching first `FuncDef` | Sound name lookup for the submitted one-function module. |
| S03 | :55 | Skip a nonmatching `FuncDef` | Sound; guard is disjoint from S02. |
| S04 | :60 | Bind empty parameters/arguments to `.Map` | Sound. |
| S05 | :61 | Bind one positional parameter and recurse | Sound for distinct parameters and equal arity, as in the real program. |
| S06 | :71 | Empty statement list returns `normal(ENV)` | Sound. |
| S07 | :72 | Assignment evaluates the RHS and updates the named binding | Sound for the used `Name` target and pure supported expressions. |
| S08 | :74 | `If` evaluates its condition and dispatches through `branch` | Sound. |
| S09 | :76 | `Return` evaluates its expression and discards following statements | Sound abrupt-return behavior. |
| S10 | :78 | True Boolean executes `THEN`, then `REST` if normal | Sound. |
| S11 | :81 | False Boolean executes `ELSE`, then `REST` if normal | Sound and guard-disjoint from S10. |
| S12 | :84 | Preserve `returned(V)` through `continue` | Sound; prevents execution after return. |
| S13 | :85 | Continue `REST` after normal branch completion | Sound. |
| S14 | :86 | Extract a returned value | Sound. |
| S15 | :87 | Map fallthrough to `VNone` | Sound Python fallthrough behavior. |
| S16 | :101 | Evaluate `Name` through `lookupVal` | Sound for bound names. |
| S17 | :102 | Retrieve a matching map entry | Sound for the distinct-key environment created by S04/S05. |
| S18 | :103 | Evaluate integer literal | Sound. |
| S19 | :104 | Evaluate unary operator and operand | Sound for the used pure unary minus. |
| S20 | :105 | Evaluate binary operator and operands | Sound for the used pure subtraction/string concatenation; order has no observable effect in this subset. |
| S21 | :106 | Evaluate comparison operands | Sound for the used pure greater-than comparison. |
| S22 | :108 | Evaluate the built-in `str` call | Sound for the used single integer argument and fixed binding. |
| S23 | :109 | Evaluate the built-in `len` call | Sound for the used single ASCII string argument and fixed binding. |
| S24 | :110 | Recognize `s[::-1]` and invoke `reverseValue` | Sound for the exact used all-bounds-omitted, step-minus-one slice. |
| S25 | :112 | Evaluate a lower-bound-only slice | Sound for the exact used form. |
| S26 | :114 | Evaluate an upper-bound-only slice | Sound for the exact used form. |
| S27 | :117 | Convert `VInt` with `Int2String` | Sound bridge for Python decimal `str(int)` over K integers. |
| S28 | :118 | Length of `VString` | Sound for decimal ASCII strings. |
| S29 | :119 | Integer unary minus | Sound. |
| S30 | :120 | Integer subtraction | Sound. |
| S31 | :121 | String concatenation | Sound. |
| S32 | :122 | Integer greater-than | Sound. |
| S33 | :126 | Clip indices below `-L` to zero | Sound whenever `L >= 0`, the complete reachable call domain. |
| S34 | :127 | Translate negative in-range index by `+L` | Sound whenever `L >= 0`. |
| S35 | :129 | Preserve indices in `[0,L]` | Sound whenever `L >= 0`. |
| S36 | :130 | Clip indices above `L` to `L` | Sound whenever `L >= 0`. |
| S37 | :132 | Lower-only string slice via clipped `substrString` | Sound on every reachable call. |
| S38 | :134 | Upper-only string slice via clipped `substrString` | Sound on every reachable call. |
| S39 | :139 | Reverse a string value through `reverseString` | Sound. |
| S40 | :140 | Seed reversal at `length - 1` | Sound. |
| S41 | :141 | End reversal below index zero | Sound. |
| S42 | :142 | Append the current one-character substring and decrement | Sound on the reachable range `0 <= I < length(S)`; recursion strictly descends. |
| V01 | verification.k:10 | Expand `solutionProgram` to a fixed AST | Sound pinning macro; fresh `kast` outputs are byte-identical. |
| V02 | :30 | Define `runSolution` with the fixed AST | Sound but unused by every claim. |
| V03 | :35 | Define normal rotation as suffix plus prefix | Sound under the normal claim guard `0 <= SHIFT <= length(S)`. |

## Construct coverage

Every constructor in `solution.mpy` is covered:

| Used construct | Declaration | Execution rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | AST syntax | S01-S05 |
| statement list, `Assign`, `If`, `Return` | statement syntax | S06-S15 |
| `Name`, `Int` | expression syntax | S16-S18 |
| `UnaryOp`, `BinOp`, `Compare`, `CmpOp` | expression syntax | S19-S21 and S29-S32 |
| `Call(str)`, `Call(len)` and expression lists | expression syntax | S22-S23 and S27-S28 |
| `Subscript`, `Slice`, `NoBound` | expression syntax | S24-S26 and S33-S42 |

The definition intentionally omits unused Python constructs. Used expression
forms are pure, so its recursive function evaluation does not expose a
left-to-right ordering difference.

## Narrow totality/guard limitation

S33-S36 are disjoint and exhaustive for every reachable `L =
lengthString(S) >= 0`. The `[total]` declaration is nevertheless wider than
that justified domain: at the unreachable helper term `clipIndex(0, -1)`, S33
has guard `0 < 1` and returns `0`, while S36 has guard `-1 < 0` and returns
`-1`. This is a global overlap/guard-scope defect. It is not classified as a
material real-program unsoundness because no intended program input can make a
string length negative, no proof claim exposes the helper, and the fresh false
real-result mutation is rejected.
