# K proof trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory SHA-256 `1c4a93073f6781879b6ae9c5aff5efce4f9089c321e7b6bacc52db91656d0a28`. It contains three rules, all of which define the mathematical summary used on the right-hand side of the Stage 1 correctness claim.

| Inventory order | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-b067b43d5f947711d358527708712198f2c109323388e41a86efd408cfe7c3aa` | `DEFINITION` | Positive branch of the piecewise `expectedDigit(A, B, D)` definition; it produces `[D]` when `D` is between the unordered endpoints, inclusively. |
| 2 | `rule-098526288db0b9357bcc0dfdb447cbb9838647572e7d85518b225581f438f785` | `DEFINITION` | Complementary branch of the same definition; it produces the empty list when `D` is outside the interval. |
| 3 | `rule-e5fd4b8a680c9837723a78964e7e9f5c5acbab3f9a323002561d8adfacf87cd4` | `DEFINITION` | Macro expansion of `expected(A, B)` into the ordered concatenation of the four possible positive even digits. |

## Derived-lemma evidence

There are no separately proved derived lemmas. Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k` as module `VERIFICATION`, which already contains all three inventoried rules, and then invokes `kprove` on `spec.k`. The only Stage 1 claim is `generate-integers-correct`; `prove.sh` does not first prove the exact statement of any inventoried rule against a module from which that rule is absent. Consequently, none meets the required evidence and ordering for `PROVED_DERIVED_LEMMA`.

## Domain and operational boundary

The `DOMAIN_LEMMA` set is empty. No inventoried rule asserts an additional trusted mathematical fact: the interval branches and four-digit expansion are equations defining the expected-result summary. The canonical inventory also contains no `OPERATIONAL_RULE`; execution rules belong to the Stage 1 semantics and are not entries in this canonical three-rule inventory. None of the inventoried rules carries the `simplification` attribute.
