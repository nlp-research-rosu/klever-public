# Independent Stage 3 classification

Frozen inputs examined directly:

- `/reference/k-proof/verification.k`
- `/reference/k-proof/semantic.k`
- `/reference/k-proof/spec.k`
- `/reference/k-proof/solution.py`
- `/reference/k-proof/solution.mpy`
- `/reference/k-proof/prove.sh`
- `/reference/k-proof/prompt.py`

The reconstructed verification-module closure is only `VERIFICATION`; its
external import `SEMANTIC` is required from `semantic.k`, not a local module in
`verification.k`. The closure contains 13 rules in source order.

| Ordinal | Source rule ID | Span | Independent class | Judgment |
|---:|---|---:|---|---|
| 0 | `rule-e763c3f3ce388151393e428198722a36cf283185f5d31d700c07a4fea32b597b` | 13–14 | `DEFINITION` | Negative branch of `fizzEnd`, a named summary of the final outer-loop index. It does not rewrite a program AST term. |
| 1 | `rule-1904e693aaf0033ea4c764af47f3256dcc77b731523dc22f4cfd10611f765237` | 15–16 | `DEFINITION` | Nonnegative branch of the same summary. The two guards are disjoint and cover all integers. |
| 2 | `rule-30079623688f5b570b38f8a2896ee5b74b79a4367acc2ab3e054817b7e0cb7a7` | 18–19 | `DEFINITION` | Base equation of the `digitSevens` recurrence. Its negative totalization is outside reachable inner-loop inputs but is still a definition, not a domain lemma. |
| 3 | `rule-729ad4a68b3299ff18b3488c12489276a4edfa8a890e236b5bcf981e6e3c6f89` | 20–21 | `DEFINITION` | Positive/last-digit-seven recurrence for `digitSevens`; division by 10 strictly decreases positive integer inputs. |
| 4 | `rule-5d535d5211f655f272b25f28b219933239017014bc24e0eaa6e81b5985089d20` | 22–23 | `DEFINITION` | Complementary positive/last-digit-not-seven recurrence. Together with ordinals 2–3, the guards are disjoint and exhaustive. |
| 5 | `rule-6f6d25b627a7de6753b30c8b1db33b14717b8740662705d84581dd0ddde88d72` | 25–26 | `DEFINITION` | First piece of `fizzContribution`: an integer divisible by 11 contributes its count of digit sevens. |
| 6 | `rule-e81d3927655b90d37b43ae533110b18c623a05009b9e1e9a3e154a6f97ffeb44` | 27–28 | `DEFINITION` | Complementary divisible-by-13 piece after excluding divisibility by 11. |
| 7 | `rule-ebf295199abbea4dc9a90303c80ad6f55809586ff7eeb17f56389907d94e7c15` | 29–30 | `DEFINITION` | Remaining piece contributes zero. Ordinals 5–7 are pairwise disjoint and exhaustive. |
| 8 | `rule-dde8b8487c0ea1e1e4fe6cb86253708342138e3bf3d5d148b5fe526cf90da8fe` | 32–33 | `DEFINITION` | Empty-interval base equation for the named interval summary `fizzFrom`. |
| 9 | `rule-7ba888d5c7f8ca80108339cec76a10640fa99b1108c9249858ebad2a85ebb7ef` | 34–35 | `DEFINITION` | Nonempty-interval recurrence; `I` advances by one toward `N`. |
| 10 | `rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7` | 38 | `DOMAIN_LEMMA` | Integer-addition associativity. It is a globally true algebraic fact over K `Int`, is not a definition, and `prove.sh` compiles it into `verification-kompiled` before proving any claim, so it is not a `PROVED_DERIVED_LEMMA`. It is relevant: both invariants and `fizzFrom` use symbolic accumulated sums, while the source loop updates `count` by addition. |
| 11 | `rule-948f699a84e5f8aba9d6d2c7879d7807ab825a002416eb1275a55c26ada875ab` | 43–48 | `DEFINITION` | Macro expansion of the named `INNER-LOOP` proof term to the exact inner-loop AST in `solution.mpy`. A `[macro]` expansion is compile-time syntax, not a runtime execution bridge. |
| 12 | `rule-55f4df2bb36ada94a0fbce4dfb208de6119596fecc5a3da9f9260be5f4f2b937` | 51–59 | `DEFINITION` | Macro expansion of `OUTER-LOOP` to the exact outer-loop AST, including the exact inner macro. |

## Operational-semantic cross-check

`semantic.k` executes the source AST by ordinary small steps: module loading,
statement sequencing, environment lookup/assignment, left-to-right binary and
comparison evaluation, short-circuit `or`, conditional choice, while unrolling,
and return. None of ordinals 0–10 matches or preempts those operational AST
constructors. Ordinals 11–12 are syntax macros whose right-hand sides match the
translated AST in `solution.mpy`; after expansion, the ordinary semantic rules
execute the bodies.

The summaries agree with the program and postcondition:

- the inner loop divides a nonnegative `x` by 10 and increments `count` exactly
  when the current last digit is 7, matching `digitSevens`;
- the outer conditional admits precisely divisibility by 11 or 13, matching
  `fizzContribution`;
- the outer loop visits exactly `[0,N)` for positive `N`, matching `fizzFrom`,
  and does not run for `N <= 0`;
- `fizzEnd` matches the resulting `i` in both cases.

The only rule carrying `[simplification]` is ordinal 10, independently
classified as `DOMAIN_LEMMA`, satisfying the simplification restriction.
There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries in this
inventory. The protected Stage 3 classifications match this independent
classification entry-for-entry.
