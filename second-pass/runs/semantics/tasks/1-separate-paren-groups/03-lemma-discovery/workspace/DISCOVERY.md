# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory SHA-256 `a63ea6ae5214bc83213ff7696c9cb7bc80ce9cf4144781e6a22ab175be497a0f`. It lists 13 rules, all in the local `VERIFICATION` module. `trust-boundary.json` preserves their canonical order and classifies each exactly once.

## Classification result

All 13 inventory rules are `DEFINITION`:

- The first six rules define the declarative output fold `scanGroups` and its close-case helper `scanClose` by base, recursive, conditional, and `owise` equations.
- The next four rules define the contract predicate `balancedTail` by structural recursion over the input code sequence and tracked depth.
- The next two rules define the accepted input alphabet predicate `parenSpaceOnly`.
- The final rule is the macro expansion of the named proof term `solutionClosure` into the exact translated function closure.

These rules are equations, recurrences, structural dispatch, or macro expansion. None is an ordinary execution/observation rule added to the verification model, so the `OPERATIONAL_RULE` set is empty. None states an additional mathematical fact beyond those definitions, so the `DOMAIN_LEMMA` set is explicitly empty. The inventory contains no rule with the `simplification` attribute; the one attributed rule is the definitional `owise` dispatch for `scanGroups`.

## Separately proved derived lemma

Stage 1 separately proves exactly one reusable derived result: the `SPEC.all-balanced-inputs` reachability claim in `/reference/k-proof/spec.k`. It is a claim, not one of the 13 canonical `source_rule_id` entries, so no inventory rule is classified as `PROVED_DERIVED_LEMMA`.

The Stage 1 evidence establishes the required ordering and exact reuse:

1. `/reference/k-proof/prove.sh` first compiles `verification.k` as the `VERIFICATION` proof definition. That module contains the 13 inventoried definitions and does not contain `SPEC.all-balanced-inputs` as a rule.
2. Its first `kprove` command selects the exact label with `--claims SPEC.all-balanced-inputs`. The immediately following check requires `/reference/k-proof/proof-invariant.out` to be exactly `#Top`; the mounted output is exactly `#Top`.
3. Only after that successful check does the second `kprove` command pass the same exact label, `SPEC.all-balanced-inputs`, via `--trusted` while proving the public-entry and concrete claims. `/reference/k-proof/proof-entry-and-examples.out` is also exactly `#Top`.

Thus the loop invariant is separately proved before modular reuse, but it is not silently reclassified onto any different canonical rule. There are no other separately proved-and-reused derived lemmas in the mounted Stage 1 evidence.
