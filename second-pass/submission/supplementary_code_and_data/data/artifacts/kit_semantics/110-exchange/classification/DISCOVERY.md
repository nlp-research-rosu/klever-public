# K proof trust-boundary discovery

The canonical inventory hash is
`28f7d11cd40b6c85cf800f361b0188ccab45c2024b37a26f522ded53d34dd534`.
It contains 37 rules, all classified exactly once and in canonical inventory
order in `trust-boundary.json`.

## Classification summary

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 29 | Exact syntax macros; equations for total projections and their structural machinery; and exhaustive equations or recurrences for `boolToInt`, the numeric-domain predicates, parity, counting, and the result summary. |
| `OPERATIONAL_RULE` | 3 | Missing execution-model cases for Bool modulo, Float modulo, and Float equality against integer zero. |
| `PROVED_DERIVED_LEMMA` | 0 | No canonical source rule has the required Stage 1 evidence of its exact statement being proved first against a module excluding that rule. |
| `DOMAIN_LEMMA` | 5 | Unproved simplifications about partial-cast definedness, parity composition, and modulo definedness. |

The macro rules are definitions because they expand names into the exact
translated program syntax and do not replace runtime execution. The
`definedProject*`, `project*Total`, and collapse/orientation/idempotence
equations define named proof helpers. The `boolToInt`, `isNumberVal`,
`allNumbers`, `numberEven`, `evenCount`, and `exchangeResult` equations define
mathematical summaries by constructor cases, structural recursion, or
complementary guards.

The three `applyBin`/`applyCmp` primitive cases at verification lines 106-108
are ordinary execution or observation rules in the extended Python model.
They are therefore `OPERATIONAL_RULE`, even though Stage 1 describes their
value contracts as part of its trust boundary.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 does contain bridge-free supporting proofs. `connection-spec.k`
imports `VERIFICATION-BASE`, which excludes the two rules in module
`VERIFICATION`, and states three per-sort parity-composition claims plus three
source-expression execution claims. `prove.sh` compiles the base definition
at lines 28-32 and runs that connection specification at lines 40-42 before
the target proof at lines 43-45; the final `prove.out` begins with `#Top` for
the connection proof and `#Top` for the target proof.

That evidence does not make a canonical rule a proved derived lemma under the
requested classification rule. The inventory contains one guarded `Val` parity
simplification, while the mounted auxiliary evidence consists of separate
`Int`, `Bool`, and `Float` reachability claims rather than the exact source-rule
statement. In addition, the parity rule carries `simplification`, which the
classification contract permits only as `DEFINITION` or `DOMAIN_LEMMA`. The
modulo-definedness simplification has no exact auxiliary claim at all. The
three partial-cast `#Ceil` simplifications likewise have no exact
pre-installation claims in `connection-spec.k`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these five canonical
rules:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`:
  definedness characterization of the partial Val-to-Int cast.
- `rule-e1f0f7da39177f5e6e65ea0afce67a1341dc2b663fda1ad070a7a09dec8d1a06`:
  definedness characterization of the partial Val-to-Bool cast.
- `rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43`:
  definedness characterization of the partial Val-to-Float cast.
- `rule-f297fbc0d836c7026aa18875014896223d568b8e6387f7a05ff3ae9fb97cdc9a`:
  parity-composition equality over guarded numeric `Val` inputs.
- `rule-4ec80ff33d0e12af220ea89dbd4fcab9751644a447d6e835ae4463ed423b09a0`:
  modulo-by-2 definedness over guarded numeric `Val` inputs.

These rules contribute additional logical facts used by symbolic
simplification. The Stage 1 connection proof is meaningful supporting evidence
for the parity-composition fact, but it does not satisfy the stricter
exact-source-rule criterion for `PROVED_DERIVED_LEMMA`. The other four have no
separate exact proof command in the mounted `prove.sh`.
