# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, with:

- schema version: `2`
- inventory SHA-256:
  `8ec67278b8911dae25f163d88afd1b55cccd504bb96573d1b111cdc4193d5663`
- canonical rule count: `27`

`trust-boundary.json` preserves all 27 canonical `source_rule_id` values in
inventory order and classifies each exactly once.

## Classification result

| Classification | Count | Reason |
|---|---:|---|
| `DEFINITION` | 19 | These are the case equations and structural recurrences defining `collatzNext`, `validCollatzTrace`, `traceFirstInt`, `traceLastInt`, `maybeOdd`, and `oddWithoutLast`. |
| `OPERATIONAL_RULE` | 0 | The canonical verification-module closure contains no rule over execution cells or an observation step of the operational model; all inventoried rules are pure summary equations or mathematical simplifications. |
| `PROVED_DERIVED_LEMMA` | 0 | Stage 1 contains no proof that first establishes any inventoried reusable rule against a module from which that exact rule is absent. |
| `DOMAIN_LEMMA` | 8 | Every `[simplification]` rule is an additional concatenation or append-observer fact loaded into the target proof theory without a qualifying separate proof. |

The first 19 inventory entries are definitions. Their rules form the guarded
cases or structurally descending recurrences for named proof summaries. They
do not assert a reusable theorem about a separately defined operation.

## Separately proved derived lemmas

There are **no separately proved derived lemmas**.

The Stage 1 evidence is decisive about ordering:

1. `/reference/k-proof/prove.sh` compiles
   `/reference/k-proof/verification.k` into `verification-kompiled`.
2. That file already contains all eight `[simplification]` rules.
3. Only after that compilation does `prove.sh` invoke `kprove` on `spec.k`.
4. There is no alternate verification module with one of those rules removed,
   no lemma-only spec establishing an exact inventoried statement, and no
   earlier `kprove` command whose successful result is imported before the
   target theory is built.

The comments in `verification.k` and prose in `PROOF.md` describe the
simplification rules as derived by structural induction, but neither is
machine-checked Stage 1 evidence satisfying the required proof-before-use
ordering. The positive target proofs and negative mutation probes all use the
already compiled theory containing the rules. Therefore no inventory entry is
classified `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these eight
canonical entries:

1. `rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa`
   — right identity of `valSeqConcat`.
2. `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97`
   — associativity of `valSeqConcat`.
3. `rule-bf51f8af576c3c723ddfe912c4608940069bce29b6be31b545366c25e65e8e30`
   — concatenation with a nonempty right operand is not empty.
4. `rule-57fc2eb6b8603c24117bc3c8656ecab475bdba5d09587b0d5fd0085351fcdb37`
   — the symmetric form of that nonemptiness fact.
5. `rule-89c097c36f3bdd496566e3c2f532dd496a1097a579d8ee9ce25c05754246d84e`
   — `traceFirstInt` after one-element append.
6. `rule-f6103b1ac225a169c76b912d0d9466de492ff6054396a5013d6ad69ec17b572b`
   — `traceLastInt` after one-element append.
7. `rule-18e026acecdd8464802b183af3b97dd206214188168f0fffab44f0e7bfeb0632`
   — `validCollatzTrace` after one-element append.
8. `rule-8b95aa8c6594806c101acbceeda1f787a0a21325465f798e55bc687f6f521caa`
   — `oddWithoutLast` after appending to a valid trace.

These rules may be mathematically derivable from the structural definitions
and the supplied sequence semantics, but the requested classification is about
the mounted Stage 1 proof evidence. In that evidence they are trusted
mathematical facts used to close the K proof, so they are `DOMAIN_LEMMA`.
