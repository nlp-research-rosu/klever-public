# Trust-boundary discovery

## Canonical scope

The sole classification source is
`/reference/rule-inventory.json`, whose recorded inventory SHA-256 is
`3c1cfab2818be9154689f36432c8453a37abe25c1ae0c194f49ab53a863ede11`.
It contains 15 rules from the local `VERIFICATION` module closure.
`trust-boundary.json` preserves their inventory order and classifies every
canonical `source_rule_id` exactly once.

The mounted Stage 1 files were inspected read-only. No Stage 1 artifact was
edited or copied.

## Classification method

Twelve rules are `DEFINITION`:

- `madBody` is a macro equation expanding a fresh proof term into the exact
  statement tree.
- The two `allFloatVS` rules define a recursive domain predicate.
- The guarded orientations and Float collapse for the fresh `projectFloat`
  symbol define that named projection term. The reverse orientation is part of
  the same definitional normalization scheme; it does not state an independent
  source-language property.
- The base and recursive equations for `sumFloatVS` and
  `deviationFloatVS` define mathematical fold summaries.
- The two complementary guarded `madResult` equations define the empty and
  nonempty result-summary branches.

No inventory rule is classified `OPERATIONAL_RULE`. The canonical inventory is
limited to the local verification modules: `madBody` is a macro definition,
the fold and result rules are mathematical definitions, and the remaining
simplification rules are definitions or additional domain facts. The ordinary
Python execution rules live in the supplied reference semantics and are not
members of this canonical inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` in full:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It then proves `spec.k` against that already-compiled definition:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The recorded `kprove-positive.out` contains `#Top`, but that proves the
reachability claims under all 15 local rules. It does not prove any reusable
rule's exact statement before admitting that rule. The two expected-failure
mutation commands likewise use the same compiled definition and do not prove a
canonical rule. Consequently, no Stage 1 evidence demonstrates the ordering
required for `PROVED_DERIVED_LEMMA`.

This conclusion intentionally overrides informal wording in `PROOF.md` that
calls some projection and dispatch rules “derived lemmas”: comments and audit
labels are not proof-order evidence under the requested taxonomy.

## Domain lemmas

The domain-lemma set is not empty. It contains exactly three rules:

1. `rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e`
   characterizes the definedness of the pre-existing partial `Val`-to-`Float`
   cast using `isFloat`.
2. `rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7`
   extends the pre-existing `applyBin("+", ...)` function from a statically
   typed Float operand to a guarded dynamic `Val` operand via `projectFloat`.
3. `rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f`
   supplies the analogous guarded dynamic dispatch equality for subtraction.

All three carry a `simplification` attribute and are classified
`DOMAIN_LEMMA`, as required. They are additional facts about existing cast or
operator symbols, not equations defining a fresh mathematical summary. Stage 1
uses them while proving the loop and target claims but contains no prior
rule-free proof of their exact statements.

The remaining simplification-bearing rules are the guarded defining
orientations and identity equation for the fresh `projectFloat` symbol, so they
are `DEFINITION`, not trusted domain facts.

## Counts

| Classification | Count |
|---|---:|
| `DEFINITION` | 12 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 3 |
| Total | 15 |
