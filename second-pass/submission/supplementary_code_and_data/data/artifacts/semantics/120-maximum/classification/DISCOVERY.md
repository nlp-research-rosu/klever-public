# Trust-boundary discovery

The canonical inventory has two rules, both from `MAXIMUM-VERIFICATION`. Each is represented exactly once in `trust-boundary.json`, in canonical inventory order.

## Classifications

1. `rule-8e525ad3c9ded20f8b26e2c2398d95661f926cd77cc2c322f7c541606c0988ad` is `DEFINITION`. It expands the macro term `maximumBody` into the translated statement sequence used as the function closure body in both claims. This is a named syntactic expansion and does not add a mathematical property.

2. `rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907` is `DOMAIN_LEMMA`. It is marked `simplification` and adds the length-preservation fact needed to reason about the supplied opaque `sortVS` summary. That fact is not operational execution behavior and is not separately proved by the Stage 1 artifacts.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 ordering in `prove.sh` compiles `verification.k`—already containing both inventoried rules—into `verification-kompiled`, and only then runs `kprove spec.k` against that definition. The `#Top` recorded in `prove.log` is therefore evidence that the two specification claims close with the length-preservation rule available; it is not evidence of an earlier proof of that exact rule against a module from which the rule was absent. No separate lemma specification, lemma-only proof command, or pre-lemma compiled definition appears in the mounted evidence.

## Domain-lemma set

The domain-lemma set is not empty. It contains exactly `rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907`.

There are no `OPERATIONAL_RULE` entries in the local verification-module inventory.
