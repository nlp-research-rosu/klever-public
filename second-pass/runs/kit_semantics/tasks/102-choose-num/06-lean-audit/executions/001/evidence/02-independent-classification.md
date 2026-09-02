# Independent classification

The selected local verification-module closure is exactly `VERIFICATION`. The trusted lexical inventory reconstructed four rules, in source order, and no rule has a `simplification` attribute.

| Source lines | Source rule ID suffix | Independent class | Judgment |
|---|---|---|---|
| 10–11 | `05e369…6c789` | `DEFINITION` | Guarded empty-interval equation for the fresh total summary `chooseNumSpec` |
| 13–15 | `18311e…4789` | `DEFINITION` | Guarded even-upper-endpoint equation for the same summary |
| 17–20 | `c36837…c2c9` | `DEFINITION` | Guarded odd-endpoint/predecessor-in-range equation |
| 22–25 | `958329…8f44` | `DEFINITION` | Guarded odd singleton/no-predecessor equation |

Operational reasoning:

- `chooseNumSpec(Int, Int) [function, total]` is fresh proof vocabulary. It is not an MPY AST constructor, K-cell item, continuation, call, lookup, branch, return, or operator-dispatch term.
- The source program executes through the supplied `Call`, `Name`, `If`, `Compare`, `BinOp`, `UnaryOp`, and `Return` rules. No inventory rule matches or preempts any such term or touches any configuration cell.
- The four guards partition `Int × Int`: `X > Y`; otherwise parity is zero or nonzero; in the nonzero branch, `Y-1 >= X` or `Y-1 < X`. Their right-hand sides reproduce the four source branches.
- The supplied `pyMod(I1,I2) => ((I1 %Int I2)+Int I2)%Int I2`, with divisor 2, makes the parity split faithful. For positive endpoints it yields 0 for even `Y` and 1 for odd `Y`.
- The piecewise result is the largest even integer in `[X,Y]`, or `-1`: even `Y` is maximal; odd `Y` has maximal even predecessor `Y-1` if it remains in range; otherwise no candidate exists.
- Boundary/adversarial cases distinguish every branch: `(13,12) -> -1`, `(12,14) -> 14`, `(12,15) -> 14`, `(13,13) -> -1`. Mutating parity, replacing `Y-1`, or weakening either range guard changes at least one of these source outcomes.

There is no `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. In particular, none of these equations independently asserts evenness/maximality; they define a named branch-result summary whose equality to fixed MPY execution is the Stage 1 claim. The independently reconstructed domain set is genuinely empty.
