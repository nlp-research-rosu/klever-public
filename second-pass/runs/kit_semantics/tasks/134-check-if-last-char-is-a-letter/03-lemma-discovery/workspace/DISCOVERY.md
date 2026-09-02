# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`d817da6122acbe7a8e69a2d9030e69eb871ccebe2fc9cf22295da968e449544a`.
It contains six rules in the local `VERIFICATION` closure. Every rule is
classified exactly once and retained in canonical inventory order in
`trust-boundary.json`.

## Classification summary

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-9f3646175b8c8b5cb64ba75a517ccb682e19312b8c145a72deccf1c5a90bad2a` | `DEFINITION` | Empty-sequence equation for the named result summary. |
| 2 | `rule-4df32a98b335031084e1e2d44c77c3aee9afd5f217f99ad1251e817e7d17ce01` | `DEFINITION` | Positive-length/nonalphabetic equation for the result summary. |
| 3 | `rule-4e7aa14452104b02dfb2ee9c7d2e2129c943e23411864d4a7c094fc06634aada` | `DEFINITION` | One-character/alphabetic equation for the result summary. |
| 4 | `rule-cde37f71888ce75952bb23d314c3a846093f8ef594206ebe110b61ae7652000a` | `DEFINITION` | Longer/alphabetic equation defining the result from the penultimate code. |
| 5 | `rule-e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4` | `DOMAIN_LEMMA` | Trusted constructor-disjointness simplification. |
| 6 | `rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030` | `DOMAIN_LEMMA` | Trusted singleton-constructor injectivity simplification. |

The first four rules are guarded equations for the
`standaloneLastLetter(IntSeq)` function. They define the named mathematical
summary by an exhaustive case split and do not match operational
configurations, so they are `DEFINITION`s.

The last two rules carry the `simplification` attribute. They state additional
mathematical facts about the `IntSeq` constructors and K equality rather than
defining a named term. Under the required classification policy, they are
`DOMAIN_LEMMA`s.

There are no `OPERATIONAL_RULE` entries: none of the six canonical rules is an
ordinary execution or observation rule over the verification configuration.

## Separately proved derived lemmas

There are no separately proved derived lemmas, so the
`PROVED_DERIVED_LEMMA` set is empty.

The Stage 1 evidence establishes this by ordering:

1. `/reference/k-proof/prove.sh` first compiles `verification.k` as module
   `VERIFICATION`.
2. That compiled definition already contains both simplification rules.
3. Every subsequent `kprove` command uses that definition. The positive target,
   model-boundary, false-result mutation, and body-mutation specs all require
   or import `VERIFICATION`.
4. Stage 1 contains no separate module omitting either simplification rule and
   no earlier claim proving either exact rule statement before it is installed.

Consequently, the target proof's `#Top`, mutation failures, comments describing
the rules as derived, and informal constructor reasoning do not constitute the
required independent proof evidence. Neither simplification qualifies as
`PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly these two rules:

- `rule-e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4`;
- `rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030`.

These two constructor facts are therefore the proof-local mathematical trust
boundary exposed by the canonical verification-rule inventory.
