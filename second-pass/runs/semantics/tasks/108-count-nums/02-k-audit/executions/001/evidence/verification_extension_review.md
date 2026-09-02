# Proof-local extension audit

This review indexes `verification.k` against the exhaustive declaration list in
`rule_inventory.md`.

## Definitional symbols and equations (`verification.k:7-71`)

- `digitQuot` and its equation implement Python floor division by positive
  divisor 10 through the supplied `pyMod`. On the nonnegative domains used by
  the loops, it is `floor(N/10)`, strictly decreases for `N > 0`, and is total.
- `positiveFold` (two disjoint guards), `positiveDigitSum`, `leadingDigit`
  (two disjoint guards), `negativeTotal` (two disjoint guards), and
  `negativeDigitSum` are terminating base-10 folds. Their recursive guards
  cover all integers; all value-bearing uses of `leadingDigit`,
  `negativeTotal`, and `negativeDigitSum` are on nonnegative magnitudes.
- `signedDigitSum` has disjoint, exhaustive `< 0` and `>= 0` equations and
  chooses the correct magnitude fold.
- `intValue` is exact on `Int`; its `owise` value 0 is used only under `isInt`.
- `positiveBit` has disjoint, exhaustive guards.
- `countFold` is structurally recursive and exact for `.ValSeq` and an
  integer-headed `vCons`. Its `[total]` declaration is broader than its
  equations for non-integer heads, but every proof use is guarded by
  `allInts`/`isInt`, so it does not supply an incorrect value on the theorem
  domain.
- `countPositive`, `allInts`, and `lastOr` are structurally recursive and their
  equations are exhaustive on their used domains.

There are no proof-local opaque symbols, `symbol(...)/no-evaluators` terms, or
`simplification` rules.

## Exact-syntax macros (`verification.k:74-137`)

The twelve macro symbols and their twelve macro-expansion rules reproduce the
three loop bodies, four function bodies, four closure values, and the helper
binding map used by the hand-written claims. Their expansions textually agree
with the submitted AST constructors. They are not linked to, parsed from, or
loaded from `solution.mpy`, which is a separate real-program pinning failure.

## Operational bridges (`verification.k:145-243`)

1. Lines 145-157, positive loop: the preceding positive-loop claim proves the
   same loop-head pattern, local map update, guard, arbitrary K continuation,
   and framed cells. Its fold equations match `% 10`, `// 10`, and termination
   at `n == 0`.
2. Lines 159-171, negative loop: likewise matches its preceding claim and
   preserves the leading digit plus accumulated trailing digits.
3. Lines 177-180, positive function: the connection claim fixed `env=0`,
   exact scopes, empty heap/stack, `ret=noRet`, and a terminating K cell. The
   rule keeps only `N >= 0` and accepts any continuation and all other cells.
   This is materially false over its match domain. With `N=12` and
   `<ret>retV(99)</ret>`, the bridge proves result 3; fixed execution gets stuck
   at `Return(3)` because the supplied Return rule requires `noRet`.
4. Lines 182-185, negative function: identical cell/continuation broadening.
   The symbolic false witness is `N=12`, `<ret>retV(99)</ret>`: the bridge
   yields 1 while fixed execution gets stuck at `Return(1)`.
5. Lines 191-194, signed function: the connection claim fixed the correct
   helper bindings and all other cells; the rule omits them all. With integer
   `12` and an empty module scope, the bridge proves result 3. Fixed execution
   gets stuck at `#look("positive_digit_sum",-1)`. Both halves are
   machine-checked in `bridge_enabled_witness.log` and
   `bridge_fixed_comparison.log`.
6. Lines 200-214, count loop with an existing `n`: the claim required
   `L =/= 0` and the exact helper bindings in scope 0. The rule drops both
   conditions and all other cells. No bridge-free theorem covers the rule's
   complete match domain.
7. Lines 220-228, empty count loop: the bridge is extensionally consistent
   with the fixed iterator rules because empty iteration performs no binding or
   helper call, although its cited claim was narrower (`L =/= 0` and helper
   scope present).
8. Lines 230-243, nonempty count loop: again drops `L =/= 0`, scope-0 helper
   bindings, and every other cell from the connection claim. It therefore
   lacks complete-domain justification and inherits the signed-call
   unsoundness.

Every bridge has priority 40 and therefore can preempt fixed execution. The
false witnesses are over integer inputs in the stated input type, not
non-integer out-of-domain values.
