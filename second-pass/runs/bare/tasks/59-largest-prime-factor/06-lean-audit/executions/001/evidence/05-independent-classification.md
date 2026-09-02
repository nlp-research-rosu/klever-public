# Independent Stage 3 classification

The trusted inventory reconstructed only the local `VERIFICATION` module from
`verification.k`. `SEMANTIC` is imported from `semantic.k` and is therefore not
a module local to `verification.k`; its ordinary language-execution rules are
not Stage 3 proof-extension inventory entries.

| Position | Source span | Short rule identity | Independent class | Judgment |
|---:|---:|---|---|---|
| 1 | 10–11 | `rule-b489…104e` | `DEFINITION` | Base equation for the named function `lpfSpec`: when `F*F > N`, its value is defined as `N`. It does not rewrite a program configuration or state a proposition. |
| 2 | 12–13 | `rule-9f46…da54` | `DEFINITION` | Divisible recurrence equation for `lpfSpec`, reducing `(N,F)` to `(N/F,F)` under the loop's divisible branch guard. |
| 3 | 14–15 | `rule-6bcf…04b` | `DEFINITION` | Nondivisible recurrence equation for `lpfSpec`, reducing `(N,F)` to `(N,F+1)` under the complementary loop branch guard. |
| 4 | 20–27 | `rule-7148…a2d7` | `DEFINITION` | Macro equation naming the exact `While`/`If` AST fragment used by the translated source loop. Macro expansion precedes operational execution; this is a named proof term, not an execution shortcut. |
| 5 | 30–35 | `rule-1cd2…b63f` | `DEFINITION` | Macro equation naming the complete translated function AST. Its assignment, loop term, and return match `solution.py` and `solution.mpy`. |

Operational-semantic cross-check:

- `semantic.k` executes `Module`, statement lists, assignment, `If`, `While`,
  and `Return` through `<k>`, `<env>`, and `<result>` rules.
- Neither `lpfSpec` nor either macro rule accepts or rewrites those operational
  cells. The `lpfSpec` equations define a pure recurrence used in the
  postcondition/loop summary. The two macro rules only expand names into AST
  constructors that the fixed operational rules then execute.
- The three recurrence guards mirror the source loop: terminate on
  `F*F > N`; while `F*F <= N`, divide by `F` when the remainder is zero and
  increment `F` otherwise.
- The source comment that the recurrence returns the greatest prime factor is
  not itself a K rule or theorem. No inventory entry asserts that number-theory
  proposition.

There are no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`
entries. No rule has a `simplification` attribute. The independently determined
domain-lemma set is therefore genuinely empty.
