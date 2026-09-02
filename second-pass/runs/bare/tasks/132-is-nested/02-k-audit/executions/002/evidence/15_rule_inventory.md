# Exhaustive local K inventory

The only local K sources in the immutable candidate are `semantic.k`,
`verification.k`, and `spec.k`; there are no generated helper K files.
`domains.md` is the installed K standard domain library.

## Syntax, attributes, and configuration

| Source | Lines | Declaration |
|---|---:|---|
| semantic.k | 10 | `Bracket ::= lbr \| rbr` |
| semantic.k | 11 | inductive `BString ::= .BString \| Bracket BString` |
| semantic.k | 13 | `Module(Stmts)` |
| semantic.k | 14 | comma-separated `Strings` list |
| semantic.k | 15 | `Params(Strings)` |
| semantic.k | 17 | comma-separated `CmpOps` list |
| semantic.k | 18 | `CmpOp(String, Expr)` |
| semantic.k | 20–25 | `Expr`: `Name`, `Int`, `Bool`, `Str`, `BinOp`, `Compare` |
| semantic.k | 27 | juxtaposed `Stmts` list |
| semantic.k | 28–32 | `Stmt`: `FuncDef`, `Assign`, `For`, `If`, `Return` |
| semantic.k | 41–43 | `Val`: integer, Boolean, bracket-string wrappers |
| semantic.k | 44 | `Result ::= noResult \| Val` |
| semantic.k | 45 | stored `function(Params, Stmts)` |
| semantic.k | 47–48 | computation items `start` and `iterate` |
| semantic.k | 50–56 | `<py>` configuration with `<k>`, `<functions>`, `<env>`, `<result>` |
| semantic.k | 74–77 | partial functions `eval`, `add`, `compare`, `getVal` |
| semantic.k | 102 | partial function `choose` |
| semantic.k | 120 | partial function `getString` |
| verification.k | 8, 20, 26 | nullary AST aliases `loopBody`, `solutionBody`, `theSolution`, all `[function,total]` |
| verification.k | 33 | postcondition automaton `scan(Int,BString)`, `[function,total]` |

There are no local `[simplification]`, `[priority]`, `[owise]`, opaque, macro,
`anywhere`, `preserves-definedness`, or hook declarations. The only `total`
declarations are the four proof-local functions above.

## `semantic.k` rules

| ID | Lines | Exact role | Static judgment |
|---|---:|---|---|
| S01 | 59 | expose module statement list | Correct list/module execution |
| S02 | 60 | sequence a nonempty statement list | Correct left-to-right order |
| S03 | 61 | empty statement list becomes `.K` | Correct no-op |
| S04 | 63–64 | bind a function definition in `<functions>` | Correct for this capture-free definition |
| S05 | 66–70 | select exact `is_nested(string)` binding, install input local, execute stored body | Correct one-function call wrapper; binding is pinned |
| S06 | 79 | map lookup for `Name` through `getVal` | Correct for present locals; absent names visibly stick |
| S07 | 80 | unwrap a looked-up `Val` | Correct |
| S08 | 81 | integer literal | Correct |
| S09 | 82 | Boolean literal | Correct |
| S10 | 83 | literal `"["` | Correct one-character `BString` |
| S11 | 84 | literal `"]"` | Correct one-character `BString` |
| S12 | 85 | pure integer `+` expression | Correct shape and evaluation for used pure operands |
| S13 | 86–87 | one-link comparison expression | Correct for every comparison in the program |
| S14 | 89 | unbounded integer addition | Correct for Python integers used here |
| S15 | 91 | integer equality | Correct |
| S16 | 92 | integer less-than | Correct |
| S17 | 93–94 | `lbr == lbr` | Correct |
| S18 | 95–96 | `lbr == rbr` | Correct |
| S19 | 97–98 | `rbr == lbr` | Correct |
| S20 | 99–100 | `rbr == rbr` | Correct |
| S21 | 103 | choose then-list on true | Correct |
| S22 | 104 | choose else-list on false | Correct; disjoint from S21 |
| S23 | 107–108 | evaluate RHS against old environment, then map-update name | Correct assignment order for used pure expressions |
| S24 | 110–112 | evaluate pure guard against current environment and choose branch | Correct branch behavior |
| S25 | 116–118 | evaluate iterable, install a dummy loop target, then iterate | Result-faithful for this program; on empty input Python leaves the target unbound, but this program never reads it and `Return` discards the local frame |
| S26 | 121 | unwrap bracket-string iterable | Correct |
| S27 | 123 | empty iterator terminates loop | Correct |
| S28 | 124–126 | bind `lbr`, execute body, continue with suffix | Correct order and state update |
| S29 | 127–129 | bind `rbr`, execute body, continue with suffix | Correct order and state update |
| S30 | 133–136 | evaluate return value, discard continuation, clear wrapper frame/maps, store result | Correct abrupt return/result behavior in the one-function wrapper |

All function-equation guards are constructor-disjoint where they overlap by
symbol. Used cases are covered. The evaluator intentionally remains partial on
unsupported operators, types, missing bindings, and unused language forms, so
these cases stick rather than fabricate a result.

## `verification.k` equations

| ID | Lines | Class | Static judgment |
|---|---:|---|---|
| V01 | 9–18 | definitional AST alias | Exact constructor body of the translated loop |
| V02 | 21–24 | definitional AST alias | Exact constructor body of the translated function |
| V03 | 27–28 | definitional AST alias | Exact translated module/function binding |
| V04 | 35 | definitional postcondition summary | Empty suffix cannot complete `[[]]` |
| V05 | 37 | scan transition | state 0 + `[` → state 1 |
| V06 | 38 | scan transition | state 0 + `]` → state 0 |
| V07 | 40 | scan transition | state 1 + `[` → state 2 |
| V08 | 41 | scan transition | state 1 + `]` → state 1 |
| V09 | 43 | scan transition | state 2 + `[` → state 2 |
| V10 | 44 | scan transition | state 2 + `]` → state 3 |
| V11 | 46 | scan transition | state 3 + `[` → state 3 |
| V12 | 47 | scan transition | state 3 + `]` → true, suffix irrelevant |

V01–V03 name constructor trees and do not replace execution. V04–V12 define
only the postcondition automaton and never rewrite a program term. The `scan`
equations are terminating and pairwise disjoint; states 0–3 cover every use.
The `[total]` declaration also gives arbitrary values to out-of-range,
nonempty states such as `scan(4,lbr .BString)`, but no rule, claim, program path,
or postcondition can produce such a state. It does not encode a task answer or
preempt execution.

## Claims and construct mapping

`spec.k` has four cumulative loop-suffix claims for concrete automaton states
0, 1, 2, and 3, followed by one universal entry claim. Every claim constrains
`<result>` to `boolVal(scan(State,BS))`; none contains a free result variable.

The submitted constructors map as follows:

| Program constructor | Declaration | Executing rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | lines 13, 15, 28 | S01–S05 |
| statement juxtaposition/empty branches | line 27 | S02–S03 |
| `Name`, `Int`, `Bool`, `Str` | lines 20–23 | S06–S11 |
| `BinOp("+",...)` | line 24 | S12, S14 |
| `Compare`/`CmpOp` (`==`, `<`) | lines 17–18, 25 | S13, S15–S20 |
| `Assign` | line 29 | S23 |
| `If` | line 31 | S24, S21–S22 |
| `For` | line 30 | S25–S29 |
| `Return` | line 32 | S30 |

Trusted installed primitives are K sequencing/list units, `Int` arithmetic and
comparison, `Bool`, `String` tokens, and `Map` lookup/update. No local opaque
symbol, oracle, operational bridge, priority rule, or simplification lemma
contributes to closure.
