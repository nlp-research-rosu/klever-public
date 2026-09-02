# Independent Stage 3 classification judgment

The trusted inventory reconstructed four rules, all in the local
`VERIFICATION` module closure. None has a `simplification` attribute.

| Span | Source rule ID | Independent class | Semantic judgment |
|---|---|---|---|
| 7–9 | `rule-91c176911d796fd34a936d1c236eea93108d5f11251e4aa98880886a8e508d37` | `DEFINITION` | Defines the `NEED <= REMAINING` equation of the named result summary `carrotContract`. It occurs as the destination summary in the first symbolic claim and does not rewrite a `run`, `eval*`, continuation, cell, or other operational term. |
| 10–12 | `rule-af091bc1f7e6cc6c775155a69831df12634c5cff689a359e16ff738e658ec166` | `DEFINITION` | Defines the complementary `REMAINING < NEED` equation of `carrotContract`. It is a summary equation, not an independently asserted arithmetic fact. |
| 14–17 | `rule-93bb107fb1fa39b78b377035f5a623e0f98ed1ccfe394e635a844116bb9a184c` | `DEFINITION` | Expands the named predicate `validInput` into the three range constraints stated in the HumanEval prompt. It is used only as a claim precondition macro. |
| 20–35 | `rule-0cf88ad480aad3ef8af77efd5071f81c8d4d4e3d955e87f4dcad541462652059` | `DEFINITION` | Expands `solutionProgram` to the exact constructor tree represented by `solution.mpy` and by the independently parsed Python AST in `75-source-solution-ast.txt`. After expansion, the frozen `run`, `evalStmts`, `evalStmt`, and `evalExpr` rules still execute the program. It is a named proof term, not a result shortcut or operational bridge. |

## Operational and counterfactual checks

- The two `carrotContract` guards are disjoint and exhaustive over K integers:
  equality takes the first equation, strict reverse order takes the second.
- Boundary witness `(number, need, remaining) = (1, 10, 10)` evaluates the
  first summary equation to `result(11, 0)`.
- Insufficient-stock witness `(2, 11, 5)` evaluates the second summary
  equation to `result(7, 0)`.
- Strict-sufficient witness `(5, 6, 10)` evaluates the first equation to
  `result(11, 4)`.
- Replacing the source comparison `need <= remaining` with `<`, changing either
  arithmetic operation, or replacing the final zero would make the
  `solutionProgram` constructor tree disagree with the independently parsed
  source AST and with at least one of those boundary witnesses.
- `validInput` is body-independent domain notation: at `(0,0,0)` it is true,
  while changing any component to `-1` or `1001` makes the corresponding
  conjunct false.

There is no rule that Stage 1 first proves in a module excluding that rule and
then imports for a later proof, so the `PROVED_DERIVED_LEMMA` set is empty.
There is no remaining mathematical proposition used to close the source
program's postcondition, so the `DOMAIN_LEMMA` set is genuinely empty.
