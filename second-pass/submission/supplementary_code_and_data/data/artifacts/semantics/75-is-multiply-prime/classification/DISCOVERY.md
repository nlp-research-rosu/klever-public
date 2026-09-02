# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory SHA-256 `ae0fa87d050d008abca2ddb10000b43b81b36a8f7ecb7e96aa6888df89debd66`. It contains three rules, all in the local `VERIFICATION` module. The classifications preserve the inventory order.

| Source rule | Classification | Basis |
|---|---|---|
| `rule-7934c46c05d38f268dac7e0abb5200dc1f3b215ab4c290963f2b490cf3450d03` | `OPERATIONAL_RULE` | `#expect` is a checkpoint observation: a matching result advances execution, while a mismatch remains stuck. It adds no mathematical fact. |
| `rule-d74705ec17c34e17dc69dc82a57d28b0c9698ee9baddb6fa909af098cbe6b504` | `DEFINITION` | It defines the named `#runIsMultiplyPrime` proof term by expanding it to the exact translated module load, call, and cleanup continuation. |
| `rule-d70780b59b96dc074b4d1a73069a3d4a9e1e96dc8bdf16bc23040237b37445e2` | `OPERATIONAL_RULE` | `#forgetEntryPoint` is guarded verification-harness state cleanup that preserves the observed result and removes the temporary module binding. |

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1's `prove.sh` first compiles `verification.k` into `verification-kompiled`, so all three inventory rules are already present. Every subsequent `kprove` command proves a claim from `spec.k` against that same compiled definition. There is no earlier command proving the exact statement of any inventory rule against a module that omits it, followed by admission of that rule.

## Domain lemmas

The domain-lemma set is empty. None of the three rules supplies an additional mathematical fact used to close the proof. The inventory also shows an empty attribute list for every rule, so there are no `simplification`-attributed rules requiring special treatment.

The Stage 1 claims in `spec.k` are proof targets rather than rules in the canonical inventory and therefore are not additional entries in this classification.
