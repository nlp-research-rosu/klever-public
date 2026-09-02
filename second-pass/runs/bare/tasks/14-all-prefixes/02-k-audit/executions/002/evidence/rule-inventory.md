# Exhaustive local K inventory

This inventory covers every declaration and rule in the candidate's
`semantic.k`, `solution-program.k`, `verification.k`, `verified-lemma.k`,
`loop-spec.k`, and `spec.k`. Imported K built-ins are listed separately as
trusted primitives.

## Syntax declarations in `semantic.k`

| Lines | Declaration / productions | Used by `solution.mpy` | Review |
|---|---|---:|---|
| 5-6 | `Program`: `Module(Stmts)`, `Run(Program,Expr)` | both | Faithful module execution and audit-call wrapper. |
| 8 | `Stmts`: empty-separated `List{Stmt,""}` | yes | Matches translated juxtaposed statements. |
| 9 | `Exprs`: `NeList{Expr,","}` | yes, singleton | Only singleton calls are used. |
| 10 | `Strings`: `List{String,","}` | yes, singleton | Used by import names and parameters. |
| 12-17 | `Stmt`: `ImportFrom`, `FuncDef`, `Assign`, `While`, `Expr`, `Return` | all | Exactly the submitted statement forms. |
| 19 | `Params(Strings)` | yes | Submitted function has one parameter. |
| 21-30 | `Expr`: `Name`, `Int`, `Str`, empty/nonempty `ListExpr`, `BinOp`, `Compare`, `Call`, `Attribute`, `Subscript` | all except nonempty `ListExpr` | Every submitted expression constructor is declared. |
| 32-33 | comparison lists and `CmpOp` | yes, singleton `<=` | Only the modeled singleton comparison is used. |
| 35-37 | `Index ::= Expr \| Slice`; `Bound ::= Expr \| NoBound` | slice with omitted lower/step | Exact submitted slice shape is covered. |

The nonempty list-literal and direct-index productions lack evaluation rules,
but are unused. This generated-semantics mode permits such unused coverage
gaps.

## Runtime declarations in `semantic.k`

| Lines | Declaration | Attributes / role |
|---|---|---|
| 47-51 | `Value`: `intVal`, `strVal`, `boolVal`, `listVal`, `noneVal` | Runtime values; `noneVal` unused. |
| 52 | `Values`: `vnil`, `vcons` | Pure list representation. |
| 54 | `Env`: `emptyEnv`, `bind` | Local variable environment. |
| 55-56 | `Function`, `FEnv` | One-parameter function and function environment. |
| 58-62 | `KItem`: `exec`, `loop`, `restoreEnv`, `returning`, `invoke` | Internal control terms. |
| 64 | `lookup` | `[function]`, partial on missing names. |
| 69 | `update` | `[function]`, covers both empty and bound environments. |
| 75 | `flookup` | `[function]`, partial on missing functions. |
| 80 | `snoc` | `[function]`, covers `vnil`/`vcons`. |
| 84 | `eval` | `[function]`, intentionally partial outside used expressions. |
| 96-100 | `addVal`, `lenVal`, `lessEqVal`, `prefixVal`, `appendVal` | `[function]`, type-specific and partial off the used types. |
| 107 | `truth` | `[function]`, defined for `boolVal`. |
| 110-115 | `<mpy>` configuration with `<k>`, `<env>`, `<functions>` | Every cell is read or changed by used rules. |

There are no local `[total]` or `[functional]` declarations.

## All 39 rules in `semantic.k`

| # | Lines | Rule | Classification and review |
|---:|---:|---|---|
| 1 | 65 | same-key `lookup` | Correct nearest-binding lookup. |
| 2 | 66-67 | different-key `lookup` recursion | Guard is disjoint from rule 1; correct. |
| 3 | 70 | `update` empty | Correct insertion. |
| 4 | 71 | `update` same key | Correct nearest-binding replacement. |
| 5 | 72-73 | `update` different key | Guard disjoint from rule 4; preserves order/rest. |
| 6 | 76 | same-key `flookup` | Correct nearest function binding. |
| 7 | 77-78 | different-key `flookup` recursion | Guard disjoint from rule 6. |
| 8 | 81 | `snoc(vnil,V)` | Correct singleton result. |
| 9 | 82 | recursive `snoc(vcons(...),V)` | Structural descent; correct. |
| 10 | 85 | integer literal evaluation | Correct. |
| 11 | 86 | string literal evaluation | Constructor preservation; correct. |
| 12 | 87 | name evaluation | Correct for the modeled environment. |
| 13 | 88 | empty-list evaluation | Correct fresh-list value for this alias-free program. |
| 14 | 89 | integer `+` through `addVal` | Correct for the submitted operands; expressions are pure. |
| 15 | 90 | built-in `len` through `lenVal` | **Not faithful to Python Unicode strings.** Rule 25 supplies byte length. |
| 16 | 91-92 | singleton `<=` through `lessEqVal` | Correct for submitted integer values. |
| 17 | 93-94 | `S[:HI]` through `prefixVal` | **Not faithful to Python Unicode slicing.** Rule 27 slices bytes. |
| 18 | 101 | integer `addVal` | Correct unbounded integer addition. |
| 19 | 102 | `lenVal(strVal(S)) => lengthString(S)` | **Material false-Python witness:** CPython `len("🙂") = 1`; fresh K execution iterates four times, establishing `lengthString("🙂") = 4` in this runtime. |
| 20 | 103 | integer `lessEqVal` | Correct. |
| 21 | 104 | `prefixVal` via `substrString(S,0,I)` | **Material false-Python witness:** CPython `"🙂"[:1] = "🙂"`; fresh K execution produces the first result `strVal("\\xf0")`. |
| 22 | 105 | `appendVal` via `snoc` | Correct returned list state for the submitted alias-free list. |
| 23 | 108 | truth of `boolVal` | Correct. |
| 24 | 117 | `Run(Module(SS),E)` | Executes module statements before call expression; correct. |
| 25 | 118 | bare `Module` | Correct statement execution wrapper. |
| 26 | 120 | empty `exec` | Correct termination of a statement list. |
| 27 | 121 | nonempty `exec` sequencing | Left-to-right execution; correct. |
| 28 | 123 | discard `ImportFrom` | Semantically inert for this typing-only import. |
| 29 | 124-125 | install `FuncDef` in function environment | Correct for the submitted single-parameter, capture-free definition. |
| 30 | 126-127 | assignment to `Name` | RHS is pure in this program; correct update. |
| 31 | 128-129 | `result.append(E)` statement | Models mutation as variable replacement. This preserves the submitted program because the fresh list has no aliases and append's return value is discarded. |
| 32 | 130 | lower `While` to `loop` | Correct. |
| 33 | 131-133 | true loop branch | Executes body then returns to the identical loop head; correct. |
| 34 | 134-136 | false loop branch | Guard disjoint from rule 33; correct. |
| 35 | 138-140 | user function call | Selects the installed binding and evaluates the pure argument in the caller environment. |
| 36 | 141-142 | function invocation | Creates a parameter-only local environment and records caller environment. Correct for this capture-free body. |
| 37 | 144-145 | return expression | Correctly evaluates the pure returned name. |
| 38 | 146 | discard remaining function `exec` after return | Correct for the submitted final return. It would not fully model return nested inside arbitrary loop/control contexts, but those contexts are unused. |
| 39 | 147-148 | restore caller environment and expose return value | Correct. |

Rules 19 and 21 are the decisive generated-semantics defect. The complete
program witness is preserved in `19-krun-emoji.log`: K returns four byte
prefixes `"\xf0"`, `"\xf0\x9f"`, `"\xf0\x9f\x99"`,
`"\xf0\x9f\x99\x82"` for input `"🙂"`, whereas both trusted canonical Python
and submitted Python return the one-element list `["🙂"]`.

## Helper and proof-extension declarations

| File:lines | Extension | Class / attributes | Complete review |
|---|---|---|---|
| `solution-program.k:3-16` | `solutionProgram` and its one rule | `[function]`; definitional syntax embedding | Fresh trusted translation and regenerated embedding are byte-identical to the submitted artifacts. The RHS is the complete submitted module term. |
| `verification.k:10-11` | `pacc(String,Int)` and `pacc(_,0) => vnil` | Plain `Values` constructor; ordinary definitional rule | Base of the abstract prefix accumulator. It does not bypass program execution. |
| `verification.k:12-15` | `snoc(pacc(S,N),strVal(substrString(S,0,I))) => pacc(S,N+1)` when `I=N+1` | Definitional summary; `[simplification]` | Truthful induction step on the invariant domain `0 <= N < lengthString(S)`. Its global guard is broader (negative/out-of-range `N` is not given a clear human meaning), so reuse outside the invariant would need a narrower guard. No false conclusion is attributed outside that unspecified abstract domain. |
| `verification.k:17-18` | `allPrefixes(String)` | `[function]`; definitional summary | Reduces to `pacc(S,lengthString(S))`. It exactly summarizes the candidate K semantics, but inherits the byte-string/Python mismatch. |
| `verified-lemma.k:7-26` | exact loop-head rewrite to `listVal(allPrefixes(S))` | Operational bridge; `[priority(30)]` | Its exact continuation is `exec(Return(result)) ~> restoreEnv(OLD)`, its exact environment is the real loop-entry state (`result=[]`, `i=1`), it preserves the implicitly framed function cell, and it requires nonnegative string length. `loop-spec.k` proves the more general bridge-free theorem with arbitrary function environment and the same complete continuation; this is its `N=0,I=1` specialization. The body mutation failed, showing the rule does not match a changed initializer. |

No proof-local declaration is `[total]` or `[functional]`. The only explicit
priority is the verified loop lemma's `priority(30)`. `pacc(S,N)` for positive
`N` is the only opaque/irreducible result-bearing term; its base/step equations
give the recursive mathematical meaning used by the invariant, but do not
provide a forward normal form into explicit `vcons` terms.

## Claims

| File | Claim | Plain-language meaning and satisfiable witness |
|---|---|---|
| `loop-spec.k:6-30` | Loop invariant / auxiliary execution theorem | If the input has K string length at least zero, `0 <= N <= lengthString(S)`, `I=N+1`, and the exact loop state contains `pacc(S,N)`, execution through the loop and final return restores `OLD` and yields `allPrefixes(S)`. Witness: `S="abc"`, `N=0`, `I=1`, `OLD=emptyEnv`. It was proved without importing the later bridge. |
| `spec.k:6-13` | Entry claim | From empty environments, execute the exact embedded module, call `all_prefixes` on arbitrary K `String` `S`, restore the empty variable environment, and return exactly `listVal(allPrefixes(S))`; the resulting function environment is existentially allowed. Witness: `S=""` or `S="abc"`. The precondition `0 <= lengthString(S)` is satisfiable and effectively universal. |

The target is neither free nor tautological. The fresh mutation
`all_prefixes("a") => []` stops at `listVal(pacc("a",1))`, while ASCII
concrete runs show the expected explicit lists. The postcondition nevertheless
describes K byte prefixes for non-ASCII strings, not Python prefixes.

## Construct-to-rule map for `solution.mpy`

| Submitted construct | Declaration | Evaluation rules |
|---|---|---|
| `Module` | `Program` | 24-29 above |
| typing `ImportFrom` | `Stmt` | 28 |
| `FuncDef`, `Params` | `Stmt`, `Params` | 29 |
| `Assign(Name,ListExpr())` | `Stmt`, `Expr` | 13, 30 |
| `Assign(Name,Int(1))` | `Stmt`, `Expr` | 10, 30 |
| `While`, `Compare <=`, `Call len` | `Stmt`, `Expr`, `CmpOp` | 15-16, 19-20, 32-34 |
| append expression statement | `Expr(Call(Attribute(...)))` | 31 |
| string prefix subscript/slice | `Subscript`, `Slice`, `NoBound` | 17, 21 |
| integer increment | `BinOp("+",...)` | 14, 18, 30 |
| `Return(Name(result))` | `Stmt`, `Expr` | 12, 37-39 |
| entry user call | `Call(Name(F),ARG)` | 35-36 |

## Imported trust boundary

The proof trusts K 7.1.293's `INT`, `BOOL`, `STRING`, `K-EQUAL`, parser, KORE
translation, and Haskell backend. In particular it trusts `+Int`, `<=Int`,
`==Int`, `lengthString`, and `substrString`. These are acceptable low-level K
primitives for a theorem about K strings. They do not by themselves establish
equivalence to CPython's Unicode `str`, and the fresh counterexample disproves
that bridge here.
