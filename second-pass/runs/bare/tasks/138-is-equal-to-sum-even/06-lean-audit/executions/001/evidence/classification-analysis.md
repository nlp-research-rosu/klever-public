# Independent Stage 3 classification analysis

The trusted inventory selects the sole local verification module,
`VERIFICATION`, from `verification.k`. Its local closure contains exactly the
three rules below. Imported module `MPY` lives in the separately required
`semantic.k`, so it is operational context rather than another module locally
declared in `verification.k`.

| Source rule | Independent class | Reason |
|---|---|---|
| `rule-df444...` (`verification.k` 10–11) | `DEFINITION` | The left side is the fresh total function `sumFourPositiveEvens(N)`, and the right side defines its Boolean value. It is a named summary, not a rewrite of a pre-existing mathematical fact. |
| `rule-88b901...` (`verification.k` 14–18) | `DEFINITION` | The left side is the fresh total function `canonicalWitnessesAreValid(N)`, and the right side expands the named proof term into positivity, parity, and sum checks for `N-6, 2, 2, 2`. |
| `rule-5eddae...` (`verification.k` 21–22) | `OPERATIONAL_RULE` | This is a cell transition: it consumes the verification command `checkCanonicalWitnesses(N)` from `<k>` and records an observed Boolean value in `<result>`. It defines ordinary execution/observation behavior and states no standalone mathematical implication. |

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 compiles all three rules
into `verification-kompiled` before its single `kprove spec.k` run; it does not
first prove any exact rule against a module lacking that rule and then import
it for a later proof.

There are no rule-level `simplification` attributes. The `[function, total]`
attributes occur on the two syntax declarations, not on the inventory rules.
Thus the special simplification-classification constraint is satisfied.

## Mathematical and operational relevance

The frozen source returns `n >= 8 and n % 2 == 0`. The generated MPY AST in
`solution.mpy` has the same comparison and modulo-by-2 structure. The fixed
semantics loads the function with input `N`, evaluates names and integer
literals, applies K integer remainder with the guard `2 =/=Int 0`, evaluates
the two integer comparisons, and applies Boolean conjunction. Although the
small semantics evaluates both conjunction operands instead of modeling
Python's short-circuit control, the second operand is total and side-effect
free here, so the returned Boolean agrees for every K `Int`.

The first definition is also the exact arithmetic characterization of a sum of
four positive even integers:

- necessity: each positive even integer is at least 2 and the sum of four
  evens is even, hence `N >= 8` and `N % 2 == 0`;
- sufficiency: if those two conditions hold, `N-6, 2, 2, 2` are four positive
  even witnesses summing to `N`.

The second definition names the executable checks for precisely those
witnesses. The third rule makes that verification-only check observable in the
result cell. All three are relevant to either the source-result summary or the
sufficiency postcondition; none is an irrelevant domain fact disguised as
another class.

Counterfactual checks reinforce the distinctions:

- replacing the first right-hand side by a constant or reversing its parity
  test changes the summary and the first specification claim, which is
  definition sensitivity rather than an independent lemma;
- changing `N-6` to `N-4` makes the four witnesses sum to `N+2`, so the named
  proof-term definition no longer supports the sufficiency claim;
- removing or changing the result-cell update in the third rule changes the
  behavior of `checkCanonicalWitnesses`, which is operational sensitivity.

Independent domain set: empty.
