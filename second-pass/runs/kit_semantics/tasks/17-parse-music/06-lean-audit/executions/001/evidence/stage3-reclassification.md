# Independent Stage 3 reclassification

Canonical closure: `VERIFICATION-SYNTAX`, `VERIFICATION`.
Canonical rule count: 17. Canonical inventory SHA-256:
`932e796013ca30c337145920f57c5b5c304c9fb7d35633917a2a159a409a7759`.

All 17 rules have an empty attribute list, so there are no
`simplification` rules to constrain further.

| Source span | Source rule ID | Independent class | Source-based judgment |
|---|---|---|---|
| 28–35 | `rule-257ca9660ae22dcacc7b15bbf785685f8c356c7b43418504a164d44e38708c9f` | `DEFINITION` | `parseMusicBody` is declared `[function, total]` with result sort `Stmts`; the rule expands that nullary named proof term to the exact source-body AST. It has no configuration cells and does not bypass program execution. |
| 37–51 | `rule-4a39232d9506f530270fcca65f8e02a3896683acbb5fe8b232cd1e547a431787` | `DEFINITION` | `parseMusicCharBody` similarly names and expands the exact per-character statement AST. The supplied `For`, `If`, assignment, lookup, comparison, call, and append semantics execute the expanded AST. |
| 54–61 | `rule-337f98ce7cc6d51fa465ab05df2a31c55eba0a5f7f685090f1b54fb1649a2514` | `DEFINITION` | `mutatedParseMusicBody` is a validation-only named statement term. It is not used by the positive claim and its equation only expands syntax. |
| 63–77 | `rule-980abec36ad2f781db47cd80b4540009c758d890a52ca2bbaf4d935b61779762` | `DEFINITION` | `mutatedParseMusicCharBody` is the mutation’s named statement term, with `o` assigning 5. It is syntax expansion, not a fact about the positive result. |
| 79–80 | `rule-b0124a9f043ed584d496c9e52429143a95acc4f175b1e56fc2eba7445209c3e9` | `DEFINITION` | First guarded equation of the one-character `nextCurrent` state-transition summary: code 111 (`o`) sets current to 4. |
| 81–82 | `rule-a59f15873fdeb400192d57d27babb377f4c0fc3adf89f5fa9056fad3fef0dda7` | `DEFINITION` | Second guarded `nextCurrent` equation: code 46 (`.`) sets current to 1. |
| 83–84 | `rule-92f4391d6442c464054dba410fc1a5878a21def33f74db3ee7db2cb2fc9abae4` | `DEFINITION` | Complementary `nextCurrent` equation: every other code resets current to 0. The three guards are disjoint and exhaustive. |
| 86–88 | `rule-dd407de08a96a30627c1b867644a8e990f4c2114bdf28a720a76d8faf5b5428d` | `DEFINITION` | First guarded equation of `nextResult`: a pipe with current 4 appends 2, matching the operational body’s conversion before `append`. |
| 89–91 | `rule-abd7cda93d21f2746bf87d8c76f2179708caf99cfd5bc4c581273af9a5837d12` | `DEFINITION` | A pipe with current not equal to 4 appends that current value. |
| 92–95 | `rule-a629c59a24598ad5aeb1674282f47234c39e83afb49bb8d3545f0c34801b0220` | `DEFINITION` | A non-`o`, non-`.`, non-pipe separator with pending current 4 flushes 4. |
| 96–98 | `rule-797e9c5a0b0cd11316f7c5583c1ae10656c9fee2c079dd5543c5eb5b00bc4e8b` | `DEFINITION` | Complementary no-append case for `o`, `.`, or an ordinary character with current not equal to 4. Together the four `nextResult` guards are disjoint and exhaustive. |
| 100 | `rule-9af625c9e24775a898bf6f08978326e33e5514631d2adecaa8ddca696dc47bce` | `DEFINITION` | Base equation of the `scanCurrent` recurrence. |
| 101–102 | `rule-bda12c0b7b12bf5165f63c4f9e337f373a5c25f912e8e05c596663abc36bd377` | `DEFINITION` | Structural recursive step of `scanCurrent`, consuming the strict `IntSeq` tail. |
| 104 | `rule-57e80bba26c5c3ffdb20ae7725ad9f53ddb6a1f6001409e9cf5b314097914076` | `DEFINITION` | Base equation of the accumulated-result recurrence. |
| 105–106 | `rule-848e66171181463d17a0396ceaf1ae273c47d3e2a59ce320572601ec6b63c47a` | `DEFINITION` | Structural recursive step of `scanResult`, using the old current for the result update and the new current for the tail. This agrees with sequential execution. |
| 108–110 | `rule-2b43fdbce21c598f6cfa95b3146c8de11d9da189c5a51c432315e84d3bb3fb49` | `DEFINITION` | First guarded equation of the final `musicResult` summary: append 4 exactly when the terminal current is 4. |
| 111–112 | `rule-2b437edda63b60e58d0efb16565d8f7af223669e9688944c34daaee4d30a6c60` | `DEFINITION` | Complementary final-summary equation with no terminal flush. |

Independent totals:

- `DEFINITION`: 17
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The two statement-body pairs are named proof-term definitions. The remaining
thirteen equations define state-transition, recurrence, and final-summary
functions. None is an ordinary `<k>`-cell execution/observation rule, none
asserts an additional mathematical property of a result, and none is presented
as a separately proved derived lemma. The operational connection is stated in
the `scan-loop` and `parse-music` claims, not assumed by any inventory rule.

The independent finite sensitivity check in `semantic-crosscheck.txt` compared
direct statement execution with the definitions over 55,987 strings (lengths
0–6 over note, pipe, separator, negative, and non-ASCII representative codes),
found zero mismatches, checked 1,224 transition-guard points with zero gaps or
overlaps, and showed that changing the operational `o` assignment from 4 to 5
breaks the connection on `o`, `o|`, and `o `.
