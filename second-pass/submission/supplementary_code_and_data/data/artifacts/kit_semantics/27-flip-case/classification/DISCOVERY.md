# Trust-boundary discovery

## Canonical inventory

The launcher-generated `/reference/rule-inventory.json` is the exhaustive
inventory used for this classification. It records:

- schema version: `2`
- inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- verification file: `verification.k`
- verification module closure: `VERIFICATION`
- canonical rule count: `0`

Because the canonical `rules` array is empty, every canonical rule is
classified exactly once by the empty `rules` array in `trust-boundary.json`.
There are no rules carrying the `simplification` attribute.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The local verification-module closure declares no equations, recurrences, macros, structural helpers, or named proof terms. |
| `OPERATIONAL_RULE` | 0 | The local verification-module closure adds no execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable local rule exists, so none can have a prior rule-free proof with exact statement correspondence. |
| `DOMAIN_LEMMA` | 0 | The finalized proof trusts no additional local mathematical fact. |

The supplied Python reference semantics contains operational and definitional
rules, but those rules are not entries in the canonical local
verification-module inventory and therefore are not added to or classified in
`trust-boundary.json`.

## Stage 1 evidence

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It contains no `rule`, local function, macro, simplification, or auxiliary
claim. The mounted `PROOF.md` independently records the same fact under “Proof-
extension inventory”: the verification module only imports `MPY` and declares
no proof extension.

The mounted `prove.sh` compiles that empty verification layer and proves the
target `SPEC.flip-case` claim. It also runs false-postcondition and
body-mutation probes. It does not first prove the exact statement of any
reusable rule against a rule-free module and then install that rule.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Accordingly, there is no Stage 1
proof command, rule-free proof module, or exact rule correspondence to cite for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty.
