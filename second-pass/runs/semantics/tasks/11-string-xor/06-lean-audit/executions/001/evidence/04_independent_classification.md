# Independent Stage 3 classification

Frozen source: `/reference/k-proof/verification.k`

Local verification-module closure reconstructed by the trusted inventory tool:
`STRING-XOR-VERIFICATION` only. The imported `MPY` module is defined in the
required supplied-semantics files, not locally in `verification.k`, so it is
outside this local lexical closure.

Every one of the 19 inventoried rules is independently classified as
`DEFINITION`. No rule is an execution/observation rule over a configuration,
no rule asserts a property of an already-defined mathematical operation, and
no rule was first proved in a module omitting it and later installed for use.

| # | Source rule ID | Span | Independent class | Reason and operational relevance |
|---:|---|---:|---|---|
| 1 | `rule-199ce5880ece2ffb12808eff7fef493bd984e1a076cd0e8d4b343706610da6dd` | 9 | `DEFINITION` | Introduces the fresh `binaryCode` predicate as exactly ASCII code 48 or 49. It supplies the input-domain predicate used by the claims. |
| 2 | `rule-a148568eb04c7f9b8870ff300eaedf75c27d7157f87329038363c581ba31e006` | 12–13 | `DEFINITION` | Equal-input guarded equation for the fresh `xorCode` summary, returning code 48 (`"0"`). |
| 3 | `rule-fe604a49861f69b3d97a975621261928274be9ca20eacdb377de3f12c4cd20be` | 14–15 | `DEFINITION` | Unequal-input guarded equation for `xorCode`, returning code 49 (`"1"`). On binary inputs its guard is disjoint from rule 2 and the pair is exhaustive. |
| 4 | `rule-62aca2024c4118a16e877ed708bc7768249c5c00041d1b722b67419785a42cb7` | 18 | `DEFINITION` | First-empty base equation for the fresh accumulator summary `xorAcc`; zip must stop and preserve the accumulated prefix. |
| 5 | `rule-3873758979b4fe1f32c7b6c9f3766c8a77b9e2692da5dd9a167d7ec6ed480a65` | 19 | `DEFINITION` | Second-empty base equation for `xorAcc`; this is the other zip-truncation case. It does not overlap rule 4 because its first remainder is nonempty. |
| 6 | `rule-5927925fd64b560eda4a130550ad28115a8190603ec3ef402ce86fd2e7f16246` | 20–21 | `DEFINITION` | Structural recursive equation for `xorAcc`: append one `xorCode` result and descend on both tails. This is the output summary in the postcondition. |
| 7 | `rule-b95fbff73db146c39988a02bbcbb098c77c0429f2871f9f6ce9412cd30eb2a41` | 25 | `DEFINITION` | Empty base equation for the fresh `binaryCodes` predicate. |
| 8 | `rule-0a4b0a280fe4a4a35fd65b3556363daab4e64279cb451ed33f6978a946f2f288` | 26–27 | `DEFINITION` | Structural recurrence for `binaryCodes`; it checks the head with `binaryCode` and descends on the tail. |
| 9 | `rule-51eed43ea34ea2b88fc0ee347ba2ce190ad10bf7d39e47c22ce25b918d176bd8` | 33 | `DEFINITION` | First-empty base equation for the fresh loop-state summary `xorLastX`; an empty iteration retains the prior `x`. |
| 10 | `rule-a38734cd4f874be55b9ca33cb03b46d5c734929e291f977a284b556b320c7a24` | 34 | `DEFINITION` | Second-empty base equation for `xorLastX`; zip stops and retains the prior `x`. |
| 11 | `rule-7fbbae800178ce2c9ba1863b427c2174c299cc3ade1339dce972aa9f67e5e909` | 35–36 | `DEFINITION` | Structural recurrence for `xorLastX`, recording the current head of the first iterable and descending on both tails. |
| 12 | `rule-7f5cb64a2e98293475868861131ad7741bf1e6a094fbf0ee0640e2a0798bb97b` | 37 | `DEFINITION` | First-empty base equation for the fresh loop-state summary `xorLastY`; zip stops and retains prior `y`. |
| 13 | `rule-27fb8fe751825dffe32c8718d119f49236783d0d07bcd8a5db653b1dea712d16` | 38 | `DEFINITION` | Second-empty base equation for `xorLastY`; zip stops and retains prior `y`. |
| 14 | `rule-0c567126c3b88db4eaddf41bd503995b9c2bb3ac347550f17551712ad2763a7b` | 39–40 | `DEFINITION` | Structural recurrence for `xorLastY`, recording the current head of the second iterable and descending on both tails. |
| 15 | `rule-b29ef2baa281c5fa26870dd0bdec73534d8ce1dfb5f50b7530fc079eb66befb8` | 44 | `DEFINITION` | Expands the fresh named proof term `stringXorTarget` to the exact tuple-binding target emitted for `for x, y`. |
| 16 | `rule-fb6d7f05a768ed8021b86cfe5116ba4f3a3285bc89b5cb1b77d93545fe5b3e63` | 47–50 | `DEFINITION` | Expands the fresh named proof term `stringXorLoopBody` to the exact equality branch and string-concatenation body. |
| 17 | `rule-9038158948b425b3a65b4356422181488831c1971604f53f17abfdf852273664` | 53–60 | `DEFINITION` | Expands `stringXorBody` to the exact translated function body, including initial `result`, `x`, and `y`, zip iteration, and return. |
| 18 | `rule-7ca33bffe28bd24537015e6017062942fea10d0e7b29d0e6493564505573088b` | 63–64 | `DEFINITION` | Defines the fresh named closure value with exact parameters, body, and defining scope. |
| 19 | `rule-ddfff0b94e57e746b0fc84a9f6b2e7f71e126aed256bc39b9680c789117a7846` | 67–70 | `DEFINITION` | Expands the fresh named module term to the translated import and function definition. |

The inventory records an empty attribute list for every entry. In particular,
there are no `[simplification]` rules to classify.

Operational cross-check:

- Supplied `zip` semantics produces paired one-character strings and stops
  when either sequence is empty (`builtins.k` 162–174).
- The loop binds the tuple, evaluates the body, and recurs on the remaining
  zip object (`controls.k` 62–74 and `tuple.k` 30–57).
- String equality compares code sequences and string `+` concatenates them
  (`str.k` 19–26); the `if` chooses the corresponding branch
  (`controls.k` 50–54).
- These rules yield exactly the `xorAcc`, `xorLastX`, and `xorLastY`
  recurrences above. The operational witness suite covers empty inputs,
  both equality branches, both unequal-length directions, longer inputs, and
  observable final `x`/`y`; all pass. A branch-mutated counterfactual is
  rejected with `AssertionError` and exit code 1.

Conclusion: the independently reconstructed true `DOMAIN_LEMMA` set is empty.
