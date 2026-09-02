# Exhaustive local K inventory

Sources inventoried: scratch copies of `semantic.k`, `verification.k`, and
`spec.k`. There are 19 local `rule` sentences and one reachability `claim`.
There are no helper K files, aliases, macros, contexts, priority rules,
`[total]`, `[functional]`, `[simplification]`, `[concrete]`, `[owise]`, or
opaque declarations.

## Local syntax and configuration

| ID | Source | Declaration | Use and judgment |
|---|---|---|---|
| S1 | semantic.k:9 | `Program ::= Module(Stmt)` | Exact outer constructor used by `solution.mpy`. |
| S2 | semantic.k:10-11 | `Stmt ::= FuncDef(String, Params, Stmt)` | Exact one-function binding used by the submitted module. |
| S3 | semantic.k:12 | `Stmt ::= Return(Expr)` | Exact sole statement used by the submitted function. |
| S4 | semantic.k:13 | `Params ::= Params(String)` | Exact one-parameter signature used by `by_length`. |
| S5 | semantic.k:15 | `Expr ::= Int(Int)` | All digit constants 1 through 9. |
| S6 | semantic.k:16 | `Expr ::= Str(String)` | The nine output-name literals. |
| S7 | semantic.k:17 | `Expr ::= Name(String)` | The parameter reference `arr`. |
| S8 | semantic.k:18 | `Expr ::= ListExpr(Expr)` | Each singleton output block. |
| S9 | semantic.k:19-20 | `Expr ::= Attribute(Expr, String)` | Used only inside `Call` for `arr.count`. |
| S10 | semantic.k:21 | `Expr ::= Call(Expr, Expr)` | The nine calls to `arr.count(digit)`. |
| S11 | semantic.k:22-23 | `Expr ::= BinOp(String, Expr, Expr)` | Used for list `+` and list-by-integer `*`. |
| S12 | semantic.k:27 | `Int`, `String`, and `PyList` are `Value` subsorts | Covers all runtime values exercised by the submitted program. |
| S13 | semantic.k:28 | `PyList ::= pyList(PyVals)` | Abstract Python list representation. |
| S14 | semantic.k:29-30 | empty and cons `PyVals` | Finite list representation; the element sort is broader than the integer source domain. |
| S15 | semantic.k:38-44 | `<k>`, `<program>`, `<input>`, `<result>` configuration | `k` is control, `program` is preserved provenance, `input` is the parameter value, and `result` is the only output state. No heap, I/O, or allocation is used by this program. |
| S16 | semantic.k:46-47 | `KItem ::= init(Program) \| noResult` | Entry control and initial-result marker. |
| S17 | semantic.k:55 | `Value ::= #eval(Expr, Map) [function]` | Structural evaluator. No totality attribute; equations cover every expression constructor used by the program. |
| S18 | semantic.k:67-71 | `[function]` declarations for `#add`, `#multiply`, `#count`, `#appendVals`, and `#repeatVals` | Models only the operand combinations used by this task; no false totality claim is made outside them. |
| S19 | verification.k:7 | `Program ::= #solutionProgram [function]` | Zero-argument definitional name for the exact submitted constructor term. |
| S20 | verification.k:42 | `Value ::= #byLength(PyVals) [function]` | Definitional result summary, not an opaque value. |

## Rule-by-rule review

| ID | Source | Rule | Complete local domain and judgment |
|---|---|---|---|
| R1 | semantic.k:51-53 | `init(Module(FuncDef(...Return(E))))` consumes `<k>` and stores `#eval(E, X \|-> V)` | Sound for the exact single-function/single-return module shape used here: binds the sole parameter to the `PyList` input, preserves input and program, writes result, and consumes control. It does not test equality with the redundant `<program>` cell, so it is deliberately not a reusable semantics for arbitrary mismatched configurations. The entry claim and every parser-created initial configuration use the same program in both places; no false conclusion follows on the real-program initial states. |
| R2 | semantic.k:56 | `#eval(Int(I), ENV) => I` | Correct integer-literal evaluation; environment is irrelevant. |
| R3 | semantic.k:57 | `#eval(Str(S), ENV) => S` | Correct string-literal evaluation; environment is irrelevant. |
| R4 | semantic.k:58 | `#eval(Name(X), X \|-> V) => V` | Correct for the exact singleton environment constructed by R1. It is intentionally partial for larger maps and has no `[total]` claim. |
| R5 | semantic.k:59 | singleton `ListExpr` evaluates to `pyList(value :: empty)` | Correct for every list literal used by the submitted program, all of which have exactly one element. |
| R6 | semantic.k:60-61 | `BinOp("+", L, R)` maps to `#add(#eval(L), #eval(R))` | Correct for the pure list expressions used here. Python's left-to-right order has no observable distinction because neither operand can mutate state or raise on an intended integer-list input. |
| R7 | semantic.k:62-63 | `BinOp("*", L, R)` maps to `#multiply(#eval(L), #eval(R))` | Correct for the exact singleton-list times integer-count operands. |
| R8 | semantic.k:64-65 | `Call(Attribute(BASE,"count"),ARG)` maps to `#count(#eval(BASE),#eval(ARG))` | Correct binding for the formal `PyList` receiver and integer argument. No subclass, custom method, side effect, or exception is present in the intended input model. |
| R9 | semantic.k:73 | `#add(pyList(XS),pyList(YS))` delegates to append | Correct Python-list concatenation on the modeled values. |
| R10 | semantic.k:74 | append-empty returns the right list | Standard true base equation. |
| R11 | semantic.k:75 | append-cons preserves the head and recurses | Standard true inductive equation; strictly decreases the first list. |
| R12 | semantic.k:77 | list multiplication delegates to repeat | Correct for a `PyList` and integer multiplier. |
| R13 | semantic.k:78 | repeat with `N <= 0` is empty | Matches Python list multiplication for zero and negative integers. |
| R14 | semantic.k:79-80 | positive repeat appends one copy and recurses at `N-1` | Correct; strictly decreases positive `N`. Its guard is disjoint from and exhaustive with R13 over `Int`. |
| R15 | semantic.k:82 | count on an empty list is zero | Correct base equation. |
| R16 | semantic.k:83-85 | equal integer head contributes one and recurses | Correct `list.count` equation for integer lists. |
| R17 | semantic.k:86-88 | unequal integer head contributes zero and recurses | Correct and disjoint from R16; integer equality/inequality guards are exhaustive and recursion decreases the tail. `#count` is intentionally partial for string or nested-list heads, which lie outside the stated array-of-integers domain. |
| R18 | verification.k:8-37 | `#solutionProgram` expands to a fixed `Module(FuncDef(...))` | Truthful definitional equation. `program_term_compare.py` mechanically matched this RHS to regenerated `solution.mpy`; it does not replace body execution. |
| R19 | verification.k:43-60 | `#byLength(XS)` expands to descending name blocks repeated according to counts | Truthful mathematical characterization for integer lists. It uses the defined `#add`, `#multiply`, and `#count` functions and introduces no fresh or opaque result. Its equivalence to sort/filter/reverse/name replacement is an elementary but informal intent bridge, supported—not proved—by differential testing. |
| C1 | spec.k:7-11 | sole entry reachability claim | No explicit `requires`; starts with the exact program in `<k>` and `<program>`, an arbitrary finite `PyVals` tail, and `noResult`; ends with `.K`, the same program/input, and result `#byLength(XS)`. For intended all-integer lists it is result-constraining and covers every finite length. |

## Coverage, overlaps, control, and state

Every constructor in `solution.mpy` maps to S1-S11 and is evaluated by R1-R8.
The material operations are list construction, integer/string literals,
parameter lookup, list count, list repetition, list concatenation, and return;
R2-R17 cover all of them. The only guarded overlaps are R13/R14 and R16/R17;
their guards are pairwise disjoint and exhaustive over the intended sorts.
Other left-hand sides are constructor-disjoint. All recursion descends on a
proper list tail or a positive integer.

There is no loop, helper claim, call stack, heap, allocation, output, exception
handler, break/continue effect, priority override, or simplification axiom.
The exact intended program on a finite integer list cannot raise under CPython,
so the omitted exception machinery is not a used construct. The evaluator's
equational treatment does not preserve Python evaluation order in general, but
the submitted operands are pure and non-raising on the intended domain, making
the order difference unobservable here.

No rule was classified as materially unsound, so there is no false-conclusion
witness to report. The two narrower limitations are instead stated as evidence
gaps: R1 is over-broad on artificial mismatched `<k>`/`<program>` states, and
R17 does not evaluate non-integer list elements. Neither state occurs in the
real entry claim over the source-contract domain, and neither can prove a false
result for an intended integer-list input.
