# Independent Stage 3 classification

Inputs used: frozen `/reference/k-proof/verification.k`, its imported supplied
semantics under `/reference/k-proof/reference-semantics`, `solution.py`,
`prompt.py`, `spec.k`, `projection-spec.k`, and the trusted reconstructed
inventory in `09_reconstructed_inventory.json`.

| Source span | Source rule ID | Independent class | Reason |
|---|---|---|---|
| 23–30 | `rule-b2c209cbfb86e10d3005fcbcaddad9fb6973a85bbc2fe08a30ef519144e95200` | `DEFINITION` | Expands the new macro `ODD-COUNT-BODY` to the submitted function body. It names syntax and does not replace a supplied-semantics redex. |
| 32–77 | `rule-f6bccf2b300308151acf57db46505922cb5a0e2dafdbd6b77d87aadedfef04c5` | `DEFINITION` | Expands the new macro `ODD-COUNT-LOOP-BODY` to the submitted loop body. |
| 79 | `rule-95374d0a84c6a23904e4713a65b95c744fe38e69620525d775e9628ff14e6752` | `DEFINITION` | Positive constructor equation for the new total recognizer `isStringVal`. |
| 80 | `rule-db5d291bfef4ca80c5d2cb8f0776deb35e0a02db35e0eea12e17a2ed0e884650` | `DEFINITION` | Owise complement of the same recognizer; together the two rules are a structural definition. |
| 82 | `rule-5161696e21cd28fd8c521223458bf22e24dc411233197e49e6996cadae2e20ba` | `DEFINITION` | Constructor projection defining the new `stringCodes` symbol on strings. It is marked `simplification`, which is permitted for a definition. |
| 84 | `rule-a5cb10bd07da5eeaf46fc3e953458938d4f05f60e707e87826a035b1d20b2e7b` | `DEFINITION` | Base equation for the new recursive input-domain predicate `allDigitStrings`. |
| 85–88 | `rule-ecc99dfcf495fb9646debbe387e8680c94ed360d8c192614f0f1793d25f55398` | `DEFINITION` | Cons recurrence for `allDigitStrings`, descending on `REST`. |
| 90–93 | `rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617` | `DOMAIN_LEMMA` | This does not define a new symbol. It adds a guarded simplification for the pre-existing supplied-semantics operation `applyMethod`, replacing a symbolic `Val` receiver by the existing string-count equation through `isStringVal` and `stringCodes`. `projection-spec.k` first proves only the constructor-specialized supplied rule `applyMethod(str(CODES), …) => cntSub(CODES, …)`; it does not prove this exact guarded rule in a module omitting it. The rule is directly relevant because the source loop calls `s.count` five times while `s` is symbolically typed as `Val`. |
| 95–100 | `rule-83a775072e73378ed8c0155ce91d0456798fc3dcffc6042703bdcd4893210cef` | `DEFINITION` | Defines the new summary `oddDigitCount` as the five supplied `cntSub` results used by the source. |
| 102–127 | `rule-67f5fd2129530d56a839f60730a014adf262947508fb5e830431372a6561d0e8` | `DEFINITION` | Defines the new result-string summary `oddLine` using the exact nested concatenations in the source. |
| 129 | `rule-08220f49c02697fb0e4703183c0c540803b0b044abb140b847951d5987027294` | `DEFINITION` | Base equation for the new accumulator summary `oddLinesAcc`. |
| 130–133 | `rule-e54bc8d016ba3ceaef31af00ca2b8557b8cd9f387e2eceb7c2a58f63d708b434` | `DEFINITION` | Cons recurrence for `oddLinesAcc`, descending on `REST` and appending the current `oddLine`. |

Classification counts: 11 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`.

The independent ordered classification exactly matches
`/reference/lemma-discovery.json`. Both simplification rules are in an allowed
class: `stringCodes` is a `DEFINITION`; the guarded `applyMethod` extension is
a `DOMAIN_LEMMA`. The domain lemma is mathematically substantive, satisfiable
for every `str(CODES)` receiver, and relevant to both the frozen source and
postcondition.
