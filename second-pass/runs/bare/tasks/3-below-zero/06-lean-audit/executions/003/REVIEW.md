# Independent Stage 3–5 audit: `3-below-zero`

## Scope and result

The launcher records:

- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

`/candidate` is absent, as required in this mode. Therefore the conditional
Stage 5 copy/build, `#print axioms Proof.final`, proof-identity, and operational
bridge checks do not apply. The Stage 4 generated project was still clean-built
inside the required trusted preflight.

I treated the mounted files and earlier reviews as untrusted evidence. I did
not adopt the prior Stage 2 verdict or Stage 3 labels. The judgment below comes
from a fresh canonical inventory, direct inspection of the frozen source and K
semantics, independent hash/bijection checks, and a rerun of the trusted
preflight.

## Producer provenance gate

This gate passed before I judged Stage 4.

| Producer | Observed SHA-256 | `generator-manifest.json` | Source manifest |
|---|---|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | same | same |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | same | same |

The generator image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in both `generator-manifest.json` and `source-manifest.json`. The
`generation_producer_sources` path recorded by `/audit-input.json` ends in the
same image digest. The producer-bundle tree hash independently recomputes to
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
matching `/audit-input.json`.

Raw evidence: [producer-provenance.txt](evidence/producer-provenance.txt).

## Inventory reconstruction and manifest bijection

I ran `tools.k_rule_inventory.inventory_verification` with
`PYTHONPATH=/reference` on `/reference/k-proof`. `prove.sh` selects
`VERIFICATION`; the local closure inside `verification.k` contains exactly that
module. The frozen `verification.k` hash is
`2bcf4b98c0ab283190e7f18d67ce40c4995229a5b61c9382dcceef818ea945c8`.

The canonical inventory contains exactly two rules, in this order:

| # | Source span | Normalized SHA-256 / source rule ID | Attributes |
|---|---|---|---|
| 1 | `VERIFICATION:11-11` | `fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` / `rule-fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` | none |
| 2 | `VERIFICATION:12-16` | `8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` / `rule-8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` | none |

The reconstructed inventory hash is
`d5def0ac85eed79dfa1a0f725d488b12243abe197cf40deeb8118eb10add9ab3`.
It matches the protected Stage 3 manifest. Ordered identities match
bijectively; both sides are unique; there are no omitted, extra, duplicated,
reordered, unclassified, or unknown-classification entries. Each
`source_rule_id` is exactly `rule-` followed by its recomputed normalized
source hash.

Raw evidence:
[inventory-reconstruction.json](evidence/inventory-reconstruction.json) and
[inventory-bijection.txt](evidence/inventory-bijection.txt).

## Independent classification

I independently classify both rules as `DEFINITION`.

1. The line 11 rule is the base equation for the fresh total function
   `belowZeroFrom(Int, IntList)`: an empty list yields `false`.
2. The lines 12–16 rule is its recursive equation. For head `I`, it tests the
   updated balance `B +Int I`; it yields `true` if that value is negative and
   otherwise recurses on the structurally smaller tail with the updated
   balance.

These equations are disjoint and exhaustive over the two `IntList`
constructors, and recursion strictly descends to the tail. They define a named
summary; they do not assert mathematical facts about existing domain
operations. Accordingly, neither is a `DOMAIN_LEMMA`.

They are not `OPERATIONAL_RULE`s. They mention no configuration cell,
continuation, binding, return action, or state update, and `belowZeroFrom`
appears operationally only in its defining equations and in the final result
of `SPEC.loop-correct`. They do not replace program execution.

They are not `PROVED_DERIVED_LEMMA`s. Stage 3 makes no such claim, and the
rules are definitions rather than rules first proved in a module omitting them
and later imported for another proof.

The classification also matches the frozen operational meaning:

- the loop takes the list head and binds it to `<current>`;
- `AugAssign` updates `<balance>` from `B` to `B +Int I`;
- the comparison then tests that updated value with strict `<Int 0`;
- a true comparison returns `BoolV(true)`;
- if it is false, execution continues on the tail at the updated balance;
- exhausting the list reaches the source program's final `False`.

Thus `belowZeroFrom(B, OPS)` is exactly the recursive running-prefix summary
used by the postcondition. It is relevant to both the source program and the
postcondition. In particular, `[5, -5]` remains false because zero is not
negative, while `[1, -2, 2]` is true because an intermediate prefix is
negative even though the final balance is positive.

As finite corroboration, an independently written direct loop simulation and
the two equations agreed on 136,717 bounded cases. Counterfactual variants
using only the final balance, a nonpositive threshold, or a check before the
addition were each separated by a concrete witness. This testing supports the
source reading; the classification itself follows from the rule form and the
operational step correspondence.

Neither rule has a `simplification` attribute, so the constraint that every
simplification rule be a `DEFINITION` or `DOMAIN_LEMMA` is also satisfied.

Independent true domain-lemma set: empty.

Detailed judgment and raw witnesses:
[classification-judgment.md](evidence/classification-judgment.md) and
[classification-witnesses.txt](evidence/classification-witnesses.txt).

## Hash and immutable-input accounting

Every hash recorded in `/audit-input.json` was recomputed with the matching
trusted hash routine:

| Recorded field | Recomputed value | Result |
|---|---|---|
| `k_workspace_sha256` | `639f7233b9f8918bec0053d213458ef1f8a66a190c4488c1b19e0914a5bd2f91` | match |
| `stage1_export_sha256` | `35f8b4a7665b79e10c58099547dd158321a19689874d8c9c48f1404e6813fa42` | match |
| `discovery_manifest_sha256` | `fabd7fe1b139d97c12d50b5f3c99abdc197b5c295867fe6cec8f84d4eb320fdc` | match |
| `k_audit_sha256` | `f9f7ea334caeb7a209c1548fa0783979f556d6aa211f3eaab9ee5bf78da925b9` | match |
| `klean_generation_sha256` | `e1e4ced1a529bdde4d102a6e55e2114976406702c38112548934d17d3bbe0bf1` | match |
| `generation_producer_sources_sha256` | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` | match |
| `generated_tree_sha256` | `322f088531b9f1e7bddd6b3fa06f63af841d42455cea66d6f0608892a6437245` | match |
| `lean_workspace_sha256` | `null` | match |
| `lean_invocation_sha256` | `null` | match |

All 240 per-file `stage1_source_hashes` also match bijectively: no missing,
extra, or changed files. The input, generator, export-result, recorded
preflight, and audit-input hashes all bind to the same Stage 1 tree, discovery
manifest, generated tree, obligation map, and trust inventory.

Raw evidence: [audit-hash-verification.txt](evidence/audit-hash-verification.txt)
and [stage4-bijection-target.txt](evidence/stage4-bijection-target.txt).

## Required Stage 4 preflight

I reran the exact trusted function:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The audit container initially exposed a procfs PID-namespace mismatch: Lean
uses `/proc/<getpid()>/exe`, but that namespace path did not exist while
`/proc/self/exe` did. I recorded the failed attempt and used a narrowly scoped
`LD_PRELOAD` shim that redirects only numeric `/proc/.../exe` readlinks to
`/proc/self/exe`. It does not inspect or alter K, Lean, manifest, or generated
project content. With that environment repair, the unchanged trusted function
returned:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: `0`
- target: `null`
- generated tree:
  `322f088531b9f1e7bddd6b3fa06f63af841d42455cea66d6f0608892a6437245`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0, output hash
  `882e1a85708a6f08f9f08dd7511cd843635b7a4db64989e72788d0226167b31a`
- designated sorry count: `0`
- trust declarations: `41`, exactly reconciled by the trusted preflight with
  `trust-inventory.json`, with proposition trust rejected by that check

The build completed all generated modules successfully. The preflight's
before/after snapshots and my later tree-hash recomputation confirm that the
mounted inputs remained unchanged.

Raw evidence:
[preflight-first-attempt.txt](evidence/preflight-first-attempt.txt),
[proc-self-workaround.txt](evidence/proc-self-workaround.txt), and
[preflight-rerun.json](evidence/preflight-rerun.json).

## Stage 4 obligation and target identity

The mathematical decision precedes the mechanical one: my independent
classification finds zero `DOMAIN_LEMMA`s.

The deterministic artifacts agree exactly with that result:

- independently classified domain-rule IDs: `[]`
- `input-manifest.json` source rules: `[]`
- `obligation-map.json` source rules: `[]`
- `obligation-map.json` obligations: `[]`
- `obligation-map.json` trust parameters: `[]`
- generator/export/preflight obligation counts: all `0`

The source-rule/obligation map is therefore an exact empty bijection, not an
omission. There are no duplicate, irrelevant, weakened, or vacuous conjuncts.
The deterministic target reconstructed from the obligation map is absent.
`tools.klean_export.target_statement` independently finds no generated target,
and the generator manifest, recorded preflight, and audit input all record
`null`. The generated `Lemmas.lean` namespace contains no proposition or proof
declaration.

Because the true domain set is genuinely empty, `KLEAN_NO_OBLIGATIONS` is the
correct Stage 4 outcome. A Stage 5 project would be invalid in this case, and
none is present.

## Final judgment

Stage 3 is complete and correctly classified; Stage 4 is bound to the frozen
inputs and immutable producer sources; the no-obligation result follows from
the independently empty domain-lemma set; there is no target change or hidden
proof obligation; and Stage 5 is correctly absent in classification-only mode.

VERDICT: PASS
LEGITIMACY: LEGIT
