# Trust-boundary classification

The canonical inventory contains 11 rules, all from `MPY-VERIFICATION`. Every rule is classified exactly once and retained in canonical inventory order in `trust-boundary.json`. The copied inventory SHA-256 is `7110b556e2e2e5f7641769542e6db909889827d1e68749a448bdf5f51d38d241`.

## Definitions

All 11 rules are `DEFINITION` rules:

- The six `runSpec` rules at `verification.k` lines 17–22 are the base equation and character-by-character recurrences of the mathematical scanner summary.
- The four rules at lines 24–27 are structural projection equations for the scanner state's depth, current group, output groups, and last character.
- The `separateSpec` rule at line 28 is the summary's entry equation, supplying initial accumulators and selecting the output component.

These rules define pure verification functions. They do not execute the Python constructor program or rewrite a K configuration, so none is classified as `OPERATIONAL_RULE`. The inventory reports no `simplification` attributes.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries and therefore no separately proved derived lemmas to identify. The Stage 1 evidence does not establish the required proof-before-use ordering: `prove.sh` lines 8–11 compile `verification.k` with all 11 inventory rules already present, and only afterward lines 35–37 run `kprove` on the claims in `spec.k`. The recorded `kprove.out` contains `#Top`, but it does not show any inventory rule first proved against a module from which that exact rule was absent.

## Domain lemmas

The `DOMAIN_LEMMA` set is explicitly empty. No additional mathematical fact is trusted to close this K proof.
