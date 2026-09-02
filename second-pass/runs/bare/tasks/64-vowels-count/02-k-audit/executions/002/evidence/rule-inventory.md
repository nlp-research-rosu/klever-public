# Independent source rule inventory

Scope: the immutable candidate sources `semantic.k`, `verification.k`, and
`spec.k`. Line numbers below refer to those candidate files. There are no
candidate helper K files.

## Imports, syntax, and generated evaluation declarations

`semantic.k` module `MPY-SYNTAX` imports `BOOL`, `INT`, `STRING`, `MAP`, and
`LIST`. Its local productions are:

| ID | Lines | Declaration | Used construct and review |
|---|---:|---|---|
| S01 | 8 | `Program ::= Module(Stmts)` | Exact outer constructor emitted by the trusted translator. |
| S02 | 9 | `Stmts ::= List{Stmt, ""}` | Exact juxtaposed statement-sequence representation. |
| S03 | 10 | one-string `Params` | Exact one-argument signature used here. |
| S04 | 12 | `FuncDef` | Exact submitted function-definition constructor. |
| S05 | 13 | `Return(Expr) [strict]` | Evaluates the returned expression before return control. |
| S06 | 14 | `If(Expr,Stmts,Stmts) [strict(1)]` | Evaluates only the guard before branch selection. |
| S07 | 16 | `Int(Int)` | Integer literal. |
| S08 | 17 | `Str(String)` | String literal. |
| S09 | 18 | `Name(String)` | Variable/function name constructor. |
| S10 | 19 | `Expr ::= PyVal` | Injects evaluated values into expressions. |
| S11 | 20 | `BinOp(String,Expr,Expr) [strict(2,3)]` | Left-to-right operand heating/cooling for the used `+`. |
| S12 | 21 | `BoolOp(String,Expr,Expr) [strict(2)]` | Evaluates the left operand first; local rules short-circuit `and`. |
| S13 | 22 | `Compare(Expr,CmpOp) [strict(1)]` | Evaluates the left operand before staging the comparator. |
| S14 | 23 | `Subscript(Expr,Expr) [strict]` | Indexing form; only safe index zero is reachable in this program. |
| S15 | 24 | `Subscript(Expr,Slice) [strict(1)]` | Slice receiver evaluation; submitted bounds are fixed syntax. |
| S16 | 25 | `Call(Expr,Expr) [strict(2)]` | Evaluates the sole argument before direct-name dispatch. |
| S17 | 27 | `CmpOp(String,Expr)` | Single comparator emitted by the trusted translator. |
| S18 | 28 | `Bound ::= Expr \| NoBound` | Submitted tail slice bounds. |
| S19 | 29 | `Slice(Bound,Bound,Bound)` | Submitted `s[1:]` constructor. |
| S20 | 31 | `intVal(Int)` | Modeled Python integer value. |
| S21 | 32 | `strVal(String)` | Modeled Python string value. |
| S22 | 33 | `boolVal(Bool)` | Modeled Python Boolean value. |
| S23 | 34 | `KResult ::= PyVal` | Stops heating at modeled values. |

`semantic.k` module `SOLUTION` imports `MPY-SYNTAX` and declares two macros:

| ID | Lines | Declaration | Review |
|---|---:|---|---|
| M01 | 41–61 | `vowelBody` macro and expansion rule | Compile-time name for the exact four-statement submitted body. Fresh `kast --expand-macros` comparison proves constructor identity. |
| M02 | 63–65 | `solutionProgram` macro and expansion rule | Compile-time name for the exact submitted one-function module. |

`semantic.k` module `SEMANTIC` imports `SOLUTION` and locally declares:

| ID | Lines | Declaration | Review |
|---|---:|---|---|
| S24 | 71 | `Function ::= function(String,Stmts)` | One-parameter closure-free function record, sufficient for the submitted program. |
| S25 | 72 | `#compare(String,PyVal,Expr) [strict(3)]` | Staging form that evaluates the comparator RHS after the LHS. |
| F01 | 73 | `#isVowelChar(String) [function,total]` | Total character predicate; equations R27–R37 are disjoint and exhaustive. |
| F02 | 74 | `#isYChar(String) [function,total]` | Total final-y predicate; equations R38–R40 are disjoint and exhaustive. |
| S26 | 75 | `#entry(String)` | Execution-harness item selecting the required entry point. |
| S27 | 76 | `#return(PyVal)` | Internal abrupt-return marker. |
| S28 | 77 | `#endCall` | Internal call-frame delimiter. |

The `[strict]` attributes above cause ordinary compiler-generated
heating/cooling rules. There are no local priority, `functional`,
`simplification`, `concrete`, or opaque declarations.

## Configuration

`semantic.k:79–85` declares `<py>` with:

- `<k>` initialized to the submitted `Program` followed by `#entry($INPUT)`;
- `<env>` for the current local mapping;
- `<functions>` for loaded function bindings; and
- `<stack>` for saved caller environments.

Every non-`<k>` cell is both read and/or written by local rules. No heap,
allocation, I/O, or exceptions are modeled because the submitted program uses
none.

## Operational and mathematical rules

Every explicit `rule` in `semantic.k` is inventoried below.

| ID | Lines | Rule | Decision |
|---|---:|---|---|
| R01 | 88 | `Module(SS) => SS` | Sound module-unwrapping step for the submitted constructor. |
| R02 | 89 | `S SS => S ~> SS` | Sound left-to-right statement sequencing. |
| R03 | 90 | `.Stmts => .K` | Sound completion of an empty statement sequence. |
| R04 | 91–92 | load `FuncDef` into `<functions>` | Sound for the submitted closure-free one-argument definition; overwrites the same key as Python module definition binding would. |
| R05 | 93 | `#entry(S) => Call(Name("vowels_count"),strVal(S))` | Explicit harness boundary selecting the contract entry. It does not summarize or bypass the function body. |
| R06 | 96 | `Int(I) => intVal(I)` | Sound literal interpretation. |
| R07 | 97 | `Str(S) => strVal(S)` | Sound literal interpretation. |
| R08 | 98–99 | local `Name` lookup in `<env>` | Sound for submitted variable use; unmatched names stop visibly. |
| R09 | 102 | direct builtin `len` on `strVal` | Sound on every reachable submitted call because the local environment contains only `s` and the exact function map contains only `vowels_count`; trusts K `lengthString`. |
| R10 | 103–106 | direct one-argument function call | Sound for the submitted call form: the strict argument is already evaluated, the exact function binding is selected, caller environment is pushed, and a fresh parameter-only local environment is installed. |
| R11 | 110 | `Return(V) => #return(V)` | Sound after strict evaluation of the return expression. |
| R12 | 111 | discard a following `Stmt` during return | Soundly discards only the rest of the active function body. |
| R13 | 112 | discard a following `Stmts` during return | Soundly discards only the rest of the active function body. |
| R14 | 113–115 | consume `#endCall`, restore env, pop stack | Sound value/control/state restoration. The arbitrary outer continuation remains. |
| R15 | 119–120 | true `If` branch | Sound and guard-disjoint from R16. |
| R16 | 121–122 | false `If` branch | Sound and exhaustive with R15 for `Bool`. |
| R17 | 123 | true-left `and` evaluates RHS | Sound short-circuit semantics. |
| R18 | 124 | false-left `and` returns false | Sound and guard-disjoint from R17. |
| R19 | 127 | integer `+` | Sound; trusts K unbounded `Int`, matching Python integers for this use. |
| R20 | 128 | stage `Compare` as `#compare` | Sound evaluation-order step. |
| R21 | 129–130 | equal strings produce true | Sound. |
| R22 | 131–132 | unequal strings produce false | Sound, disjoint from and exhaustive with R21. |
| R23 | 133–134 | equal integers produce true | Sound. |
| R24 | 135–136 | unequal integers produce false | Sound, disjoint from and exhaustive with R23. |
| R25 | 137–138 | membership in literal `aeiouAEIOU` | Sound on the submitted first-character operand; reduces to F01. |
| R26 | 139 | membership in literal `yY` | Sound on the submitted first-character operand; reduces to F02. |
| R27 | 141 | F01 true for `"a"` | Sound. |
| R28 | 142 | F01 true for `"e"` | Sound. |
| R29 | 143 | F01 true for `"i"` | Sound. |
| R30 | 144 | F01 true for `"o"` | Sound. |
| R31 | 145 | F01 true for `"u"` | Sound. |
| R32 | 146 | F01 true for `"A"` | Sound. |
| R33 | 147 | F01 true for `"E"` | Sound. |
| R34 | 148 | F01 true for `"I"` | Sound. |
| R35 | 149 | F01 true for `"O"` | Sound. |
| R36 | 150 | F01 true for `"U"` | Sound. |
| R37 | 151–156 | F01 false when unequal to all ten letters | Sound, disjoint from R27–R36, and completes totality for every K `String`. |
| R38 | 158 | F02 true for `"y"` | Sound. |
| R39 | 159 | F02 true for `"Y"` | Sound. |
| R40 | 160–161 | F02 false otherwise | Sound, disjoint from R38–R39, and completes totality. |
| R41 | 162–163 | string subscript via `substrString(S,I,I+1)` | Sound on the only reachable domain: `I=0` after the empty-string branch has been rejected. It is intentionally not a general Python negative/out-of-range indexing semantics. |
| R42 | 164–165 | exact `s[1:]` slice | Sound for every reachable string; trusts K `substrString`/`lengthString`. |

R09 and R41 are broader at the source-pattern level than their demonstrated
Python-equivalent reachable domains. This is a generated minimal semantics, not
a reusable full-Python definition. They cannot enable a false result for the
submitted program on any input string: exact loading produces no `len` shadow,
and every R41 use is index zero under `s != ""`. Therefore they are recorded as
scope/trust limitations rather than materially unsound rules. No rule encodes
the requested result or replaces execution with an unconstrained oracle.

## Proof-local mathematical definition

`verification.k` imports `SEMANTIC` and declares only
`#vowels(String) [function,total]`. It is not present in any operational
semantic rule.

| ID | Lines | Rule | Decision |
|---|---:|---|---|
| V01 | 11 | `#vowels("") => 0` | Sound empty-string base equation. |
| V02 | 13–16 | nonempty ordinary-vowel head adds one and recurses on tail | Sound; tail is strictly shorter. |
| V03 | 18–22 | non-vowel one-character `y/Y` gives one | Sound final-y case. |
| V04 | 24–29 | every other nonempty non-vowel head recurses without adding | Sound; disjoint from V02/V03 and tail is strictly shorter. |

Coverage: V01 handles empty; for nonempty strings F01 splits ordinary-vowel
versus non-vowel. The latter splits `(length == 1 and F02)` versus
`(length != 1 or not F02)`. The guards are pairwise disjoint and exhaustive.
Thus `[total]` has truthful coverage and recursion descends by one character.
`#vowels` is a definitional postcondition summary, not an operational bridge:
the submitted function body executes under R01–R42, and the proof must derive
that execution's value equals this independently defined summary.

## Reachability claims

`spec.k` contains no rules, functions, simplifications, priorities, or opaque
symbols. It contains:

| ID | Lines | Claim | Review |
|---|---:|---|---|
| C01 | 8–16 | `program-loads-solution` | Executes `solutionProgram` from empty cells and proves installation of the exact `vowelBody` binding before the entry call. |
| C02 | 20–28 | `vowels-count-correct` | For every K string, arbitrary caller env/stack/continuation, and the exact singleton body binding, executes the call and constrains the result to `intVal(#vowels(S))` while restoring caller state. Recursive uses are reachability circularities after semantic progress on the shorter tail. |

No candidate proof-local operational bridge exists. No same-symbol circular
oracle exists: `#vowels` occurs only in the postcondition and its mathematical
equations, never on the execution side.
