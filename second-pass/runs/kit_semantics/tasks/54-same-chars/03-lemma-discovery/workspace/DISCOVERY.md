# Trust-boundary discovery

## Canonical inventory

`/reference/rule-inventory.json` is the exhaustive inventory for the local
verification-module closure. It identifies `VERIFICATION` as the sole local
verification module and contains zero rule entries:

```text
inventory_sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
rules: 0
```

Accordingly, `trust-boundary.json` has an empty `rules` array. This classifies
every canonical rule exactly once because the canonical set itself is empty.
No imported `MPY` semantic rule is added: doing so would exceed the
launcher-generated canonical inventory.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The canonical local closure contains no equations, recurrences, macros, structural helpers, or other rules. |
| `OPERATIONAL_RULE` | 0 | The canonical local closure contains no execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | Stage 1 contains no local reusable rule and no staged proof establishing a rule before importing it. |
| `DOMAIN_LEMMA` | 0 | The canonical local closure contains no additional trusted mathematical fact. |

There are no canonical rules carrying the `simplification` attribute, so the
required `DEFINITION`-or-`DOMAIN_LEMMA` restriction is satisfied vacuously.

## Stage 1 evidence

`/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It declares no local syntax, equation, recurrence, simplification rule,
operational rule, or lemma. Its SHA-256 value
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`
matches the `verification_sha256` recorded in the canonical inventory.

`/reference/k-proof/prove.sh` compiles that unchanged module and proves
`spec.k`; it also runs expected-failure postcondition and body mutations. It
does not first prove an exact reusable rule against a module lacking that rule
and then rebuild with the rule present. Therefore there are no separately
proved derived lemmas and no Stage 1 evidence that would justify a
`PROVED_DERIVED_LEMMA` entry.

The Stage 1 `PROOF.md` independently records that its proof-extension inventory
is empty and that `verification.k` only imports the supplied semantics.

## Domain-lemma boundary

The domain-lemma set is empty.
