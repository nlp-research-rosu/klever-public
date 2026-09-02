# Exhaustive local K inventory

This inventory covers every local declaration and rule in
`/candidate/semantic.k`, `/candidate/verification.k`, and `/candidate/spec.k`.
Imported builtin modules are accounted for separately in the trust ledger.
Line references use the immutable candidate files and are reproduced in
`logs/stage5-numbered-sources.log`.

## Syntax, configuration, and attributes

| Lines | Declaration | Use and assessment |
|---|---|---|
| semantic.k:7 | `Py ::= Module(Stmts)` | Used by `solution.mpy`; exact translator constructor. |
| 9 | `Stmts ::= List{Stmt,""}` | Used for ordered function/loop bodies; empty separator matches translator output. |
| 10-13 | `Stmt ::= FuncDef / Assign / While / Return` | Exactly the four statement forms in the submitted AST. |
| 15 | `Params(String)` | Exact one-parameter constructor used by the AST. |
| 17-23 | `Expr ::= Name / Str / Int / BinOp / Compare / Call / Subscript` | Exactly the seven expression forms in the AST. |
| 25 | `CmpOp(String,Expr)` | Used for `< len(s)`. |
| 26 | `Index ::= Expr \| Slice` | Distinguishes integer indexing from slicing. |
| 27 | `Slice(Bound,Bound,Bound)` | Used for `s[i:i+2]` and `s[i:]`. |
| 28 | `Bound ::= Expr \| NoBound` | Covers the two submitted slice shapes. |
| 38 | `Val ::= pyInt / pyStr / pyBool` | Runtime tagged values. |
| 39 | `Result ::= noResult \| Val` | Final result cell state. |
| 41-59 | 19 `KItem` control constructors | `run`, `exec`, `eval`, assignment, binary/compare continuations, `builtinLen`, index/slice continuations, loop continuations, and `doReturn`. Every constructor is consumed by rules S01-S34 below. |
| 61-64 | Configuration | `<k>` starts `run($PGM,$S)`; `<env>` starts empty; `<result>` starts `noResult`. All three cells are read or written. |
| 133 | `solutionProgram [function,total]` | Closed, zero-argument definitional macro. S35 is its sole exhaustive equation. |
| 162 | `decodeFrom(String,Int,String) [function]` | Partial mathematical summary. It intentionally lacks `total`; S36-S37 cover exactly `0 <= I <= length(S)`. |
| 179 | `decodeBody [function,total]` | Closed definitional macro; S38 is exhaustive. |
| 194 | `decodeTest [function,total]` | Closed definitional macro; S39 is exhaustive. |
| 200 | `decodeReturn [function,total]` | Closed definitional macro; S40 is exhaustive. |

There are no local `functional` declarations, opaque symbols, priorities,
`owise` rules, strictness attributes, or unlisted helper K files.

## Ordinary semantics and definitional rules

| ID / lines | Rule | Static judgment |
|---|---|---|
| S01 / 66-68 | `run(Module(FuncDef("decode_cyclic",Params("s"),BODY)),S)` initializes `s` and executes `BODY` | Sound specialized entry binding for the exact submitted one-function module. No lookup or argument effect is skipped for this fixed entry and string argument. |
| S02 / 70 | Empty `exec` becomes `.K` | Sound list base case. |
| S03 / 71 | `exec(STMT REST)` schedules `STMT ~> exec(REST)` | Sound left-to-right statement order. |
| S04 / 73 | Assignment evaluates RHS before `store` | Sound evaluation order for the submitted name assignments. |
| S05 / 74-75 | `store` updates the environment at the selected name | Sound state update via total `MAP.update`. |
| S06 / 77 | `While` enters `whileLoop` | Sound control normalization. |
| S07 / 78 | `whileLoop` evaluates the test before `whileGuard` | Sound per-iteration guard reevaluation. |
| S08 / 79-80 | True guard schedules body then the next loop head | Sound true branch and loop back-edge. |
| S09 / 81 | False guard consumes the loop | Sound exit branch; disjoint from S08. |
| S10 / 83 | `Return(E)` evaluates `E` before `doReturn` | Sound return-expression order. |
| S11 / 84-86 | `V ~> doReturn ~> REST` discards the remaining computation, clears locals, stores `V` | Sound for this top-level-only language: `doReturn` can only arise from S10, the suffix is the remaining function statements, and there is no caller/cleanup/output/heap cell. The rule would not be reusable for a semantics with call frames or `finally`, but no such state or construct exists here. |
| S12 / 88 | String literal becomes `pyStr` | Sound constructor interpretation. |
| S13 / 89 | Integer literal becomes `pyInt` | Sound constructor interpretation. |
| S14 / 90-91 | Name reads its environment binding | Sound lookup for all reachable names (`s`, `i`, `result`). |
| S15 / 93 | Binary operation evaluates left operand first | Sound Python evaluation order. |
| S16 / 94 | Then evaluates right operand, retaining left value | Sound Python evaluation order. |
| S17 / 95 | Integer `+` uses `+Int` | Sound on reachable integer operands. |
| S18 / 96 | String `+` uses `+String` | Sound on reachable string operands. |
| S19 / 98-99 | Comparison evaluates left operand first | Sound Python evaluation order. |
| S20 / 100 | Then evaluates right operand, retaining left value | Sound Python evaluation order. |
| S21 / 101-102 | Integer `<` true branch guarded by `A < B` | Sound. |
| S22 / 103-104 | Integer `<` false branch guarded by `A >= B` | Sound, disjoint from and exhaustive with S21. |
| S23 / 106 | Exact `len` call evaluates its argument | Sound for the submitted body, which never rebinds `len`. Builtin-name lookup is specialized rather than generally modeled. |
| S24 / 107 | String `len` uses `lengthString` | Sound for K Unicode strings. Compiled-literal hook probes give length 1 for `é`, `α`, and `🙂`; the wrapper execution matches Python. The separate `krun -cS` serialization discrepancy is an external input-bridge limitation. |
| S25 / 109-110 | Integer-index subscript evaluates base first | Sound Python order. |
| S26 / 111 | Then evaluates the index | Sound Python order. |
| S27 / 112-114 | Valid nonnegative index selects `[I,I+1)` | Sound on the reachable loop domain; the guard is guaranteed by the loop test. Negative and exceptional indexing are unused. |
| S28 / 116-117 | Bounded slice evaluates base first | Sound Python order. |
| S29 / 118 | Then evaluates the lower bound | Sound Python order. |
| S30 / 119 | Then evaluates the upper bound | Sound Python order. |
| S31 / 120-122 | Valid bounded slice uses `substrString(S,L,U)` | Sound on reachable `0 <= L <= U <= len(S)`. Python's broader clamping behavior is unused. |
| S32 / 124-125 | Tail slice evaluates base first | Sound Python order. |
| S33 / 126 | Then evaluates its lower bound | Sound Python order. |
| S34 / 127-129 | Valid tail slice selects `[L,len(S))` | Sound on reachable `0 <= L <= len(S)`. |
| S35 / 134-158 | `solutionProgram` expands to a closed `Module(FuncDef(...))` term | Truthful definitional macro. Mechanical token comparison proves identity with trusted-regenerated `solution.mpy`; it does not summarize execution. |
| S36 / 163-171 | Recursive `decodeFrom` equation for a complete 3-character block | Truthful specification equation: appends `S[I+2]` then `S[I:I+2]`, advances by 3, and strictly decreases remaining length. |
| S37 / 173-177 | Base `decodeFrom` equation appends the short tail | Truthful specification equation. Its guard is disjoint from S36 and, with `0 <= I <= len(S)`, exhaustive. |
| S38 / 180-192 | `decodeBody` expands to the exact two loop-body assignments | Truthful closed macro and exact unique subterm of S35. |
| S39 / 195-198 | `decodeTest` expands to the exact loop guard | Truthful closed macro and exact unique subterm of S35. |
| S40 / 201-206 | `decodeReturn` expands to the exact return statement | Truthful closed macro and exact unique subterm of S35. |

## Proof-local simplifications

| ID / lines | Rule | Class and static judgment |
|---|---|---|
| V01 / verification.k:9-11 | Equality of the same map updated at the same key simplifies to equality of the two values | Derived simplification. `MAP.update` is total and overwrites exactly that key, so the equality is equivalent. It does not fabricate an environment or result. |
| V02 / 13 | `0 <= lengthString(S)` simplifies to true | Derived builtin fact. String length is nonnegative for every K String. |
| V03 / 14 | `substrString(S,0,lengthString(S))` simplifies to `S` | Derived full-range substring identity, including the empty string. It only affects proof simplification and agrees with concrete hook behavior. |

V01-V03 are equations, not operational bridges. No local proof rule rewrites a
program-defined invocation to `decodeFrom`, and no fresh or opaque
result-bearing symbol appears.

## Claims

| ID / lines | Claim | Assessment |
|---|---|---|
| C01 / spec.k:8-22 | `loop-correct` | A circularity from the real loop head plus the real return continuation. Precondition `0 <= I <= len(S)` is satisfiable; it returns `decodeFrom(S,I,ACC)` and clears the final environment. It is the execution connection used by C02. |
| C02 / 25-28 | `program-correct` | Executes `run(solutionProgram,S)` from empty state for every K String and constrains the final result to `decodeFrom(S,0,"")`. No free RHS value or implication weakens the result. |

## Construct coverage

Every constructor token in the trusted-regenerated `solution.mpy` maps to a
syntax declaration and an execution path above:

`Module/FuncDef/Params` -> S01; statement-list structure -> S02-S03;
`Assign/Name/Str/Int/BinOp` -> S04-S05 and S12-S18; `While/Compare/CmpOp/Call`
-> S06-S09 and S19-S24; integer `Subscript` -> S25-S27; bounded `Slice` ->
S28-S31; tail `Slice` -> S32-S34; `Return` -> S10-S11.

The rule overlap analysis found only intentional, disjoint branch pairs
(S08/S09, S17/S18 by value sort, S21/S22 by complementary guards,
S25/S28/S32 by index/slice shape, and S36/S37 by complementary guards).
