# Independent classification ledger

This ledger records the audit's classifications after reading the frozen
`verification.k`, its imported operational semantics, the source solution,
the postcondition, and Stage 1 proof order. It is not copied from the protected
classification rationales. Exact full identities and source text are in
`reconstructed-inventory.json` and `13_inventory_classification_index.log`.

| Inventory position | Source lines | Independent class | Reason |
|---:|---:|---|---|
| 1 | 34–76 | `DEFINITION` | Expands the named `innerBody` proof/program term. |
| 2 | 78–79 | `DEFINITION` | Expands the named `outerBody` proof/program term. |
| 3 | 81–109 | `DEFINITION` | Expands the named `findBody` proof/program term. |
| 4 | 111–118 | `DEFINITION` | Expands the named `solutionModule` proof/program term. |
| 5 | 120 | `DEFINITION` | Empty base equation of `allFloatVS`. |
| 6 | 121–122 | `DEFINITION` | Tail-recursive equation of `allFloatVS`. |
| 7 | 123 | `DEFINITION` | Float projection equation. |
| 8 | 125 | `DEFINITION` | Empty base equation of `allFloatItems`. |
| 9 | 126–133 | `DEFINITION` | Tail-recursive equation of `allFloatItems`. |
| 10 | 134–136 | `DEFINITION` | Canonical-tuple projection defining `itemIndex`. |
| 11 | 137–139 | `DEFINITION` | Canonical-tuple projection defining `itemFloat`. |
| 12 | 141–147 | `DOMAIN_LEMMA` | Guarded cross-symbol fact: operational `applyIndex` at 0 agrees with the summary projection. |
| 13 | 148–154 | `DOMAIN_LEMMA` | Guarded cross-symbol fact: operational `applyIndex` at 1 agrees with the summary projection. |
| 14 | 156–159 | `DOMAIN_LEMMA` | Cross-function preservation fact from `allFloatVS` through operational enumeration. |
| 15 | 161–162 | `DEFINITION` | True branch defining `orderedFirst`. |
| 16 | 163–164 | `DEFINITION` | Complementary branch defining `orderedFirst`. |
| 17 | 165–166 | `DEFINITION` | True branch defining `orderedSecond`. |
| 18 | 167–168 | `DEFINITION` | Complementary branch defining `orderedSecond`. |
| 19 | 169–173 | `DEFINITION` | Defines the Boolean `candidateWins` summary. |
| 20 | 175–177 | `DEFINITION` | Nonwinning branch of `stepFirst`. |
| 21 | 178–181 | `DEFINITION` | Winning/ordered branch of `stepFirst`. |
| 22 | 182–185 | `DEFINITION` | Winning/reverse branch completing `stepFirst`. |
| 23 | 187–189 | `DEFINITION` | Nonwinning branch of `stepSecond`. |
| 24 | 190–193 | `DEFINITION` | Winning/ordered branch of `stepSecond`. |
| 25 | 194–197 | `DEFINITION` | Winning/reverse branch completing `stepSecond`. |
| 26 | 199 | `DEFINITION` | Empty base equation of `innerFirst`. |
| 27 | 200–209 | `DEFINITION` | Tail-recursive equation of `innerFirst`. |
| 28 | 211 | `DEFINITION` | Empty base equation of `innerSecond`. |
| 29 | 212–221 | `DEFINITION` | Tail-recursive equation of `innerSecond`. |
| 30 | 223 | `DEFINITION` | Empty base equation of `outerFirst`. |
| 31 | 224–233 | `DEFINITION` | Tail-recursive equation of `outerFirst`. |
| 32 | 235 | `DEFINITION` | Empty base equation of `outerSecond`. |
| 33 | 236–245 | `DEFINITION` | Tail-recursive equation of `outerSecond`. |
| 34 | 247 | `DEFINITION` | Empty base equation of `lastItem`. |
| 35 | 248–249 | `DEFINITION` | Tail-recursive equation of `lastItem`. |
| 36 | 255–316 | `PROVED_DERIVED_LEMMA` | Exact loop-state transition was first proved in `CONNECTION-SPEC` against `VERIFICATION-BASE`, which excludes this rule, and only later compiled into `VERIFICATION`. The independent rerun returned `#Top`. |

Counts: 32 `DEFINITION`, 0 `OPERATIONAL_RULE`, 3 `DOMAIN_LEMMA`, and
1 `PROVED_DERIVED_LEMMA`. The only three `[simplification]` rules are entries
12–14, all `DOMAIN_LEMMA`.
