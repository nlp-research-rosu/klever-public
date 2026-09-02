# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256
`8f5de4345417a8095331e88a362aedcf63567db12bd5e59a3e717b2b1f960037`.
It contains three rules, all from the mounted `VERIFICATION` module. Each
canonical `source_rule_id` appears exactly once in `trust-boundary.json` and in
the same order as the inventory.

## Classifications

| Inventory position | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-696c1fa8e2517781ece04e7a5c6625a8196ade913ec6b9596f7c7dafd66ed095` | `DEFINITION` | Base equation defining `countUpperEven` on the empty sequence. It names a mathematical summary and does not match an operational configuration. |
| 1 | `rule-d15a2cae4392a54744c0a40798a805f226e2ebb158b68d3c6b74f95f088ef09d` | `DEFINITION` | Guarded recursive equation defining the same summary on nonempty sequences. Although marked `simplification`, it is a recurrence fixing the named summary rather than an additional domain fact. |
| 2 | `rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4` | `DOMAIN_LEMMA` | Integer-addition reassociation is an extra mathematical normalization used to close the invariant. It is not a definition and Stage 1 provides no earlier proof of the exact rule without the rule present. |

No canonical rule matches Python execution state or observes an operational
configuration, so the `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The mounted Stage 1 `prove.sh` first runs:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

That compilation includes all three canonical rules. Both subsequent `kprove`
commands use that same `verification-kompiled` definition. The focused and full
proofs print `#Top`, but neither command proves any inventory rule against a
module from which that rule was absent. The mutation probes also reuse the same
compiled definition. Consequently, Stage 1 contains no evidence satisfying the
required ordering and exact-correspondence test for a separately proved derived
lemma. In particular, the Stage 1 comment and report description of integer
reassociation as a derived lemma do not change its trust classification.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4`

This is the sole additional mathematical fact trusted by the finalized local
verification-module closure.
