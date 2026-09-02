# Independent Stage 3 classification assessment

Frozen source: `/reference/k-proof/verification.k`  
Verification-module closure reconstructed by trusted inventory: `VERIFICATION`
only. Imported `MPY` is supplied from the required semantics and is not a
local module in `verification.k`.

The reconstructed inventory contains 18 rules. No source rule has an explicit
`simplification` attribute, so the simplification-category restriction is
vacuously satisfied.

| Lines | Source rule ID | Independent class | Source/semantic judgment |
|---:|---|---|---|
| 10–17 | `rule-f8c202908b80c2c388b99c1be16abaf8f9c4b8fc3cee914fff74d55d480342ef` | `DEFINITION` | Macro expansion naming the exact translated loop body. |
| 20–27 | `rule-00812545b60ae4c5d7fd77d9fdecc79cc044f1d1404fe725a3575e70fbef4262` | `DEFINITION` | Macro expansion naming the exact translated function body. |
| 30–32 | `rule-f7be3d212c3d1592ebdf79a22df3ecc6771305d4bb7565346a02fe6bea376f6d` | `DEFINITION` | Macro expansion naming the translated module and function declaration. |
| 37 | `rule-0d4c46a7163f5c5ee21b30bb397721cb0628a5455c22404392aa20e5e8d42cb8` | `DEFINITION` | Empty structural case of the `IntSeq` to `ValSeq` embedding. |
| 38 | `rule-90183a8c4394bedf217e3827729c4a9e6cb5d3a2559e7db0e395c06351a69a52` | `DEFINITION` | Nonempty recursive case of the `IntSeq` to `ValSeq` embedding. |
| 44–45 | `rule-f1304b61ef0700f6d784c4f479dc6ca307a1ea188eac478c7a4c6ab0f135804b` | `OPERATIONAL_RULE` | Ordinary iterator observation: the empty embedded list produces `#iterDone` in the active `<k>` cell. |
| 46–48 | `rule-36391f8e12f5f8d94c79a65f738754ea5869d8276718c9ebab81902718eed204` | `OPERATIONAL_RULE` | Ordinary iterator observation: a nonempty embedded list yields its head and residual iterator in the active `<k>` cell. |
| 53 | `rule-28c461bc215c70d08c69af6f83df7c19347afe113c4faac903bffd93b1ebaf5b` | `DEFINITION` | First-element equation for the named `nextRolling` summary. |
| 54 | `rule-031f07f511776c57805e9703f5aacf45f3bcdcbdeb67a8526a9cf0edef797337` | `DEFINITION` | Initialized-state equation for `nextRolling`, using the supplied integer maximum. |
| 57 | `rule-93ce0d1418cc4746b2a77cb93cd1fae392dee7212adcba594e7beb78ce3b65ac` | `DEFINITION` | Empty base equation for the named accumulator summary `rollingAcc`. |
| 58–60 | `rule-4988a36c4820a41daeb7519719fcab344fb535b61db16dcb9890a7570791b1bd` | `DEFINITION` | Structurally recursive equation for `rollingAcc`; consumes one `IntSeq` constructor. |
| 65 | `rule-49d35612d63bf56fdd624a16c30b97a62ddbf196c0acb5a07976bc8b31be1a41` | `DOMAIN_LEMMA` | Sequence-independent shortcut `firstAfter(IS,false) = false`. It follows by the empty/nonempty structural cases below, but `prove.sh` compiles it into `VERIFICATION` before the only `kprove` run; Stage 1 never first proves this exact rule in a module omitting it. It therefore cannot be `PROVED_DERIVED_LEMMA`, and it is a redundant theorem rather than a structural defining case. |
| 66 | `rule-21e311b677245a3588f3fdf17486b6433041519d4dfc2db17823ead5b4f5000c` | `DEFINITION` | Empty base equation `firstAfter(.IntSeq,F) = F`. |
| 67 | `rule-47cd64e11bfe4d5400e0c8493531f3dfdc997241fb44f11ac0ea1a85b059fbc3` | `DEFINITION` | Nonempty structural equation: executing at least one iteration clears the first-element flag. |
| 70 | `rule-c78b46c124c162a2ce4be242da78ad71608ea739808b453e38a3d06dda083403` | `DEFINITION` | Empty base equation for final-maximum summary `maximumAfter`. |
| 71–72 | `rule-a717a58b1e928e5a992ae9697da1d2e92f5cd196dea1d865d7d01c1e95feb44f` | `DEFINITION` | Structurally recursive final-maximum equation. |
| 75 | `rule-10994d65e9ac31b3b7356400325c3cd65b9fdc2215f9251d061e05ef206dd524` | `DEFINITION` | Empty base equation for final loop-variable summary `numberAfter`. |
| 76 | `rule-68d75551ff66412917fa7bf8014d718e942c5b72b9c02eaf2ccd715cb817f649` | `DEFINITION` | Structurally recursive final loop-variable equation. |

Independent counts: 15 `DEFINITION`, 2 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`.

The domain lemma is relevant. The source loop initializes `first = true` and
sets it to `false` on the first iteration; the Stage 1 loop claim records the
final binding as `firstAfter(INPUT,FIRST)`. After one symbolic head, the
recursive invariant must reason about `firstAfter(REST,false)`. The shortcut
states exactly that loop fact for arbitrary remaining input, and the end-to-end
claim uses the loop claim to establish the source function's result.

The lemma is mathematically valid under the two structural defining equations:

- empty input: `firstAfter(.IntSeq,false) = false`;
- nonempty input: `firstAfter(iCons(I,R),false) = false`.

It overlaps those cases consistently and makes no claim unrelated to
`rolling_max`.
