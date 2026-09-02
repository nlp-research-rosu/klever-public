# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`.

- Schema version: `2`
- Inventory SHA-256:
  `e7581c4cdd2c4847747f0d1386bc17857b25c08874b12a090a6be0c32116955b`
- Verification-module closure: `VERIFICATION`
- Canonical rule count: `12`

`trust-boundary.json` preserves all 12 canonical `source_rule_id` values
exactly once and in inventory order.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

The macro expansions and the equations for `allInts`, `scanDrops`,
`lastAfter`, and `moveSpec` define named syntax or mathematical summaries.
They are therefore `DEFINITION`.

There are no local ordinary execution or observation rules in the canonical
verification-module closure, so the `OPERATIONAL_RULE` set is empty.

## Rule-by-rule classification

| Inventory order | Source rule ID | Classification | Basis |
|---:|---|---|---|
| 1 | `rule-2113f0fdc2009228980618182d1e8b1e9cbb2b4e997089fa8e3b9265644d811b` | `DEFINITION` | `scanBody` macro expansion defining the loop-body AST. |
| 2 | `rule-a954c7fce79d3cc622c51dd0a87db8553231b26de3aaa807968ebbf55e3e4381` | `DEFINITION` | `moveOneBallBody` macro expansion defining the function-body AST. |
| 3 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty base equation for `allInts`. |
| 4 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | Constructor recurrence for `allInts`. |
| 5 | `rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d` | `DOMAIN_LEMMA` | Guarded `applyCmp` simplification added as a mathematical fact, without a prior exact proof. |
| 6 | `rule-4e59619ad0d5e4c817fce319f536d37391f7c43783f89757495c9ed16530e409` | `DEFINITION` | Empty base equation for `scanDrops`. |
| 7 | `rule-bd22b95ff27fa507ace8a55b23e07960d0ba7af1765c6c5a6c75faeb33a2aeee` | `DEFINITION` | Recursive accumulator equation for `scanDrops`. |
| 8 | `rule-2fcb91a07fe018ada596c62b5c013251f64fc0c3817612c4f480cbc51f49374f` | `DEFINITION` | Empty base equation for `lastAfter`. |
| 9 | `rule-f7986d4c0e6a22445baeea69ebcde91b805f9c0d364d6d60d917b74a2ab2005f` | `DEFINITION` | Constructor recurrence for `lastAfter`. |
| 10 | `rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1` | `DOMAIN_LEMMA` | Guarded simplification for comparison with `lastAfter`, used without a prior exact proof. |
| 11 | `rule-5c07cca7fdc014be55b52c0e209519d4b57df23c2b7d0323cd179fcd59f76d32` | `DEFINITION` | Empty-domain equation for `moveSpec`. |
| 12 | `rule-5277cf06d6a112559474beb63e50a1eced34870a71610af9bc1b31a081414e17` | `DEFINITION` | Nonempty all-integer equation for `moveSpec`. |

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 evidence does not demonstrate the required proof ordering for either
simplification rule:

1. `/reference/k-proof/prove.sh` compiles `verification.k` into
   `verification-kompiled` with both simplification rules already present.
2. Its first positive proof command proves `SPEC.scan-loop` using that compiled
   definition.
3. Its second positive proof command proves the full `SPEC`, again using the
   same definition.
4. `/reference/k-proof/kprove-loop.out` and
   `/reference/k-proof/kprove-all.out` each contain `#Top`, but neither is an
   exact claim proving one simplification rule in a module that excludes that
   rule.
5. The mutation probes and differential tests are validation evidence, not
   prior machine proofs of either exact rule.

Comments in `verification.k` and the “Derived lemmas” label in the Stage 1
`PROOF.md` do not satisfy the required rule-free proof ordering.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d`
- `rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1`

Both carry the `simplification` attribute, add facts about an existing
comparison operation, and were present in the theory used to obtain the Stage
1 `#Top` results. Because Stage 1 supplies no earlier exact proof with the
respective rule absent, both remain trusted domain lemmas.
