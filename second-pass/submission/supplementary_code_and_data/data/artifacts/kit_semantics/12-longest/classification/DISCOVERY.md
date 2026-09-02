# Trust-boundary discovery

## Canonical source

The classification uses `/reference/rule-inventory.json` as the exhaustive
inventory. Its copied inventory digest is
`11838d318c7fc07f68702a780c2b4e461084d9eeb535b76cad4d65a4128c7631`.
All 16 source rule IDs occur once, in canonical order.

| Classification | Count |
|---|---:|
| `DEFINITION` | 14 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

## Definitions

The `isStringValue` and `allStrings` rules are exhaustive structural
definitions of the proof domain. The `projectString` equations define and
normalize a named total projection, including guarded cast orientation,
static-sort collapse, and idempotence. `seqLenString` defines a named
static-sort length summary. The remaining equations define the recursive
`scanLongest` fold and the `longestValue` contract summary.

Those rules introduce or normalize proof-local named terms rather than assert
new facts about an already fixed operation, so they are `DEFINITION`. This
also places every definitional simplification rule in one of the two
classifications permitted for rules carrying `simplification`.

## Separately proved derived lemmas

There are no inventory rules classified as `PROVED_DERIVED_LEMMA`.

Stage 1 does contain two separately run connection claims:

- `CONNECTION-SPEC.string-length-connection` checks the canonical `Str`
  instance connecting fixed `seqLen` with `seqLenString`.
- `CONNECTION-SPEC.string-projection-connection` checks projection collapse
  for canonical `str(CS)` values.

The ordering evidence is `/reference/k-proof/prove.sh`: it compiles
`verification.k` with main module `VERIFICATION-BASE`, runs
`kprove connection-spec.k --definition connection-kompiled --spec-module
CONNECTION-SPEC`, and only afterward compiles the full `VERIFICATION` module.
`/reference/k-proof/PROOF.md` records `#Top` and exit 0, along with
`WarnTrivialClaim` for both claims.

Neither claim has exact statement correspondence with a canonical inventory
rule. In addition, the base definition used for those proofs already contains
the `projectString` collapse and `seqLenString` constructor equations.
Therefore the connection evidence does not make either defining equation a
separately proved rule, and its canonical-string scope does not prove the
broader guarded dynamic-`Val` `seqLen` simplification exactly.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

1. `rule-ddffe23dc5c6ffd5ffac0d16bb982569a790626473fe51f3053dbbcfd160d303`,
   which characterizes the definedness of the pre-existing partial cast
   `{V}:>Str` using `isStringValue`.
2. `rule-a83d2beb46d0d51905977beb804054c3129461bb6f5faf35187591b53b4dc122`,
   which rewrites the pre-existing `seqLen(V)` observation to the proof-local
   projected length under `isStringValue(V)`.

Both carry `simplification`, both assert additional facts about fixed
operations rather than merely define their left-hand symbols, and neither is
the exact statement of a rule proved earlier by `prove.sh`. They are therefore
the trusted mathematical facts in the local verification-module closure.

## Operational rules

No canonical local rule is classified as `OPERATIONAL_RULE`. Source-language
execution rules live in the supplied imported semantics and are outside this
launcher-generated local inventory. The only local rule that rewrites an
existing observation, the guarded `seqLen` simplification, must be classified
as `DOMAIN_LEMMA` because it carries `simplification` and is an unproved
additional equivalence.
