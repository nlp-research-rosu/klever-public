# Independent Stage 3 classification

The trusted inventory selected `MAX-FILL-SUMMARY` and its local closure, which
contains only that module. Its ordered 19-rule inventory hash is
`c38d770ae0a9652b812217694490b3b0706fee0fe43a7d38653391e673572a78`.

| # | Frozen span | Source rule ID | Independent class | Reason |
|---:|---|---|---|---|
| 1 | 9-9 | `rule-3d79da82b43c275c9d34980f5c70a5d2655a97a29064001247280c1e26e49628` | `DEFINITION` | Defines the new named predicate `definedProjectInt` as the supplied-semantics sort test `isInt`. |
| 2 | 14-16 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` | Does not define a new summary or proof-term head: it rewrites the built-in `#Ceil` of a partial Val-to-Int projection into the proposition that the value is an integer (plus the value's definedness). Stage 1 contains no earlier proof of this exact rule in a module omitting it. The fact is relevant because `allBinary`, `rowSum`, the sum loop, and the final program claim project source row elements to integers. |
| 3 | 17-19 | `rule-44699459891b0065e1274df000145d152d5593dbc795d66a9108a23233e8be46` | `DEFINITION` | Guarded defining equation for the named proof term `projectInt`; it names the supplied partial projection when `definedProjectInt` holds. |
| 4 | 20-22 | `rule-2f319fc608bca611d97f73f2eccd57da4594fe7eccf200e64ea8ed18a6d1d77c` | `DEFINITION` | Reverse definitional orientation connecting the supplied projection to the named `projectInt` proof term under the same domain guard. |
| 5 | 23-23 | `rule-46034a138591ba84c5320bfdce28ff27c4aa3b71ab6d96d8b058b079aaf09395` | `DEFINITION` | Constructor case defining `projectInt` on an already-Int value. |
| 6 | 27-27 | `rule-a84abb0c9f7460007105f14618fe68e01c23ed95d5e76276d9dbbbf6caaaa4ab` | `DEFINITION` | Constructor case defining the named `rowVals` projection on a list value. |
| 7 | 30-30 | `rule-ba030e77444ea0ae71094841ccfc19ed9c36a3a4d7d781feeba64d83869abd91` | `DEFINITION` | Defines the named predicate `isListVal` by reconstruction with `rowVals`. |
| 8 | 37-37 | `rule-d485439b4f9a7bc2e21a43a788c49763ed95bb43ce67c13ed8de6c7ae72e5684` | `DEFINITION` | Empty-sequence base equation for the named recursive domain predicate `allBinary`. |
| 9 | 38-42 | `rule-39d37bb16064c309a28bcf1621f1b5d89ffcb8e6e081129875411ff8b13e3020` | `DEFINITION` | Nonempty recursive equation for `allBinary`, with the integer and 0-or-1 head conditions. |
| 10 | 44-44 | `rule-1881128594a7caf02b04803f8a2dfcfc888430ef33bfa5b8a5caabafcdd6327e` | `DEFINITION` | Empty-sequence base equation for the named recursive grid-domain predicate `allRows`. |
| 11 | 45-46 | `rule-5ff5b6060b1a32de00d5fe758e5eaf41e5a1abf0b58b43d5e111a32c905a2fc8` | `DEFINITION` | Nonempty recursive equation for `allRows` in terms of the list projection, `allBinary`, and the tail. |
| 12 | 54-54 | `rule-41943ae4d2d233c4fc22178aa9c1fc1f6c7d9fd9d3c074edcb6f474c9c114cc3` | `DEFINITION` | Base equation for the named `rowSum` execution summary. |
| 13 | 55-55 | `rule-86b1ccf093b81e9c9d9ca5149e3534f3b4b7600685efab3663b1175e00d352f2` | `DEFINITION` | Structurally decreasing recurrence for the named `rowSum` summary, using supplied `intOf`. |
| 14 | 59-62 | `rule-64d73f88068d2576ba631bbefba2d4b4d016acc401b9b48b4abfb2466e99b7fb` | `DEFINITION` | Positive-capacity equation for the named `bucketCost` summary; it mirrors supplied Python floor division via `pyMod`. |
| 15 | 63-64 | `rule-d212810cc7f5c01a08d820bb3797b78d481037be2ba27fcf8d82366426404bfb` | `DEFINITION` | Disjoint totalization equation for the new `bucketCost` summary on nonpositive capacities; it is not an execution rule and the program theorem requires positive capacity. |
| 16 | 66-66 | `rule-d64dccd6306357f40c9b821cb592e9b1ae30964f44f52576617a90c97cb434cb` | `DEFINITION` | Base equation for the named `gridCost` recurrence. |
| 17 | 67-67 | `rule-8e4ed42ce768056a9a2107e00bc2962b9a3f934581c589d848903da0a97a8dc2` | `DEFINITION` | Structurally decreasing equation for `gridCost`, combining the head-row summary with the tail summary. |
| 18 | 72-72 | `rule-63b8f99214b24f4293f9007e279bd8591f69b68897b3583455f02e39940ab1a8` | `DEFINITION` | Base equation for the named `finalRow` loop-target summary. |
| 19 | 73-73 | `rule-979fbd648068a0707834be206f2ec357c17842a5f3a3e6191fbe12989c1a186c` | `DEFINITION` | Structurally decreasing equation for `finalRow`, carrying the current head as the next previous value. |

Independent partition: 18 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`. Every rule carrying a
`simplification` form is therefore classified as either `DEFINITION` or
`DOMAIN_LEMMA`.
