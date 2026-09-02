# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with
`inventory_sha256`:

```text
197dc991c50e36d5ad237696d7faf9e483d8344bd1affc10da338a7be6a8093d
```

It contains six rules from `VERIFICATION`. Every canonical `source_rule_id`
appears exactly once in `trust-boundary.json`, in canonical inventory order.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 5 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

The two `tailIS` rules are `DEFINITION` entries because they are the exhaustive
constructor equations for a named structural helper. The three
`overlapCount` rules are also `DEFINITION` entries: they are the guarded base
and recursive cases of the mathematical result summary. None of these five
rules is an ordinary execution or observation rule, so the
`OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` compiles `verification.k` with all six inventory rules
already present and then proves `SPEC.loop-inv` and the complete `SPEC` module.
It does not first prove any inventory rule against a module from which that
rule is absent.

The mounted `slice-lemma-spec.k` is not invoked by `prove.sh`. Moreover,
`PROOF.md` records that its bridge-free `kprove` attempt against
`lemma-kompiled` exited 1 with a residual symbolic `buildIS`. The `#Top`
outputs in `loop-proof-output.txt` and `target-proof-output.txt` therefore do
not establish the required prior, rule-free proof ordering: both use the
already-extended `VERIFICATION` definition.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536`

This is the sole rule carrying the `simplification` attribute. It supplies the
slice-to-tail fact used to normalize symbolic `buildIS`. The Stage 1 finite
evidence reports `SLICE_CASES=9840` and `SLICE_MISMATCHES=0`, but finite
testing is not a separate proof of the exact rule. Because no successful
prior proof appears in `prove.sh`, the rule is classified as `DOMAIN_LEMMA`,
not `PROVED_DERIVED_LEMMA`.

## Rule-by-rule result

| Canonical order | Source rule ID | Classification |
|---:|---|---|
| 1 | `rule-993f1ddeb82f8ec3058462bbc0bc6a359326253665e58baa0229c8ff3387f51e` | `DEFINITION` |
| 2 | `rule-76f74f31823745350d94934f77a8b1740fb37bf6ce4be8986b32cd0e40ea55d6` | `DEFINITION` |
| 3 | `rule-7d8832f9476a30d90c0dc5ff351d655f77be7e3f7d280223e5275d3f137e948f` | `DEFINITION` |
| 4 | `rule-29f9efb6fc47c221fe5c4d6a8b72995b4966c7b257bd75c9928ce9d7ccbf0a9b` | `DEFINITION` |
| 5 | `rule-48a4b84d7a4f49eddd82fbf489ed5db68e8505668dbff98cd6bb049cbb651062` | `DEFINITION` |
| 6 | `rule-5c20d5ec621bca8278848104f215af1fb7138a185114c645f09ab29c710fd536` | `DOMAIN_LEMMA` |
