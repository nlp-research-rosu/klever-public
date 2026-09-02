# Trust-boundary discovery

## Canonical inventory

This classification uses `/reference/rule-inventory.json` as the exhaustive
inventory. Its copied inventory digest is
`0ebb6d2902488cbd08d9a03c06d8a8d5707b37278af455cb56c373e3c0899f2b`.
The inventory contains five rules, and `trust-boundary.json` preserves their
canonical order and includes every `source_rule_id` exactly once.

Classification totals:

| Classification | Count |
|---|---:|
| `DEFINITION` | 4 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

## Definitions

- `rule-3af6834c5d265aaa932ee4a8d6e9c27217a407ae8d47026f5f3bded39d1d39bc`
  is the macro equation for `fileNameCheckBody`. It expands a named proof term
  into the translated statement tree and disappears before runtime execution.
- `rule-090cffa7fcdc5ffc47356048225b8e0752c4c5eb3eee496ad6a1f6c758c90243`
  is the exhaustive equation for `decimalDigitCount`. It names the sum of the
  fixed `cntSub` computations used to partition the digit-count cases.
- `rule-bbf7cf0b4fb369fbc48c61958bcbe40df6c243afe391fe598d557324862e89c4`
  defines `fileExtensionIs` using the fixed slice and comparison terms.
- `rule-359a1379ae7cf0fd25d119b9d40416cdee51f7a8b2a512b81c012bdf386f8523`
  defines `allowedFileExtension` by composing the three extension summaries.

These rules name syntax or mathematical summaries. None is an ordinary
execution/observation rule, and none adds a free-standing mathematical fact.

## Operational rules

The canonical local verification-module inventory contains no
`OPERATIONAL_RULE` entries. Program lookup, calls, slicing, comparison,
short-circuiting, returns, and state transitions remain in the supplied `MPY`
semantics rather than in these five local rules.

## Separately proved derived-lemma evidence

The only canonical rule for which Stage 1 supplies a separate derived-lemma
proof is
`rule-62d1bbd5b25d2b70152e85917d8c17ce8f2ed86c82cce542d4527216437bc22c`
at `verification.k` lines 128–130.

The mounted evidence establishes the required ordering and correspondence:

1. `lemma-spec.k` lines 6–20 state the same guarded K simplification fact
   inside an otherwise unchanged MPY configuration.
2. `prove.sh` lines 68–71 compile only
   `reference-semantics/semantics.k`, with main module `MPY`, into
   `audit-kompiled`. That definition does not import `VERIFICATION`, and its
   recorded main module is `MPY`.
3. `prove.sh` lines 72–74 run `kprove` on `lemma-spec.k` against that
   rule-free audit definition.
4. The target proof is run later, at `prove.sh` lines 76–78.
5. `PROOF.md` records the independent audit result as `#Top` with exit 0.

Thus Stage 1 separately proves the exact mathematical fact before using the
local rule. Nevertheless, the canonical rule itself carries the
`simplification` attribute. The benchmark requires every such rule to be
classified only as `DEFINITION` or `DOMAIN_LEMMA`; because this rule is an
additional mathematical fact rather than a definition, its classification is
`DOMAIN_LEMMA`, not `PROVED_DERIVED_LEMMA`.

No other canonical rule has separate Stage 1 derived-lemma evidence, and no
rule is classified `PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-62d1bbd5b25d2b70152e85917d8c17ce8f2ed86c82cce542d4527216437bc22c`.

Its inclusion follows from its role as an additional guarded arithmetic fact
and from the mandatory classification rule for canonical entries carrying the
`simplification` attribute.
