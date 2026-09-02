# Trust-boundary discovery

## Canonical inventory

The sole classification source is `/reference/rule-inventory.json`.
Its copied inventory digest is:

```text
b74ac0a769f9ce93027f625ba4030e585fe307aa7c7ec1941c933938c4cea026
```

The inventory contains 21 rules, all in the local `VERIFICATION` module. Each
canonical `source_rule_id` appears exactly once in `trust-boundary.json` and in
the same order as the inventory.

Classification totals:

| Classification | Count |
|---|---:|
| `DEFINITION` | 17 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 4 |

## Definitions

The following groups are equations or structural recurrences defining fresh
mathematical summaries or named proof terms:

- `definedProjectStr`, the guarded defining orientations and static collapse
  for `projectStrTotal`, and `codesOf`;
- both equations of the structural input predicate `allStrings`;
- `uniqueCount` and `candidateWins`;
- the base and cons equations for `bestWord`, `bestScore`, `lastWord`, and
  `lastScore`.

The guarded forward and reverse projection orientations are definitions because
they assign the meaning and normal form of the fresh `projectStrTotal` proof
term on its stated domain. The static collapse is likewise a defining case.

## Operational rules

The canonical local closure contains no `OPERATIONAL_RULE` entries. It has no
ordinary K-cell execution rule or local observation rule without a
`simplification` attribute. The two rules over `applyBuiltin` and `applyCmp`
are simplifications, so the requested classification constraint excludes
`OPERATIONAL_RULE`; their actual trust role is recorded as `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no canonical rules classified as `PROVED_DERIVED_LEMMA`.

Stage 1 does contain separate bridge-free proof evidence:

```bash
kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

`connection.k` imports only the supplied `MPY` semantics and does not import
`VERIFICATION`. The recorded output in `prove.out` is two
`WarnTrivialClaim` notices followed by `#Top` at line 267. The claims checked
are the static constructor equations:

- fixed `set(str(CS))` produces `setV(dedupCodes(CS))`;
- fixed `str(A) < str(B)` produces `strLt(A, B)`.

Those claims are not exact statements of either canonical dispatch rule. The
inventory rules quantify over dynamic `Val` operands, add
`definedProjectStr` guards, and use `projectStrTotal` plus `codesOf` on their
right-hand sides. Because the required exact correspondence is absent, the
Stage 1 connection claims do not justify labeling either dynamic rule
`PROVED_DERIVED_LEMMA`. No other rule is first proved by `prove.sh` in a module
that omits that exact rule.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly four rules:

1. `rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83`
   — the `#Ceil` characterization of the partial `Val :> Str` cast.
2. `rule-f85e27b93f985712e161e1d9f93c9edc4bb9b998f80b67e076ae37e57255f5e0`
   — idempotence of `projectStrTotal`.
3. `rule-ec057976d8c8f7e9534ebd2d518671f034dd02fd1170d6411f89c1fd1a2417c3`
   — guarded dynamic dispatch for `set`.
4. `rule-1684a1226f0f56832d19a2311f81f35f276a3945a3d87268f06be40436a1f20b`
   — guarded dynamic dispatch for string less-than.

The cast-definedness and idempotence rules are additional simplification facts
and have no exact prior proof in Stage 1. The two dispatch rules are supported
by, but are strictly more general in syntax than, the separately checked
static constructor equations. They therefore remain inside the trusted
mathematical domain-lemma boundary.
