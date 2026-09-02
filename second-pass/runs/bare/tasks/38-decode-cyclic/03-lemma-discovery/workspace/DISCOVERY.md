# Trust-boundary discovery

The canonical verification-module-closure inventory contains three rules. Each carries the `simplification` attribute, so each must be either a `DEFINITION` or a `DOMAIN_LEMMA`. None defines an equation, recurrence, macro expansion, mathematical summary, or named proof term. All three are therefore classified as `DOMAIN_LEMMA`:

- The map rule supplies an injectivity fact: equality of maps updated at the same key implies equality of the updated values.
- The length rule supplies the string-domain fact that every string length is nonnegative.
- The substring rule supplies the identity that slicing from zero through the full length returns the original string.

There are no inventoried `DEFINITION` or `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first compiles `semantic.k` and then invokes `kprove spec.k` with `verification.k` imported. Consequently, all three inventoried simplification rules are already available during the proof. The script contains no earlier proof against a module that omits any of these rules, and there is no evidence establishing exact statement correspondence before later reuse.

The domain-lemma set is **not empty**; it contains all three canonical rules.
