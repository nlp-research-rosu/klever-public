# Trust-boundary discovery

The canonical inventory SHA-256 is
`da317030086d190a2a4b66952efe2d94d9777d72413dabf6d2fb32bd5d672de7`.
All 26 rules in `/reference/rule-inventory.json` are classified exactly once
and in canonical inventory order in `trust-boundary.json`.

## Classification result

- `DEFINITION`: 22 rules. These introduce or recursively define named proof
  terms and mathematical summaries: projection predicates and total projection
  helpers, string-code projections, the allowed-operator and valid-input
  predicates, `runPairCodes`, and `lastPairValue`. The guarded cast
  orientations and collapse equations are part of the definitions of the
  newly named total projection helpers.
- `OPERATIONAL_RULE`: 0 rules. None of the local rules is an ordinary
  execution rule added to the verification model. The two rules that resemble
  runtime dispatch are marked `simplification`, concern pre-existing semantic
  operators, and are unproved bridge facts, so they are domain lemmas under
  the required classification rules.
- `PROVED_DERIVED_LEMMA`: 0 rules.
- `DOMAIN_LEMMA`: 4 rules. These are the unproved simplification bridges listed
  below.

Every inventory rule carrying `simplification` or `simplification(10)` is
classified as either `DEFINITION` or `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles the complete `verification.k` as module
`VERIFICATION` into `verification-kompiled`. Both positive `kprove` commands
then use that already compiled definition. The claims in `spec.k` are
`SPEC.algebra-loop` and `SPEC.do-algebra`; no command first proves the exact
statement of any inventory rule against a module omitting that rule. The two
negative mutation probes use the same complete compiled definition. Thus the
Stage 1 evidence does not establish the ordering required for
`PROVED_DERIVED_LEMMA`, regardless of comments or prose in `PROOF.md` that call
some helpers “derived lemmas.”

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   — the `#Ceil` characterization of the existing Val-to-Int partial cast.
2. `rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83`
   — the `#Ceil` characterization of the existing Val-to-Str partial cast.
3. `rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d`
   — guarded `applyBuiltin("str", ...)` dispatch for a dynamically sorted
   `Val`.
4. `rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5`
   — guarded string `applyBin("+", ...)` dispatch for a dynamically sorted
   `Val`.

The two `#Ceil` rules state facts about the definedness of existing semantic
partial casts rather than defining new named helpers. The two dispatch rules
state facts about existing semantic operations. All four are simplification
rules present in the verification definition before the target claims are
proved, and Stage 1 contains no prior exact proof of them in a module from
which they are absent. They therefore belong to the trusted mathematical
boundary as `DOMAIN_LEMMA`.
