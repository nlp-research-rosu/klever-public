# Rule-by-rule static soundness review

This review uses the numbering in `stage5_static_inventory.md`. `T-SOUND`
means the rule is faithful on every state reachable from the submitted program
for positive integer inputs. `LIMIT` identifies a broader-language or execution
model limitation that does not create a false result on the candidate's 13
ground proof inputs. `REAL-MISMATCH` has a witness for the real submitted
program on the intended positive-integer domain. `UNUSED-SOUND` is a truthful
proof-local definition that no submitted claim depends on.

## `semantic.k` rules 01–40

| Rule | Class | Finding | Review |
|---|---|---|---|
| 01 | operational initialization | T-SOUND | Reads the parsed module, collects its two bindings, and invokes the required `factorize` entry point at `$INPUT`. |
| 02 | result plumbing | T-SOUND | Moves the halted value into `<result>` without changing it. |
| 03 | call/stack operation | REAL-MISMATCH | Binding, arguments, local environment, continuation, and function map are preserved, but stack growth is unbounded. Witness: at `n=1000003`, repeated applications let K return `[1000003]`; CPython raises `RecursionError`. |
| 04 | statement execution | T-SOUND | Empty statement sequence continues with the saved computation. |
| 05 | return control | T-SOUND | Evaluates the returned expression before initiating return. The omitted exception/finally mechanisms are unused by this program. |
| 06 | conditional control | T-SOUND | Evaluates the guard before selecting a branch, then continues with remaining statements. |
| 07 | true branch | T-SOUND | Guard `B` and rule 08's `notBool B` are disjoint and exhaustive for concrete booleans. |
| 08 | false branch | T-SOUND | See rule 07. |
| 09 | return/frame pop | T-SOUND | Discards only the returning function's active continuation, restores the caller environment, preserves functions/result, and pops one frame. |
| 10 | final halt | T-SOUND | Converts the top-level returned value to `Halted`; applicable only with `noResult`. |
| 11 | integer literal | T-SOUND | Exact arbitrary-precision integer injection. |
| 12 | name lookup | T-SOUND | Selects the map binding and preserves the environment. All target names are bound. |
| 13 | empty list | T-SOUND | Exact empty list value. |
| 14 | singleton-list evaluation | T-SOUND | The only nonempty list literal shape in the submitted program is singleton. |
| 15 | singleton-list construction | T-SOUND | Exact list wrapping after element evaluation. |
| 16 | binary evaluation start | T-SOUND | Enforces Python's left-before-right evaluation order. |
| 17 | binary right operand | T-SOUND | Preserves the evaluated left value while evaluating the right. |
| 18 | binary operation dispatch | T-SOUND | Applies the operation only after both operands are values. |
| 19 | comparison evaluation start | T-SOUND | Enforces left-before-right evaluation for the one-comparator target expressions. |
| 20 | comparison right operand | T-SOUND | Preserves the evaluated left value. |
| 21 | comparison dispatch | T-SOUND | Applies comparison to evaluated values. |
| 22 | one-argument call start | T-SOUND | The target callee is always a direct global `Name`; arbitrary callable expressions are intentionally unmodeled. |
| 23 | one-argument invocation | T-SOUND | Passes the already evaluated value as the sole argument. |
| 24 | two-argument call start | T-SOUND | Begins left-to-right argument evaluation for the only two-argument calls in the target. |
| 25 | second argument evaluation | T-SOUND | Preserves the first argument value. |
| 26 | two-argument invocation | T-SOUND | Preserves argument order in the invocation list. |
| 27 | empty function collection | T-SOUND | Exact empty map. |
| 28 | typing import collection | LIMIT | Ignores `from typing import List`. This is inert for the submitted translated bodies in the normal HumanEval environment, but does not model import failure or side effects. |
| 29 | function collection | T-SOUND for target; LIMIT globally | The two submitted names are unique. For a different module with duplicate `def f`, this right-to-left collection lets the earlier definition overwrite the later one, unlike Python. That broader-language witness is outside the immutable submitted program and is not used as a target unsoundness claim. |
| 30 | parameter binding dispatch | T-SOUND | Delegates exact target parameter/value lists. |
| 31 | empty parameter binding | T-SOUND | Exact zero-tail base case. |
| 32 | recursive parameter binding | T-SOUND for target; LIMIT globally | Correct for equal arity, which every target call has. Python `TypeError` on mismatched arity is left as a stuck K term. |
| 33 | integer addition | T-SOUND | Exact on Python integers. |
| 34 | integer multiplication | T-SOUND | Exact on Python integers. |
| 35 | list concatenation | T-SOUND | Exact for immutable value lists. |
| 36 | integer remainder | T-SOUND for target; LIMIT globally | All reachable divisors and dividends are positive, where `%Int` agrees with Python. Off target, `-3 % 2` is `1` in Python but t-remainder is `-1` in K. |
| 37 | integer floor division | T-SOUND for target; LIMIT globally | All reachable operands are positive. Off target, Python `-3 // 2 == -2`, while K `/Int` rounds toward zero to `-1`. |
| 38 | integer less-than | T-SOUND | Exact. |
| 39 | integer greater-than | T-SOUND | Exact. |
| 40 | integer equality | T-SOUND | Exact for the target integer operands. |

The collective resource mismatch attached to rule 03 is material: it enables a
false normal-return conclusion for the actual submitted Python program at a
positive input, as recorded in `stage3_concrete_execution.log`. The other
`LIMIT` cases have no false target-program witness and are therefore recorded
as narrower evidence/model limitations, not as target-unsound rules.

## `verification.k` rules 41–62

| Rule | Class | Finding | Review |
|---|---|---|---|
| 41 | definitional program term | T-SOUND | The extracted RHS is constructor-AST equal to trusted regeneration of `solution.mpy`. |
| 42 | definitional function map | T-SOUND | Applies rule 44 to the exact rule-41 module. |
| 43 | definitional entry state | T-SOUND | Invokes the actual collected `factorize` binding with `N`, empty locals/stack, and `Finish`; it does not replace execution with an oracle. |
| 44 | definitional collector projection | T-SOUND | Projects the module statement list into the semantic collector. |
| 45 | `FactorFrom` equation | UNUSED-SOUND | Correct empty result for `N < 2`; submitted claims never reference `FactorFrom`. |
| 46 | `FactorFrom` equation | UNUSED-SOUND | Correct residual factor when `D² > N` under the stated positive guards. |
| 47 | `FactorFrom` equation | UNUSED-SOUND | Correctly emits a divisor and recurs on positive quotient under divisibility guard. |
| 48 | `FactorFrom` equation | UNUSED-SOUND | Correctly advances the trial divisor under the complementary nondivisibility guard. |
| 49 | factorization specification | UNUSED-SOUND | Names `FactorFrom(N,2)` but is absent from all claims. |
| 50 | list constructor helper | UNUSED-SOUND | Exact prepend equation; used only by unused `FactorFrom`. |
| 51 | product equation | T-SOUND | Empty product is 1. |
| 52 | product equation | T-SOUND | Exact structural product over integer list values. |
| 53 | order equation | T-SOUND | Empty list is ordered above any lower bound. |
| 54 | order equation | T-SOUND | Checks the current lower bound and recurs with the current item. |
| 55 | execution observation | T-SOUND | Extracts exactly the value from a halted machine; no fresh or opaque result is introduced. |
| 56 | divisor search equation | T-SOUND on use domain | If `D² > N` for `N >= 2, D >= 2`, no divisor at or above `D` is needed for primality. |
| 57 | divisor search equation | T-SOUND on use domain | Finds a concrete divisor under a divisibility guard. |
| 58 | divisor search equation | T-SOUND on use domain | Advances under the complementary nondivisibility guard. |
| 59 | primality equation | T-SOUND | Combines the lower bound with exhaustive divisor search from 2. |
| 60 | all-prime equation | T-SOUND | Empty list vacuously satisfies the property. |
| 61 | all-prime equation | T-SOUND | Exact structural conjunction. |
| 62 | contract equation | T-SOUND | Requires product equality, nondecreasing factors starting at 2, and primality, exactly matching the positive-integer factorization contract. |

Rules 45–50 do not contribute to closure of any submitted claim and therefore
cannot smuggle the task answer into the proof. Rules 51–62 inspect the concrete
value obtained by executing rules 41–44 plus `semantic.k`.

## Declarations, overlaps, and construct coverage

- The inventory contains 37 local syntax/configuration declarations and 62
  rules. There are no generated helper K files.
- `[function]` occurs on `Machine`, the semantic helper functions, the exact
  program constructors, and the mathematical observers. There are no
  `[total]`, `[functional]`, `[simplification]`, priority, `owise`, `anywhere`,
  macro, or opaque declarations.
- The reachable rule families are pairwise disjoint by constructor or by
  complementary boolean/integer guards. `FactorFrom` is disjoint and exhaustive
  only for its stated `N < 2` or `N >= 2, D >= 2` domains; `HasDivisor` is used
  only from `D=2` with candidate factors `N >= 2`.
- `solution.mpy` uses `Module`, `ImportFrom`, `FuncDef`, `Params`, sequential
  `Stmts`, `If`, `Return`, `Int`, `Name`, `BinOp` (`+`, `*`, `%`, `//`),
  `Compare` (`<`, `>`, `==`), empty/singleton `ListExpr`, and one/two-argument
  `Call`. Declarations 01–09 cover their syntax; semantic rules 01, 03–40 cover
  their reachable behavior. No used construct is fabricated by a catch-all
  rule.
