# Independent Stage 3 classification

The canonical local verification-module closure is only `VERIFICATION`. It
contains 10 rules, in source order.

| Source span | `source_rule_id` | Independent class | Judgment |
|---|---|---|---|
| 7–9 | `rule-106b748797b8869ec5735d1b277b53f4922be8d92cbb3ba87f899c23d0041e14` | `DEFINITION` | Expands the named `vowelCodes` macro to the exact ten-code `IntSeq`. |
| 12–16 | `rule-c967809d7c1f7190c8ad73e7c196724ba72b22ff8161f4b280ffeb5eec91a81e` | `DEFINITION` | Defines the named total predicate `isVowelCode` as equality with exactly the ten vowel codes. |
| 21–23 | `rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93` | `DOMAIN_LEMMA` | Neither side is newly defined here: `strContains` is defined in supplied `MPY-STR`, while `isVowelCode` was already defined above. The rule adds a specialization equating one-character substring membership in `vowelCodes` with the vowel predicate. Stage 1 did not first prove the exact rule in a module omitting it, so it is not a `PROVED_DERIVED_LEMMA`. It is relevant because source line 5 evaluates `char not in "aeiouAEIOU"` through `strContains`, while the loop claims split on `isVowelCode(C)`. |
| 26 | `rule-97869f576bcf072c1e721ed24f69ba5c2404fb7d8241edd4bd0cbf2adf281b44` | `DEFINITION` | Base recurrence for the named accumulator summary `removeVowelCodesAcc`. |
| 27–29 | `rule-df6da58f7a0c1c0940d1bd577e8a42fc8ff60217334b4e9bd2e5a09b1823c83d` | `DEFINITION` | Vowel branch of the named accumulator recurrence. |
| 30–34 | `rule-8ec35c1199777440cd8b9746f870473e6535a49693f2fb23e096ec49b033f27c` | `DEFINITION` | Non-vowel branch of the named accumulator recurrence. |
| 37–38 | `rule-e49f3d3c6e39dc85fb288d725af9349d2df4de5586b32a1b424f814fac9349eb` | `DEFINITION` | Defines the named `removeVowelCodes` summary by initializing its accumulator. |
| 41–44 | `rule-a9e187a09a57d67c0d8c745e6d6ada346f64b15ef44e8ec7b86c0a2433ed155c` | `DEFINITION` | Expands the named loop-body macro to the exact source AST operation. |
| 47–51 | `rule-5394773feede596d124dfa31cfc1aa168d372d38c5862101ecba343ac2ca9a0a` | `DEFINITION` | Expands the named function-body macro to initialization, loop, and return AST. |
| 54–56 | `rule-1c6bbd7732f50537067c061cd7f506047f5635d0143334615f896552cdfe5711` | `DEFINITION` | Expands the named program macro to the source function definition AST. |

Independent totals: 9 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`. These exactly equal the protected
Stage 3 labels.

The supplied string semantics defines `strPrefix` structurally and
`strContains(P, X)` by returning true at a matching prefix and otherwise
recursing over the haystack. For a singleton needle `[C]` and the concrete
haystack `[97,101,105,111,117,65,69,73,79,85]`, this is true exactly when `C`
equals one of those ten values, which is exactly `isVowelCode(C)`. Thus the
domain lemma is mathematically valid over all K `Int` values.

No inventoried rule has a `simplification` attribute. The domain lemma has only
`priority(40)`, so the special simplification-class restriction is satisfied.
