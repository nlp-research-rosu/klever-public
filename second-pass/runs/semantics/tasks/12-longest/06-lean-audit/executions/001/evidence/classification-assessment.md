# Independent Stage 3 classification assessment

Frozen verification module closure: `VERIFICATION` only.

| Frozen source span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| `verification.k:12` | `rule-61a7e85b99e1fd517b3f029cca636566b11a786aa2f24d053db8e5dea4317820` | `DEFINITION` | Base equation for the structural embedding `stringVals`; it names the empty embedded value sequence. |
| `verification.k:13-14` | `rule-06cf824ccd2247d57e4141172b5e6494e4acc57dc1a88a94144097b09d59b0c1` | `DEFINITION` | Constructor equation for the structural embedding `stringVals`; it maps the head string and recurs on the tail. |
| `verification.k:18-19` | `rule-285b45564f2d7dce460b69dbde1ea9178bdc2bd530970d2320373eaba6467c80` | `OPERATIONAL_RULE` | Ordinary iterator observation for an empty embedded list. After the `stringVals` base equation, it is exactly the supplied `MPY-LIST` rule `#iterNext(list(.ValSeq)) => #iterDone`, with no additional state effect. |
| `verification.k:20-22` | `rule-55d56cc27c981347c574d1ce91485262c24edb072a6b353a25dac39dfaa97e32` | `OPERATIONAL_RULE` | Ordinary iterator observation for a nonempty embedded list. After the `stringVals` constructor equation, it is exactly the supplied `MPY-LIST` rule yielding the head and residual list, with no additional state effect. |
| `verification.k:27` | `rule-f40c65506711d9264ce5e002c00c58e14bffb284ba0a0ef1e062022c850058fa` | `DEFINITION` | Base equation for the named mathematical fold `longestAcc`. |
| `verification.k:28-29` | `rule-4344ff90b2feb479d11bd8ad23e5a852fa65b2184ee2ab2a22a60b8b24b7a9ba` | `DEFINITION` | Initialization equation for the `longestAcc` recurrence when the accumulator is `noneV`. |
| `verification.k:30-32` | `rule-0f388914c90471f2074c0ae8359e3fa11b9f73200e404e8cded4c53936bcd932` | `DEFINITION` | Recursive `longestAcc` equation for a strictly longer head. |
| `verification.k:33-35` | `rule-370c2d5a71b42f964c5e0bc4fde658a3d2f206ee26b68793283aebc5d57f27f9` | `DEFINITION` | Recursive `longestAcc` equation for a shorter or tied head, preserving first-on-tie behavior. Together with the strict case, the integer guards are disjoint and exhaustive. |
| `verification.k:40-57` | `rule-1b6d53d96f4b4a82eb6b7f9bafc5577f204500d0110e04dbb065f0e26a91bc18` | `DEFINITION` | Macro expansion of the named proof term `longestSolution` to the translated program closure. |

Independent totals: 7 `DEFINITION`, 2 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 0 `DOMAIN_LEMMA`.

The two iterator rules are execution/observation rules, not mathematical
implications. The four `longestAcc` equations are a named structurally
recursive summary definition, not facts asserted about a pre-existing
function. The macro is a named proof-term expansion. None is first proved in
a module omitting that exact rule and then reused: `prove.sh` compiles
`verification.k` containing all nine rules before proving only the claims in
`spec.k`. No inventory rule can therefore qualify as
`PROVED_DERIVED_LEMMA`.

There are no `simplification` attributes in the reconstructed inventory.
The protected Stage 3 classifications agree entry-for-entry and in canonical
order with this independent assessment.
