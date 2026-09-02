# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the exhaustive canonical inventory for
this classification. It contains one rule, with inventory digest:

```text
3eb2050e8c9cec58287e26ab1c6d749f2c97c11af0a4174a42cc5e77f4f8421a
```

The output preserves that one `source_rule_id` exactly once and in inventory
order. No entries were synthesized for source text absent from the canonical
inventory.

## Classification

`rule-af419f60f77e409fe9d74f8499c04f5bc5e7c6463972156d45ed7a152331ad03`
is classified as `PROVED_DERIVED_LEMMA`.

The rule is an executable loop summary: it replaces the exact translated loop,
singleton return-statement sequence, `#endcall`, and frame pop with
`S +Int qualifyingPrefix(VS, N)`. Ordinarily that operational role would call
for `OPERATIONAL_RULE`, but the Stage 1 artifacts satisfy the more specific
`PROVED_DERIVED_LEMMA` requirement:

1. `/reference/k-proof/loop-spec.k` lines 8–61 state
   `LOOP-SPEC.loop-connection`.
2. Apart from the declaration keyword/label and the later rule-priority
   attribute, its complete statement is the same as
   `/reference/k-proof/verification.k` lines 10–64: the K computation, return
   continuation, environment transition, scopes and bindings, scope location,
   heap, heap location, stack frame, return/exception/exit cells, and all three
   guards correspond exactly.
3. `loop-spec.k` requires and imports only `verification-base.k` /
   `VERIFICATION-BASE`. That module does not contain the inventoried rule and
   does not import `VERIFICATION`.
4. `/reference/k-proof/prove.sh` lines 15–23 compile
   `VERIFICATION-BASE` and run:

   ```bash
   kprove loop-spec.k \
     --definition verification-base-kompiled \
     --spec-module LOOP-SPEC
   ```

5. `/reference/k-proof/PROOF.md` records the actual result as `#Top`, exit 0.
6. Only afterward do `prove.sh` lines 25–29 compile `verification.k`, making
   the already-proved statement available as the reusable `priority(30)` rule.

This is the only separately proved derived lemma in the canonical inventory.

## Other classification sets

- `DEFINITION`: empty.
- `OPERATIONAL_RULE`: empty. The only operationally acting rule is placed in
  `PROVED_DERIVED_LEMMA` because its exact statement was proved first in the
  bridge-free definition.
- `DOMAIN_LEMMA`: empty.

The domain-lemma set is explicitly empty.

The canonical rule has only the `priority(30)` attribute and does not carry
`simplification`, so the special simplification-classification restriction is
not triggered.
