# Static rule-review decisions

The complete, source-line-addressed inventory is `k_rule_inventory.txt`: 942
items comprising 705 rules, 229 syntax declarations, five evaluation contexts,
one configuration, and two claims. Each inventory item carries a decision. This
document explains the grouping behind those per-item decisions.

## Fixed supplied semantics

The candidate's 25-entry `reference-semantics` tree is path/type/content
identical to the trusted mount. The full fixed tree was still reviewed, rather
than treating that equality as permission for proof-local additions.

- `syntax.k` contains constructor declarations and strictness annotations.
  They are well sorted and the used subset is mapped in
  `used_construct_map.md`.
- `core.k`, `operators.k`, `int.k`, `controls.k`, `functions.k`, and `call.k`
  contain every rule on the submitted execution path. Their detailed path,
  evaluation order, bindings, continuation behavior, and state footprint are
  in `used_construct_map.md`. Integer `%` and `//` use `pyMod`; the submitted
  divisors are the nonzero constants 2 and 10. All relevant rule overlaps are
  separated by constructor sorts or guards.
- `assert.k`, `bool.k`, `builtins.k`, `comprehension.k`, `dict.k`, `float.k`,
  `iter.k`, `list.k`, `methods.k`, `range.k`, `set.k`, `sort.k`, `str.k`,
  `subscript.k`, and `tuple.k` do not receive a constructor reachable from this
  program. Their rules were checked for cross-module heads (`applyUn`,
  `applyBin`, `applyCmp`, `#applyK`, and priority rules). Those heads are
  separated from this path by operand/callee constructors and guards; none can
  rewrite the submitted integer operations or `digits` closure call.
- `concrete.k` is imported only by `MPY-KRUN`, not by the proof's `MPY` import.
  Its 16 rules are LLVM-only and were not present as proof extensions.

There are 45 inventoried priority-bearing rules. None is proof-local. On the
submitted path, ref/cell priorities are disabled because all values are
integers and the unannotated function frame lacks `"$cells"`; specialized
math/hashlib/sorted/list/dict calls do not match `Call(Name("digits"), ...)`.

There are 22 `no-evaluators` declarations: md5, sort/key-sort, and float
operations/conversions. No such symbol occurs in `solution.mpy`, either claim,
or the proof-local summaries. They have no dependent claim here. There are no
local `functional` declarations.

No fixed-semantics rule supplied a task-specific answer, intercepted the
`digits` body, fabricated a used operation, or enabled a concrete false
conclusion on a positive-integer input. Consequently there is no unsound-rule
witness to report.

## Proof-local `verification.k`

There are exactly two declarations and ten rules, with no `<k>`-cell rule,
priority, `owise`, `concrete`, or opaque symbol.

1. `oddDigitsProduct(Int) [function,total]`

   - `N <= 0` maps to the empty product 1.
   - For `N > 0`, the guards `pyMod(N,2) == 1` and `== 0` are disjoint and
     exhaustive because Python remainder modulo positive 2 is in `{0,1}`.
   - The recursive argument `(N - pyMod(N,10)) / 10` is the nonnegative decimal
     prefix and is strictly smaller for `N > 0`.
   - The odd case multiplies by the final decimal digit; the even case omits it.

2. `oddDigitSeen(Int) [function,total]`

   - The same disjoint/exhaustive/descending partition applies.
   - It returns 1 immediately for an odd final digit and otherwise searches the
     remaining prefix; the nonpositive base is 0.

For `N = 10q+r` with `0 <= r < 10`, `10q` is even, so `N` and final digit `r`
have the same parity. This connects the summaries' parity guard to the decimal
digit being included. Neither function replaces program execution; the loop
claim proves that fixed execution reaches state values expressed by these
fully defined functions.

The four simplification rules are universal integer equalities:
`1*X=X`, `X*1=X`, `(X+1)-X=1`, and
`(X*Y)*Z=X*(Y*Z)`. Any overlaps have equal normal values. They neither match a
Python AST constructor nor alter a configuration cell.

## Claims

`digits-loop` is a satisfiable auxiliary circularity over the exact real loop.
It maps `n=N` to 0, `product=P` to
`P*oddDigitsProduct(N)`, and Boolean-presence accumulator `F` to
`F + oddDigitSeen(N) - F*oddDigitSeen(N)` under `N>=0` and `F in {0,1}`.
It frames the continuation and unrelated scopes/cells.

`digits-entry` starts from a complete normal module state, loads the exact
constructor term mechanically matched in `program_pinning_check.log`, performs
ordinary lookup/call/frame/body/return execution, and constrains the final
`<k>` value to `oddDigitsProduct(N)*oddDigitSeen(N)` for every `N>0`. Other
specified cells must return to their stated normal values; only the global map
is existentially widened after installing the function binding.

