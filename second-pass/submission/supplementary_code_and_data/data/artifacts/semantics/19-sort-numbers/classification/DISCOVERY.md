# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory SHA-256
`bbc103c45933fff14c2d2ca4db25fe227558633eacf355687354aabcd8c83563`.
It contains 31 rules, all from `SORT-NUMBERS-VERIFICATION`.

## Classification summary

- `DEFINITION`: 30 rules.
- `OPERATIONAL_RULE`: 1 rule.
- `PROVED_DERIVED_LEMMA`: 0 rules.
- `DOMAIN_LEMMA`: 0 rules.

The four rules for `numberBody`, `sortBody`, `solutionModule`, and `numberKey`
expand macros or name proof terms. The ten `wordVal` equations and ten
`wordCodes` equations define the finite numeral-word representation. The two
`wordsVS` rules and three `encodedWords` rules are structural recurrences. The
final `numericOutput` rule defines the named postcondition summary. These 30
rules are therefore `DEFINITION`.

Rule
`rule-b25203fce8fc32addea6c7671ce933b1a9ee841e26d4b5263e1113d6ed4ffaed`
is the sole `OPERATIONAL_RULE`. It is a problem-local symbolic execution rule:
when the modeled bound `split` method is applied to `str(encodedWords(WORDS))`,
it rewrites the `<k>` cell to list allocation. Its configuration transition,
method-call dispatch shape, allocation effect, and priority make it part of the
verification execution model rather than a context-free mathematical equation.

No inventory rule has the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence in `/reference/k-proof/prove.sh` first compiles
`verification.k` as `SORT-NUMBERS-VERIFICATION` and then runs `kprove spec.k`
against that already-compiled definition. Thus every inventory rule is present
before all Stage 1 claims are proved. There is no earlier proof command against
a module omitting one of these rules, followed by insertion of a rule with the
exact proved statement.

The ten `number-value-*` claims prove executions of the solution's key function,
and `sort-numbers-symbolic` proves the wrapper behavior for an arbitrary
`NumWords` sequence. None of those claim statements exactly corresponds to a
reusable inventory rule proved before that rule is available. Consequently,
none qualifies as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. In particular, the symbolic `split` interception
is classified as an operational modeling rule, not as an additional
mathematical fact, and the other local rules only define representations,
recurrences, macros, or the named expected-output term.
