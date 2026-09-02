# Exhaustive local K inventory and assessment

This inventory covers the copied source files under
`/tmp/audit-work/104-unique-digits/candidate`. There are no candidate helper K
files. Imported `INT`, `BOOL`, string, and list machinery is recorded as a
built-in trust boundary rather than as candidate-authored rules.

## `semantic.k`: syntax and configuration

| Lines | Declaration | Attributes / role | Assessment |
|---|---|---|---|
| 8-10 | `Program ::= Module(Stmts) \| solutionProgram`; `Stmts ::= List{Stmt,""}` | `solutionProgram` is `[function,total]` | The AST container and statement list parse the submitted term. `solutionProgram` is a proof constant, not source syntax. |
| 12-14 | `Stmt ::= FuncDef(...) \| If(...) \| Return(...)` | Constructors only | Every statement constructor used by `solution.mpy` is declared, but none has an evaluation rule. |
| 16-17 | `Params( Strings )`; comma-separated `Strings` | Constructors/list only | Parses parameters; there is no binding behavior. |
| 19-25 | `Expr ::= Name \| Int \| Bool \| BinOp \| Compare \| Call \| ListComp` | Constructors only | Parses every submitted expression; none has evaluation, lookup, call, return, or comprehension rules. Operator strings `%`, `//`, and `==` are not interpreted at this AST level. |
| 27-31 | `Exprs`, `CmpOp`, `CmpOps`, `CompFor`, `CompFors` | Constructors/lists only | Parses call arguments, comparisons, and the comprehension clause; none has behavior. |
| 33-36 | `IntSeq ::= .Ints \| cons(Int,IntSeq)`; `PyVal ::= pyList(IntSeq) \| pyBool(Bool)` | Abstract input/result data | Finite integer sequences are the entire represented list model. `pyBool` is unused. |
| 44 | `KItem ::= invoke(String,PyVal)` | Uninterpreted invocation marker | This is not a Python call constructor and has no generic call semantics. |
| 46 | `<k> $PGM:Program ~> invoke("unique_digits",$ARGS:PyVal) </k>` | Sole configuration cell | There is no environment, frame/call stack, heap, iterator, exception, or built-in namespace cell. |

Construct mapping for the submitted `solution.mpy`:

- `Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`, `CmpOp`, `Int`,
  `Return`, `Bool`, `BinOp("%",...)`, `BinOp("//",...)`, `Call`,
  `ListComp`, and `CompFor` all have grammar declarations.
- None has an operational rule. Each occurs only inside the structural
  `solutionProgram` equation and `isUniqueDigitsProgram` pattern.
- Therefore the semantics does not evaluate either function body or any
  individual construct used by the program.

## `semantic.k`: all 16 local rules

| Lines | Rule(s) | Classification | Coverage / overlap / descent / assessment |
|---|---|---|---|
| 51-66 | `solutionProgram =>` the exact submitted `Module(...)` AST | Definitional identity (1 rule) | Truthful because trusted regeneration is byte-identical. Total for its nullary domain. It pins syntax only and proves no execution property. |
| 68-85 | `isUniqueDigitsProgram(exact AST) => true` | Partial structural recognizer (1 rule) | Truthful on its only equation. It is deliberately not `[total]`; other programs remain unevaluated. It supplies syntactic identity, not semantic equivalence. |
| 90-96 | `oddDigits(N)` negative, zero, positive-even, and positive-odd-recursive cases | Definitional mathematical summary (4 rules), `[function,total]` | Guards are disjoint and cover every K `Int`; positive recursion strictly decreases under `/Int 10`. On positive integers it computes whether every decimal digit is odd. The negative case is an out-of-contract convention and is not Python-equivalent, but the verdict does not rely on an out-of-domain witness. |
| 98-103 | Empty, keep-head, and drop-head equations for `filterOddDigits` | Definitional summary (3 rules), `[function,total]` | Empty/cons cases cover `IntSeq`; keep/drop guards are complementary because `oddDigits` is total. Recursion descends on the tail and preserves order and multiplicity. |
| 105-110 | Empty, insert-before, and recurse-after equations for `insertSorted` | Mathematical helper (3 rules), `[function,total]` | Empty/cons cover `IntSeq`; `N <= M` and `N > M` are disjoint and exhaustive on mathematical integers. Tail recursion descends and preserves duplicates. |
| 112-114 | Empty and cons equations for `sortInts` | Mathematical helper (2 rules), `[function,total]` | Exhaustive on finite `IntSeq`; structural recursion descends. This is insertion sort. |
| 116-117 | `uniqueDigitsMeaning(NS) => sortInts(filterOddDigits(NS))` | Task-answer summary (1 rule), `[function,total]` | A total name for the desired mathematical result. It is not independently connected to execution of the submitted Python bodies. |
| 119-121 | Exact recognized `P ~> invoke("unique_digits",pyList(NS)) => pyList(uniqueDigitsMeaning(NS))` | **Operational bridge** (1 ordinary semantic rule) | This is the only execution rule. It accepts every `IntSeq` and an arbitrary framed `<k>` suffix, consumes the whole program and invocation, and fabricates the task-answer summary without bindings, evaluation, calls, recursion, comprehension, `sorted`, returns, state, or exceptions. No auxiliary execution claim or connection theorem justifies it. |

The operational bridge has a concrete false-behavior witness on the intended
positive-integer domain. Let `D = int("1" * 1200)` and
`NS = cons(D,.Ints)`. The guard recognizes the exact submitted AST and the rule
returns `pyList(cons(D,.Ints))` (`stage4_krun_deep_positive.log`, exit 0).
Actual CPython execution of the submitted `solution.py` raises
`RecursionError`, while the trusted canonical function returns `[D]`
(`stage2_differential.log`). Thus the bridge changes exceptional control into a
normal result. Independently of that resource witness, the rule is an
unproved, result-bearing replacement of program-defined computation.

Changing the second branch of `no_even_digit` to return `True` causes the
translated program to remain stuck at its AST under the K definition even
though Python evaluates the mutation (`stage4_mutated_body_krun.log` and
`stage4_mutated_body_python.log`). This confirms exact syntactic sensitivity
but also confirms there are no construct semantics behind the recognizer.

## `verification.k`: all six local rules

| Lines | Rule(s) | Attributes / assessment |
|---|---|---|
| 7-9 | Empty and cons equations for `positiveInts` | `[function,total]`; exhaustive structural recursion. It states exactly that every represented integer is greater than zero. |
| 14-15 | `allDecimalDigitsOdd(N) => oddDigits(N)` | `[function,total]`; truthful alias, not a theorem about the Python helper. |
| 17-19 | `retainAllOddDigitItems(NS) => filterOddDigits(NS)` | `[function,total]`; truthful alias. |
| 21-22 | `inIncreasingOrder(NS) => sortInts(NS)` | `[function,total]`; truthful alias. |
| 24-26 | `uniqueDigitsSpec(NS) => inIncreasingOrder(retainAllOddDigitItems(NS))` | `[function,total]`; exact mathematical postcondition. It reduces to the same functions used by the operational bridge, making the entry proof circular as a program-correctness argument. |

## `spec.k`: five claims

| Lines | Claim | Assessment |
|---|---|---|
| 8-10 | Universal entry claim for arbitrary `NS` with `positiveInts(NS)` | Result-constraining, but closes because the operational bridge and postcondition reduce to the same hand-written filter/sort equations. |
| 13 | `allDecimalDigitsOdd(97531) => true` | Ground equation check; reconstructed K warns it is trivial. |
| 14 | `allDecimalDigitsOdd(1422) => false` | Ground equation check; reconstructed K warns it is trivial. |
| 17-19 | First prompt example | Exact ground result, but it uses the same bridge. |
| 21-23 | Second prompt example | Exact ground result, but it uses the same bridge. |

There are no loop claims, helper-body execution claims, connection theorems,
simplification rules, priority rules, `[functional]` declarations, `[opaque]`
attributes, `[concrete]` rules, or proof-local ordinary operational rules.
There are no pairwise conflicting candidate equations in the mathematical
helpers. The material soundness failure is the whole-program operational
bridge, not the filter/sort arithmetic itself.
