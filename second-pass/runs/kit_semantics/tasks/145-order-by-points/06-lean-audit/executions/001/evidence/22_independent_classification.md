# Independent Stage 3 classification

The canonical inventory contains 20 rules in source order. Every rule has an
empty attribute list, so there are no `simplification` rules to constrain.

| Index | Source span | `source_rule_id` | Independent class | Operational judgment |
|---:|---:|---|---|---|
| 0 | 8–11 | `rule-664c5cffd59c4d15b07d7fe6963f00cf5c76f67667d8d821ffde854f571a8012` | `DEFINITION` | Macro defining the exact two-statement loop body. |
| 1 | 14–23 | `rule-37a274447eef3c1ee182a04b21215a965bc6dfb48a8d775adac404e38ed35b2e` | `DEFINITION` | Macro defining the exact helper body. |
| 2 | 26–28 | `rule-d10f1357927738dce878b76dcd6916c350886d346342c7e1507243e50c56b398` | `DEFINITION` | Macro defining the exact `order_by_points` body. |
| 3 | 31–34 | `rule-2bcc3a782cae89edaedc8c1c582e99adc92dd5b52e6e4293aaa849284675298e` | `DEFINITION` | Macro defining the exact two-function solution module. |
| 4 | 53–54 | `rule-89524501d065de2184fd649e6c2a4d12c0617b3d9484d98f412da0bc5a320a58` | `DEFINITION` | Nonnegative equation for the named magnitude summary. |
| 5 | 55–56 | `rule-51613c351a9ee9d29c0df749014a4c0ec66657c732af60663ce004d43d9db384` | `DEFINITION` | Negative equation completing the magnitude summary. |
| 6 | 58–59 | `rule-1bf5ab2e5866c1d5602ded739d5e0f210a57c3bf0cec5ef2927d240001947300` | `DEFINITION` | Base equation for the named leading-digit recurrence. |
| 7 | 60–62 | `rule-314cf3fcec8b46a733193a40de36b18e51627b0fb15c93b03494ec3721866b49` | `DEFINITION` | Descending recursive equation for leading digit. |
| 8 | 63–64 | `rule-097fea3c01124835e2ae5042549724568e9e5006cd3f576914127cd69a3c9df9` | `DEFINITION` | Sign-normalization equation completing leading digit. |
| 9 | 66–67 | `rule-69e315e1d05a8f425b9cfcb934b2f1905a48322f4195804aa285ca0e4427e91f` | `DEFINITION` | Nonnegative wrapper for the named lower-digit-sum summary. |
| 10 | 68–69 | `rule-3b276991d1f91b8e5cc51735489951abd73fb526169bb04e399104f001a224a4` | `DEFINITION` | Negative wrapper completing lower digit sum. |
| 11 | 71–72 | `rule-3f844955132ca42829d67c395f3288694844caafb14ad7b4fe8ef53187d4f118` | `DEFINITION` | Base equation for the accumulator recurrence. |
| 12 | 73–77 | `rule-b4920009e06113fdf703a6cb36186666742665c97b4ed78943a227243de5dc4d` | `DEFINITION` | Descending accumulator recurrence matching `% 10` and `// 10`. |
| 13 | 78–80 | `rule-96f8620115502a6df22703a1d746725f82cad0295eb51649668c01cbae750d9c` | `DEFINITION` | Sign-normalization equation completing the accumulator. |
| 14 | 82–84 | `rule-76f34bf82234cb4c2c32cbab9099c92eb28349df1463a03bff220a05fc31f22c` | `DEFINITION` | Nonnegative equation for the named signed-digit-sum summary. |
| 15 | 85–87 | `rule-5dbcf12000be30e9fb65265653327ab18992752ce00fe93176b8e6b5c49b0564` | `DEFINITION` | Negative equation for the signed-leading-digit convention. |
| 16 | 89 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty-sequence equation for the named input predicate. |
| 17 | 90 | `rule-eb01b6f961218a9e5b8ece457a30b8c7cb8b55db7fb423d286186ba232f0aee3` | `DEFINITION` | Integer-head recurrence for the input predicate. |
| 18 | 91–92 | `rule-571c5f5e487d813d7b511f60c911baa33380f2fcf106096134e0fb29fc85d948` | `DEFINITION` | Guarded noninteger-head equation completing the predicate. |
| 19 | 94–97 | `rule-c5fdbfcf27bbfa96fa6468cc9627e36302b4d27e47f7921e4affc7d9e52f3ae6` | `DEFINITION` | Named postcondition term, exactly `sortKeyVS` with the exact helper closure. |

No rule is an ordinary execution/observation rule: none rewrites a K
configuration, continuation, call, loop, cell, or observable state. No rule is
a proved-derived lemma: the inventory contains equations only, and no entry is
first proved as an exact rule in an earlier lemma-free module. No rule relates
already-defined concepts by a new source-domain fact. In particular,
`expectedOrder` does not assert ordering, permutation, or stability; it merely
names the supplied semantics' opaque keyed-sort result.

The fixed semantics connects the summaries to execution through the Stage 1
claims, not through inventory rules: `While` expands to `#while`, `AugAssign`
updates the current scope through `applyBin`, integer `%` is `pyMod`, integer
`//` is `(n - pyMod n d) / d`, function calls execute the stored closure body,
and keyed `sorted` allocates `list(sortKeyVS(VS, KV))`. Thus the local inventory
has a genuinely empty domain-lemma set.
