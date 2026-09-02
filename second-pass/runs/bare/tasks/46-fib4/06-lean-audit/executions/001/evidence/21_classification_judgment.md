# Independent Stage 3 classification judgment

Frozen inputs inspected:

- `solution.py` and its frozen `solution.mpy` constructor tree;
- `semantic.k`, especially operational rules at lines 76–117;
- `verification.k`, especially the seven-rule closure at lines 9–23; and
- `spec.k`, which uses the two named mathematical functions in the loop
  invariant and result claims.

The local verification-module closure is exactly `VERIFICATION`. It contains
seven rules and imports no local module containing additional rules.

| Rule (source span) | Independent class | Operational and mathematical judgment |
|---|---|---|
| `rule-5cc3…ae38b` (9–10) | `DEFINITION` | This is the terminating equation of the newly declared `advanceTo` summary. When `I > N`, the operational while-exit rule (`semantic.k` 99–102) schedules `Return(d)`, and the return rule (104–106) observes `D`. The rule neither matches nor replaces a program configuration. |
| `rule-93cd…61a7` (11–13) | `DEFINITION` | This is the recursive equation of `advanceTo`. The operational loop body computes the old-window sum into `e`, then sequentially updates `(a,b,c,d,i)` to `(B,C,D,A+B+C+D,I+1)`, exactly the recursive arguments. It names the loop summary; it is not an independently asserted algebraic fact. |
| `rule-b6e0…e628` (18) | `DEFINITION` | Defining base branch `fib4Spec(0)=0`, matching the first early return in the source and `solutionProgram`. |
| `rule-aefe…261a7` (19) | `DEFINITION` | Defining base branch `fib4Spec(1)=0`, matching the second early return. |
| `rule-b63d…ac46` (20) | `DEFINITION` | Defining base branch `fib4Spec(2)=2`, matching the third early return. |
| `rule-ae0f…e92c` (21) | `DEFINITION` | Defining base branch `fib4Spec(3)=0`, matching the fourth early return. |
| `rule-c546…a242` (22–23) | `DEFINITION` | Defining branch for `N ≥ 4`. The source initializes `(a,b,c,d,i)` to `(0,0,2,0,4)` before entering the loop, exactly the initial arguments of `advanceTo`. |

Classification exclusions:

- No rule is an `OPERATIONAL_RULE`: none matches an AST term, `<k>` cell, map,
  result cell, or another operational configuration.
- No rule is a `PROVED_DERIVED_LEMMA`: the frozen workspace contains no earlier
  proof of the exact rule against a module omitting it, followed by later use.
- No rule is a `DOMAIN_LEMMA`: all seven are branch equations for symbols
  declared immediately above them and used as named proof summaries.
- None has a `simplification` attribute.

Guard and sensitivity checks:

- `advanceTo` guards `I > N` and `I ≤ N` are disjoint and exhaustive over
  mathematical integers. The recursive branch increments `I`, and each step
  matches one operational loop iteration.
- The `fib4Spec` branches are pairwise disjoint on their covered domain:
  exact inputs 0, 1, 2, 3 and `N ≥ 4`.
- Boundary witnesses are:
  `advanceTo(1,2,3,4,6,5)=4`,
  `advanceTo(1,2,3,4,5,5)=10`,
  `fib4Spec(4)=2`, `fib4Spec(5)=4`, and `fib4Spec(7)=14`.
  A constant/identity summary would fail the second witness, and a changed
  state shift or old-window sum would fail at `N=5` or later.

The `[total]` declaration on `fib4Spec` has no defining branch for negative
integers, but no frozen claim uses `fib4Spec` there: the claims are the four
exact base cases and the `N ≥ 4` branch. This coverage limitation does not turn
any defining equation into a domain lemma and does not create a Stage 4
obligation.

Independent true `DOMAIN_LEMMA` set: empty.
