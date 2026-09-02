# Static rule review ledger

This ledger accompanies `27-k-inventory.log`, which contains every source
configuration, syntax declaration, context, rule, and claim with its file and
line. The inventory totals are 1 configuration, 234 syntax declarations, 5
contexts, 708 rules, and 4 claims. The judgments below cover every inventoried
item by file; proof-local items are then reviewed individually.

## Supplied fixed semantics, by file

| File | Inventory | Proof dependency and disposition |
|---|---:|---|
| `semantics.k` | assembly only | Imports the proof-side `MPY` modules and keeps concrete-only rules in `MPY-KRUN`; correct module separation. |
| `semantics/syntax.k` | 16 syntax | Declares all AST constructors. The used `Module`, `FuncDef`, `Params`, `If`, `Compare`, `CmpOp`, `Name`, `Int`, `Return`, `TupleExpr`, `BinOp`, `Assign`, `AugAssign`, and `Call` shapes match the trusted translator output. Strict/seqstrict attributes give the used expressions left-to-right evaluation. |
| `semantics/core.k` | 1 configuration, 37 syntax, 46 rules | Used: initial cells, module loading, statement sequencing, name lookup, builtin root construction, left-to-right argument evaluation, integer literals, operator dispatch declarations, and `Vals` conversion. Their cell effects agree with the entry/final claims. Unused heap/cell/collection helpers do not contribute. No false conclusion witness was identified. |
| `semantics/operators.k` | 2 contexts, 10 rules | Used generic `BinOp` and `Compare` dispatch plus compare operand contexts preserve evaluation order. Heap-reference priority rules are unreachable because this program uses only integers. No false conclusion witness was identified. |
| `semantics/int.k` | 1 syntax, 16 rules | Used `+`, `-`, `*`, `%`, `//`, `<`, and `==`. For the proof domain all divisors are the positive constants 2, 10, 11, and 100; `pyMod` plus `(a-r)/b` implements Python floor division, including the program's possible negative numerator `n % 100 - hundreds`. Other cases are unused. |
| `semantics/controls.k` | 3 syntax, 34 rules | Used simple-name assignment, simple-name augmented addition, and `If` branching. The rules update only the active callee scope and preserve every other cell. Loop, import, heap-reference, and expression-statement rules are unused. No proof rule preempts them. |
| `semantics/functions.k` | 4 syntax, 15 rules | Used top-level function definition, parameter binding, `Return`, `#endcall`, and `#pop`. The frame saves/restores the caller continuation/environment, deletes the callee scope, restores `scopeLoc`, and leaves heap allocation monotone. Annotated closures are unused. |
| `semantics/call.k` | 3 syntax, 21 rules | Used callee lookup, left-to-right argument evaluation, and `closureVal` dispatch. Binding/body/control/stack effects match the real call. Builtin, method, heap-reference, and annotated closure cases are unused. |
| `semantics/tuple.k` | 4 syntax, 21 rules | Used tuple literal evaluation and ordered conversion from evaluated arguments. Tuple comparison, iteration, target binding, and unpacking are unused. |
| `semantics/assert.k` | 3 rules | Used only by the independent LLVM smoke harness, never by a proof claim. It cannot contribute to `#Top`. |
| `semantics/bool.k` | 1 context, 13 rules | Unused; the program uses comparison-produced K booleans directly in `If`, not Python `BoolOp` nodes. No false conclusion witness was identified. |
| `semantics/builtins.k` | 38 syntax, 137 rules | Unused except that builtin values exist in the root map. Its opaque `md5hexCodes` is not reachable and cannot affect control or result. No candidate rule depends on any builtin summary. |
| `semantics/comprehension.k` | 3 syntax, 7 rules | Unused. |
| `semantics/concrete.k` | 5 syntax, 16 rules | Present only in the LLVM definition and unused by this program. It is absent from the Haskell `MPY` proof definition. |
| `semantics/dict.k` | 12 syntax, 28 rules | Unused. |
| `semantics/float.k` | 34 syntax, 121 rules | Unused. Its 22 float-related `symbol(...)` declarations (many with `no-evaluators`) are fixed-semantics opaque primitives, but no float term occurs in the program, spec, or residuals. |
| `semantics/iter.k` | 1 syntax | Unused iterator protocol declarations. |
| `semantics/list.k` | 5 syntax, 27 rules | Unused. |
| `semantics/methods.k` | 27 syntax, 75 rules | Unused. |
| `semantics/range.k` | 2 syntax, 6 rules | Unused. |
| `semantics/set.k` | 6 syntax, 12 rules | Unused. |
| `semantics/sort.k` | 6 syntax, 19 rules | Unused. Opaque `sortVS` and `sortKeyVS` cannot affect this proof. |
| `semantics/str.k` | 5 syntax, 28 rules | Unused. Compiler warnings about unused tail variables in `strLt` are irrelevant to this integer-only proof. |
| `semantics/subscript.k` | 2 contexts, 15 syntax, 40 rules | Unused. Its intentionally partial/totalized positional-access boundary cannot affect this proof. |

The supplied tree also contains 45 priority-bearing rules. Every priority rule
is shown with context in `28-special-attributes.log`; none is proof-local, and
none matches the integer-only program path except ordinary closure-cell
preemption guards, whose `$cells` conditions are false in this plain frame.
There are no simplification rules in the candidate proof. The 25 `symbol(...)`
declarations are exactly the 22 float symbols, `md5hexCodes`, `sortVS`, and
`sortKeyVS`; none is reachable.

## Proof-local declarations and rules

| Location | Extension | Class and complete judgment |
|---|---|---|
| `verification.k:8-56` | `solutionBody` and its equation | Definitional program term, one unconditional equation. Mechanical normalized constructor comparison has the same SHA-256 as regenerated `solution.mpy`. No abstraction or skipped execution. |
| `verification.k:58-64` | `solutionModule` and its equation | Definitional module/binding wrapper. It binds the required name and one parameter to exactly `solutionBody`. |
| `verification.k:68-71` | `#runEvenOdd(N)` | Operational entry wrapper, not a summary: it expands to fixed-semantics `#loadAll(solutionModule) ~> Call(Name("even_odd_palindrome"), N)`. It does not fabricate a return, alter cells, discard a continuation, or bypass lookup/call/body execution. |
| `verification.k:75-76` | total `leadingDigit(N)` | Mathematical definition `N /Int 100`; one unconditional, total, terminating equation. |
| `verification.k:78-80` | total `currentBlock(N)` | Mathematical definition `(N %Int 100 -Int leadingDigit(N) +Int 10) /Int 10`; one unconditional, total, terminating equation. |
| `verification.k:82-93` | `evenPalindromes` (4 equations) | Postcondition-only definitional summary. Guards `1..9`, `10..99`, `100..999`, and exact `1000` are satisfiable, pairwise disjoint, and cover the full source domain. The equations terminate and have no overlap. They never replace program execution. |
| `verification.k:95-107` | `oddPalindromes` (4 equations) | Same classification and guard analysis as the even summary. |
| `spec.k:6-31` | entry claim 1 | Executes the real body for every integer `1 <= N < 10` and requires its returned tuple to equal both summary components while pinning all cells. |
| `spec.k:33-58` | entry claim 2 | Same, for `10 <= N < 100`. |
| `spec.k:60-85` | entry claim 3 | Same, for `100 <= N < 1000`. |
| `spec.k:87-112` | entry claim 4 | Same, for the satisfiable singleton `N = 1000`. |

The summary-to-contract derivation is: one-digit palindromes give `(floor(n/2),
ceil(n/2))`; two-digit palindromes are `11*j`, so their parity is the parity of
`j`; three-digit palindromes are `101*a + 10*b`, so parity is the parity of the
leading digit `a`, each completed leading-digit block has ten values, and
`currentBlock` counts the current block's admissible `b`. At `1000`, all 90
three-digit palindromes plus the 18 shorter ones give `(48, 60)`. This is
ordinary finite mathematics and is independently exhaustively checked for all
1,000 inputs, but it is not itself represented as a K palindrome predicate.
