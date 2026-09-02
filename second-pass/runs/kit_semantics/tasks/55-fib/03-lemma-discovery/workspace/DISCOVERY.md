# Trust-boundary discovery

The canonical inventory has three rules, all from the Stage 1 `VERIFICATION`
module. Each canonical `source_rule_id` is classified exactly once and remains
in inventory order in `trust-boundary.json`.

## Definitions

- `rule-0151c94749b8017ab1ca7d238620beed0c8ae98bf6d0591e136a99bf3f95d944`
  is `DEFINITION`. It is the guarded base equation for the mathematical
  `fibFrom` summary when the iteration count is nonpositive.
- `rule-c122a6c58de509694010cd1eeb7f5ecbec714b80ca196cf36fe97c8480fb570a`
  is `DEFINITION`. It is the guarded recursive equation that defines one
  accumulator transition of `fibFrom`.

Together these rules define the proof's named Fibonacci summary. They are
equations over the summary symbol, not Python execution or observation rules.

## Domain lemmas

- `rule-3937e2183350f860b8052e715b9784df8e149714f99e2077f426b8adaae07193`
  is `DOMAIN_LEMMA`. It carries the `simplification` attribute and supplies the
  universal integer identity needed to normalize the value computed by the
  loop assignments. It is an additional mathematical fact rather than a
  defining equation for a named summary.

The domain-lemma set is **not empty**; it contains this one arithmetic
simplification rule.

## Operational rules

The canonical inventory contains no `OPERATIONAL_RULE` entries. Python
execution rules come from the supplied reference semantics and are outside the
launcher-defined local verification-module inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 provides no qualifying separate proof evidence for any inventory rule.
In `prove.sh`, `verification.k` is first compiled as module `VERIFICATION`;
that compilation already includes all three canonical rules. Only afterward
does `prove.sh` invoke `kprove` on `spec.k`. In particular, it never first
proves the exact arithmetic simplification statement against a module that
omits that rule. The Stage 1 `PROOF.md` calls the arithmetic rule a derived
lemma and records that adding it makes the residual close, but that is not the
required rule-free proof ordering and therefore does not justify the
`PROVED_DERIVED_LEMMA` classification.
