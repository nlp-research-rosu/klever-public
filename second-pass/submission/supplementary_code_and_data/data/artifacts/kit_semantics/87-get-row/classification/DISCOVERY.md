# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`341c239f750211e8fd0165f2fec51a0237792c9f2ecb13194dc5a1c10de5135c`.
It contains 13 rules, all classified exactly once and in canonical order in
`trust-boundary.json`.

## Classification summary

- 12 `DEFINITION`
- 0 `OPERATIONAL_RULE`
- 1 `PROVED_DERIVED_LEMMA`
- 0 `DOMAIN_LEMMA`

The domain-lemma set is empty. No additional unproved mathematical fact in the
canonical inventory is trusted to close the proof.

## Rule-by-rule classification

| Canonical rule | Classification | Reason |
|---|---|---|
| `rule-884ba37529d334ff1536a797b79c37b0c1aec1517e50018bbcdd7e37dc667f49` | `PROVED_DERIVED_LEMMA` | The `For`-to-`#loop` rule has a prior bridge-free proof of the exact rewrite and guard, as detailed below. |
| `rule-61639aeb3e4eded394e1d4b26f9ee1295448bf3ece5ac65e09a909061f5802ed` | `DEFINITION` | Empty-sequence base equation for `advanceIndex`. |
| `rule-66ce320138cf211431fb75578ddb97ab1ae42b0641cbe44f60c87c594342d78b` | `DEFINITION` | Structurally recursive cons equation for `advanceIndex`. |
| `rule-c194ab0b0d5b805678184ae23956c929962cbe0d80d58f6329b819af01736b5b` | `DEFINITION` | Empty-sequence base equation for the `scanAppend` summary. |
| `rule-f34eeff932b7abe8c16eabf63b849ff14abedadb470e8cc2afef3c5432725a54` | `DEFINITION` | Matching-element recurrence for `scanAppend`; its `simplification` attribute does not turn the defining equation into a lemma. |
| `rule-4e4b59f2ee8e8937c5779283b3c612d56db07d5a6665f7d3c5cd3081cfe4c1ff` | `DEFINITION` | Complementary nonmatching-element recurrence for `scanAppend`, also marked `simplification`. |
| `rule-4812be0f87480004ec1d88555dc42724de85607ba560b55f59cc783b411b4b54` | `DEFINITION` | Empty-row-sequence base equation for the `rowsAppend` summary. |
| `rule-ca82d2906a1a64f2f30d91c523b1da3a97bdc91d39bf996607ba4b0eb8dedf1f` | `DEFINITION` | Guarded row recurrence for `rowsAppend`, marked `simplification`. |
| `rule-513effea58452b129f11e969f69b8b1ba4753f0475e7adccd0435ef28aa12dc3` | `DEFINITION` | Macro expansion defining `INNERBODY`. |
| `rule-a5d752033c107eb7ed24b3bd20619e493bc116b42cee0b9c358ddef4a7846bce` | `DEFINITION` | Macro expansion defining `OUTERBODY`. |
| `rule-f1c7c2f7e079aec7d74121119086f5ce9b88d758dc886ab637c02f5d1a3efff4` | `DEFINITION` | Macro expansion defining `GETROWBODY`. |
| `rule-f673c7a1de0fb731d8b8b9003d5b2dc47528b1ed6b2c77eea115e579be27e7f5` | `DEFINITION` | Macro expansion defining the named closure term `COLUMNCLOSURE`. |
| `rule-734823e8299b7b2d2a2ba3a8604e4912e0ff16f6d7012cabd5bf2251083265db` | `DEFINITION` | Macro expansion defining the named closure term `ROWCLOSURE`. |

The three canonical rules carrying `simplification` are therefore all
`DEFINITION`: the two complementary recursive `scanAppend` equations and the
guarded recursive `rowsAppend` equation.

## Separately proved derived lemma

There is exactly one separately proved derived lemma:
`rule-884ba37529d334ff1536a797b79c37b0c1aec1517e50018bbcdd7e37dc667f49`.

The mounted Stage 1 evidence establishes both exact correspondence and proof
ordering:

1. `/reference/k-proof/shape-connection-spec.k`, lines 6–9, contains
   `SHAPE-CONNECTION-SPEC.for-list-shape` with the same `For` source,
   `#loop(list(rowContents(V)), T, B)` destination, arbitrary continuation, and
   guard as the canonical verification rule.
2. `/reference/k-proof/shape-connection.k`, lines 1–5, imports only
   `ROW-MODEL`; it does not import `VERIFICATION` and therefore does not contain
   the canonical rule being proved.
3. `/reference/k-proof/prove.sh`, lines 34–40, compiles that bridge-free module
   and proves the connection claim. `/reference/k-proof/prove.log`, line 94,
   records `#Top`.
4. Only afterward, at `/reference/k-proof/prove.sh`, lines 42–48, is
   `verification.k` compiled and the target specification proved. The reusable
   priority rule appears at `/reference/k-proof/verification.k`, lines 21–24;
   the later target proof records `#Top` at `/reference/k-proof/prove.log`,
   line 151.

Although the derived rule accelerates an operational `For` setup step, it is
not classified as an unproved `OPERATIONAL_RULE`: the mounted evidence meets
the requested stricter `PROVED_DERIVED_LEMMA` criterion before the rule enters
the verification module.

## Empty classes

There are no `OPERATIONAL_RULE` entries after recognizing the independently
proved `For` connection. The other canonical rules only define summary
functions or expand named macro terms; they do not add ordinary execution or
observation behavior.

The `DOMAIN_LEMMA` set is empty: none of the canonical rules supplies an
additional unproved mathematical fact.
