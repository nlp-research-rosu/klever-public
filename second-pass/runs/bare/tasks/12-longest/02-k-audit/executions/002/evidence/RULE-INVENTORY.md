# Exhaustive local K inventory

This inventory covers the immutable candidate sources `semantic.k`,
`verification.k`, and `spec.k`. Line numbers refer to those candidate files.
Imported K framework modules (`INT`, `STRING`, `BOOL`, and `MAP`) are trusted
library dependencies, not local declarations.

## Local syntax and configuration in `semantic.k`

| Lines | Declaration | Attributes / role |
|---|---|---|
| 5 | Empty sort declaration `Expr` | Forward declaration |
| 6 | `Exprs ::= List{Expr, ","}` | Expression-list syntax |
| 7 | `CmpOp ::= CmpOp(String, Expr)` | Comparison constructor |
| 8 | `CmpOps ::= List{CmpOp, ","}` | Comparison-list syntax |
| 9 | `Strings ::= List{String, ","}` | String-list syntax |
| 10 | `Params ::= Params(Strings)` | Parameter constructor |
| 11 | Empty sort declaration `Stmt` | Forward declaration |
| 12 | `Stmts ::= List{Stmt, ""}` | Statement-list syntax |
| 14–21 | `Expr` constructors `NoneVal`, `Int`, `Str`, `Name`, `Call`, `Compare`, `Subscript`, `ListExpr` | Program AST |
| 23–30 | `Stmt` constructors `Module`, `ImportFrom`, `FuncDef`, `If`, `Assign`, `For`, `Return(Expr)`, `Return()` | Program AST |
| 38 | Empty sort declaration `Value` | Forward declaration |
| 39 | `Values ::= List{Value, ","}` | Runtime list payload |
| 40–44 | `Value` constructors `noneVal`, `intVal`, `strVal`, `boolVal`, `listVal` | Runtime values |
| 46 | `Output ::= noOutput \| Value` | Return-output state |
| 47–48 | `Function ::= noFunction \| function(Params, Stmts)` | Single stored function |
| 50–57 | `<mpy>` configuration with `<k>`, `<args>`, `<env>`, `<function>`, `<out>` | Complete local runtime state |
| 59–65 | `KItem` constructors `exec`, `execStmt`, `invokeEntry`, `functionEnd`, `branch`, `forValues`, `returning` | Internal control |
| 67–72 | Value-valued symbols `eval`, `lookup`, `pyLen`, `isEmpty`, `compare`, `head` | Each declared `[function]` |
| 142 | `sizeValues : Values -> Int` | Declared `[function]` |

There are no local `[total]`, `[functional]`, `[macro]`, priority, or opaque
declarations in `semantic.k`. The two lookup rules S28–S29 below are the only
local `[simplification]` rules.

## Rules in `semantic.k`

| ID | Lines | Rule | Static decision |
|---|---:|---|---|
| S1 | 74 | `Module(SS)` schedules `exec(SS)` then `invokeEntry` | Valid for the target one-module execution model. |
| S2 | 76 | Empty statement list finishes | Valid list base case. |
| S3 | 77 | Nonempty statement list schedules its head then tail | Valid ordered sequencing. |
| S4 | 79 | `ImportFrom` is inert | Valid for this typing-only import; it deliberately omits general Python import effects. |
| S5 | 80–81 | A `FuncDef` stores parameters/body in the sole function cell | Valid for the target’s single definition; broader multi-function Python is outside the generated subset. |
| S6 | 83–88 | `invokeEntry` binds the sole argument and initializes the two target locals | Valid on the exact target body. Preallocating locals is unobservable because neither is read before its Python assignment. |
| S7 | 90–92 | Name assignment evaluates the RHS in the old environment and replaces that binding | Valid for the target’s preallocated name targets. |
| S8 | 94–96 | `If` evaluates its guard, then creates `branch` | Valid; target guards are pure. |
| S9 | 97 | True branch executes `THEN` | Valid. |
| S10 | 98 | False branch executes `ELSE` | Valid. |
| S11 | 100–102 | `For` evaluates the iterable and creates `forValues` | Valid; target iterable expression is pure. |
| S12 | 103 | Empty `listVal` iteration finishes | Valid. |
| S13 | 104–106 | Cons `listVal` iteration binds the head, executes the body, then the tail | Valid order, state, and control for the target’s immutable list of strings. |
| S14 | 108–109 | Return with expression evaluates it and creates `returning` | Valid for pure target return expressions. |
| S15 | 110 | Bare return produces `noneVal` | Valid but unused. |
| S16 | 112 | A pending return discards a remaining `exec` continuation | Valid return control for this subset. |
| S17 | 113 | A pending return discards a remaining loop continuation | Valid return control for this subset. |
| S18 | 114–115 | Return at `functionEnd` writes `<out>` and terminates | Valid. |
| S19 | 117 | `eval(NoneVal)` | Valid. |
| S20 | 118 | `eval(Int(I))` | Valid. |
| S21 | 119 | `eval(Str(S))` | Valid but unused by the submitted body. |
| S22 | 120 | Name evaluation calls `lookup` | Valid. |
| S23 | 121 | Built-in `len` calls `pyLen` | Valid for target list/string operands. |
| S24 | 122–123 | The exact `len(E) == 0` AST calls `isEmpty` | Valid for list/string operands; invalid-type cases remain visibly stuck. |
| S25 | 124–125 | Greater-than comparison evaluates both sides and calls `compare` | Valid for the target’s pure integer lengths. |
| S26 | 126 | Index zero calls `head` | Valid on the target’s checked-nonempty path. |
| S27 | 128 | Lookup in a map decomposition containing `X |-> V` returns `V` | Valid Map lookup. |
| S28 | 129 | Lookup after same-key Map update returns the new value | Valid `[simplification]`; overlaps S27 consistently. |
| S29 | 130–132 | Lookup after a distinct-key Map update ignores that update | Valid guarded `[simplification]`; guard is disjoint from S28. |
| S30 | 134 | String length uses `lengthString` | Valid target primitive; K/Python Unicode samples agree in the recorded differential run. |
| S31 | 135 | Concrete list length uses `sizeValues` | Valid. |
| S32 | 137 | Empty concrete list is empty | Valid. |
| S33 | 138 | Cons concrete list is nonempty | Valid and disjoint from S32. |
| S34 | 139 | Empty string is empty | Valid but unused by this body’s emptiness check. |
| S35 | 140 | Guarded nonempty string is not empty | Valid and disjoint from S34. |
| S36 | 143 | Empty Values list has size zero | Valid. |
| S37 | 144 | Cons Values list has size one plus tail size | Valid, structurally descending. |
| S38 | 146 | Integer equality returns `boolVal(I ==Int J)` | Valid; unused by the exact special-case guard after S24. |
| S39 | 147 | Integer greater-than returns `boolVal(I >Int J)` | Valid. |
| S40 | 149 | Head of a nonempty concrete list returns its first value | Valid; empty input has no matching rule, preserving the error/stuck boundary. |

No local semantic rule has an overlap yielding conflicting right-hand sides.
No local function recursion fails to descend on its list argument. The
semantics is intentionally partial outside the target subset.

## Used-construct map

| `solution.mpy` construct | Syntax | Executing rules |
|---|---|---|
| `Module` | `Stmt` line 23 | S1–S3 |
| `ImportFrom("typing",...)` | `Stmt` line 24 | S4 |
| `FuncDef`, `Params` | `Stmt` line 25; line 10 | S5–S6 |
| `If` | `Stmt` line 26 | S8–S10 |
| `Compare(len(...), == 0)` | `Expr` lines 18–19 and `CmpOp` line 7 | S19–S24, S27–S35 |
| `Assign(Name, Expr)` | `Stmt` line 27 | S7 and expression rules |
| `Subscript(..., Int(0))` | `Expr` line 20 | S20, S22, S26, S40 |
| `For(Name, Name, body)` | `Stmt` line 28 | S11–S13 |
| `Compare(len(...), > len(...))` | `Expr` lines 18–19 | S22–S23, S25, S27–S31, S39 |
| `Return(NoneVal/Name)` | `Stmt` line 29 | S14, S16–S19, S22, S27–S29 |

`ListExpr`, literal `Str`, and bare `Return()` are declared but not exercised.
Missing behavior for unrelated Python constructs is not a generated-semantics
defect.

## Declarations and rules in `verification.k`

| ID | Lines | Declaration / rule | Attributes and static decision |
|---|---:|---|---|
| V1 | 8–14 | `longestLoopBody : Stmts` and expansion rule | `[macro]`; mechanically expands to the exact submitted loop body. |
| V2 | 16–27 | `longestProgram : Stmt` and expansion rule | `[macro]`; expanded KORE is byte-identical to parsing `solution.mpy`. |
| V3 | 31,33 | `stringList(Strings)` and its rule | `[function]`; truthful wrapper `listVal(stringValues(...))`, but unused by every universal claim. |
| V4 | 32,34 | Empty `stringValues` | `[function]`; truthful list base. |
| V5 | 32,35–36 | Cons `stringValues` | `[function]`; truthful and descending. |
| V6 | 40,43 | `expectedLongest(.Strings)` | `[function]`; correct empty result, but unused by the claims. |
| V7 | 40,44–45 | Nonempty `expectedLongest` | `[function]`; delegates to the transparent fold, unused by the claims. |
| V8 | 41,47 | Empty-tail `firstLongest` | `[function]`; returns current best. |
| V9 | 41,48–50 | Longer next string replaces best | `[function]`; truthful, guarded, descending. |
| V10 | 41,51–53 | Shorter/equal next string keeps best | `[function]`; truthful; guard is disjoint from and exhaustive with V9. |
| V11 | 57 | `stringAt(String,Int) : String` | Opaque `[function,total]` with no equations. It denotes external symbolic sequence contents; no answer is fixed by it. |
| V12 | 58 | `seqVal(String,Int,Int) : Value` | Proof-only symbolic sequence constructor; no attributes. |
| V13 | 60–61 | `isEmpty(seqVal(...,N))` for `N == 0` | Valid under the declared sequence interpretation. |
| V14 | 62–63 | `isEmpty(seqVal(...,N))` for `N > 0` | Valid; disjoint from V13 on the claimed domain. Negative lengths remain stuck. |
| V15 | 64–65 | `head(seqVal(ID,I,N))` | Returns `stringAt(ID,I)` when nonempty; valid under the sequence interpretation. |
| V16 | 67–68 | Empty symbolic iteration finishes | Ordinary operational rule; valid for `N == 0`. |
| V17 | 69–74 | Nonempty symbolic iteration binds `stringAt(ID,I)`, executes the real body, increments `I`, decrements `N` | Ordinary operational rule; preserves continuation and environment footprint and executes one body per element. |
| V18 | 77–79 | `firstInSeq` at `N == 0` | `[function]`; returns current best. |
| V19 | 77,80–83 | `firstInSeq` replaces best on a longer element | `[function]`; truthful and decreases `N`. |
| V20 | 77,84–87 | `firstInSeq` keeps best on a shorter/equal element | `[function]`; truthful, disjoint/exhaustive with V19, and decreases `N`. |

There are no explicit priority, `[simplification]`, or `[functional]`
declarations in `verification.k`. `stringAt` is the sole opaque/`[total]`
symbol. The `[function]` symbols otherwise have guarded, nonoverlapping,
structurally terminating equations over every domain used by a claim.

V13–V17 do not overlap the fixed `listVal` rules because `seqVal` is a disjoint
constructor. Thus they do not enable a concrete false `listVal` conclusion.
They are nevertheless a proof-local representation bridge: the candidate has
no bridge-free theorem connecting arbitrary `listVal(stringValues(SS))`
execution to `seqVal(ID,0,N)`. Recorded ground interpretations agree with
fixed `listVal` execution for two distinct outcomes (`"ccc"` and `"zzzz"`),
but those finite checks are not a universal connection theorem. This is an
evidence limitation, not a demonstrated false rule.

## Claims in `spec.k`

| ID | Lines | Claim | Formal scope |
|---|---:|---|---|
| C1 | 8–18 | `longest-loop` | For arbitrary `ID,I,BEST` and `N >= 0`, execute the symbolic-sequence loop and return; output is `firstInSeq(BEST,ID,I,N)`. |
| C2 | 20–25 | `longest-empty` | Exact submitted program on `seqVal(ID,0,0)` returns `noneVal`. |
| C3 | 27–34 | `longest-nonempty` | Exact submitted program on `seqVal(ID,0,N)`, `N > 0`, returns the transparent fold over the `N` symbolic elements. |
| C4 | 38–43 | `concrete-empty` | Exact submitted program on empty `listVal` returns `noneVal`. |
| C5 | 45–50 | `concrete-first-tie` | Exact submitted program on `["a","b","c"]` returns `"a"`. |
| C6 | 52–57 | `concrete-increasing` | Exact submitted program on `["a","bb","ccc"]` returns `"ccc"`. |
| C7 | 59–64 | `concrete-late-tie` | Exact submitted program on `["aa","b","cc"]` returns `"aa"`. |

All seven postconditions constrain `<out>` to a specific value or transparent
fold. Final environments and function cells are existentially framed, which is
appropriate because the source contract observes only the return value.
