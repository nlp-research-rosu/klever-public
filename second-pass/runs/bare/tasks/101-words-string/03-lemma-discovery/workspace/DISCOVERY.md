# Trust-boundary discovery

The canonical inventory hash is `086bf69ce233b71b39bec7b995b58e03fdb91b9abb938717d25130a09d35f43a`. Its verification-module closure contains exactly five rules, all from `VERIFICATION` and all classified as `DEFINITION`.

The first four rules are the exhaustive cases defining the recursive mathematical summary `splitSpaces`:

1. the empty-string base case;
2. the leading-space recurrence;
3. the nonempty, no-space terminal case; and
4. the recurrence that emits the word before the first space and processes the suffix.

The fifth rule defines the named summary `wordsContract` by replacing commas with spaces and applying `splitSpaces`. These are equations and recurrences that give meaning to proof-summary functions. They are therefore definitions, not operational execution or observation rules and not extra mathematical facts.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` compiles `semantic.k`, which imports `VERIFICATION` and therefore already contains all five inventory rules, before invoking `kprove` on `spec.k`. The three Stage 1 claims (`words-string-general`, `prompt-example-hi`, and `prompt-example-numbers`) prove program-level reachability properties; none first proves the exact statement of an inventory rule against a module from which that rule is absent. Consequently, no inventory entry meets the required evidence ordering for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventory rule carries the `simplification` attribute, and none asserts an additional mathematical fact beyond defining `splitSpaces` or `wordsContract`.
