# Independent Stage 3 classification

Frozen source: `/reference/k-proof/verification.k`, local closure selected by the trusted inventory code: module `VERIFICATION` only.

| # | Source span | `source_rule_id` | Independent class | Judgment |
|---:|---|---|---|---|
| 1 | 8–26 | `rule-23c2b487a0d8f29700e6ac4089fe525ffc9c872931fc8c2f43167977faff2b4a` | `DEFINITION` | Expands the named `Stmts` proof term `evenOddBody` to the exact translated function body; it matches no configuration cell. |
| 2 | 29 | `rule-2310190f9336d3807b3f0a9541b7575ee65338e32de301a678715767e85bcc90` | `DEFINITION` | Defines the named closure proof term from the parameter, body, and parent scope. |
| 3 | 39 | `rule-4d91b8b2c3d8954a2c376e8dff3c8ce44249a4bc613bfcac28a37aac6cb252f2` | `DEFINITION` | Base equation `evenPos(0) = 0`. |
| 4 | 40 | `rule-0721755b2e82fbb486e3f764bcea50657b9308215644bd93a0c614a14803ab02` | `DEFINITION` | Base equation `oddPos(0) = 0`. |
| 5 | 41 | `rule-ef45f1edf85562d1c3e7ca8657f4b35a5876fb08b17a1a7361b02e1d499ca001` | `DEFINITION` | Guarded symbolic form of the same `evenPos(0)` defining equation; its `simplification` attribute is permitted. |
| 6 | 42 | `rule-039beca211ce6b817aac64ca6bf2feac799b0609c7717fd19e4c10cd73dedf18` | `DEFINITION` | Guarded symbolic form of the same `oddPos(0)` defining equation; its `simplification` attribute is permitted. |
| 7 | 45 | `rule-ba793812532883dfdd8d12cb3946f3305f2ff4a6f0a33ad45d8432118c01ff61` | `DEFINITION` | Totalizes `evenPos` on negative arguments by positive magnitude. |
| 8 | 46 | `rule-51300200ac378272fdf4ff0484cbe9079d9978ae2265e209ce1ae2a624cf98a4` | `DEFINITION` | Totalizes `oddPos` on negative arguments by positive magnitude. |
| 9 | 48 | `rule-a07409cfab312e5dbd4ee7e30648f2d4d2e1788669ff389374802027d8737625` | `DEFINITION` | Defines the public special zero result `decEven(0) = 1`. |
| 10 | 49 | `rule-e6a79a4a24ead81deda4a678a4dc45107b24438ee3322bbdf89d25709439c289` | `DEFINITION` | Defines positive `decEven` through `evenPos`. |
| 11 | 50 | `rule-419675d8cedf38aadb7832913fedc30a1d02a5024494ef2823781b30327b5a13` | `DEFINITION` | Defines negative `decEven` through the positive magnitude. |
| 12 | 52 | `rule-14199729c393d801ede96d8f3a1ee81b9fc4f97e85e61f60c9e346717c6c093c` | `DEFINITION` | Defines the public special zero result `decOdd(0) = 0`. |
| 13 | 53 | `rule-ad936706b62967bc0e29477f3bb5c5dff0fe51e7a3436de91434f872798381ab` | `DEFINITION` | Defines positive `decOdd` through `oddPos`. |
| 14 | 54 | `rule-5f5cc5d965ac0619ed07821b496cf1ab1eca1e70caa4573a0a44b08f683b3667` | `DEFINITION` | Defines negative `decOdd` through the positive magnitude. |
| 15 | 57–59 | `rule-bf2f17042baead9b767eb8154375d9748d18a100e17da03642a77cfe406ce383` | `DOMAIN_LEMMA` | Proposition-level zero-case equality for the externally visible even result; it is not first proved in a module omitting itself. |
| 16 | 60–62 | `rule-b844cb11342eaa449e577cd7e74b99d3283bacf3b169e29c94235f1c7edc1748` | `DOMAIN_LEMMA` | Proposition-level zero-case equality for the externally visible odd result; it is not first proved in a module omitting itself. |
| 17 | 63–65 | `rule-2f7142f79fcc9e619c4580decceb38a73bb3716819a71c7503d94cb1dc77b79c` | `DOMAIN_LEMMA` | Positive-magnitude normalization `evenPos(abs(N)) = decEven(N)`, admitted as a proposition simplifier. |
| 18 | 66–68 | `rule-2a60622c3bbfa43590a66aa9e80b161f0edcd18ff09827cc120a8dec01c2e0b6` | `DOMAIN_LEMMA` | Reverse orientation of the preceding admitted equality. |
| 19 | 69–71 | `rule-61db74cde356f6655a9b1b0684b4d8bce65291a3f9cd8deb327f942ea6a7d071` | `DOMAIN_LEMMA` | Positive-magnitude normalization `oddPos(abs(N)) = decOdd(N)`, admitted as a proposition simplifier. |
| 20 | 72–74 | `rule-0f9ee7597728fa7f27d3d9ad4a8f4339e78c38563b31dbb6199eea9aa11d82ec` | `DOMAIN_LEMMA` | Reverse orientation of the preceding admitted equality. |
| 21 | 78–83 | `rule-5a0a2cc7a4d444f988e3cebb6dc26aebd6f8dde901db6bda39bde915d219c1cb` | `DOMAIN_LEMMA` | Forward accumulated even-count decimal recurrence; it directly supplies mathematics needed at the loop circularity. |
| 22 | 84–89 | `rule-72eaeaa9cbb5d008fe6415d81db969a48965568d1278c34ae925816b5e85b44f` | `DOMAIN_LEMMA` | Reverse orientation of the same accumulated even-count recurrence. |
| 23 | 90–95 | `rule-316f5e2aa29d4aa0e25b0c2870a62f8dbc956a33e3070de5c80aafba74e0893d` | `DOMAIN_LEMMA` | Forward accumulated odd-count decimal recurrence. |
| 24 | 96–101 | `rule-e0dab4a9b20997030cfca78b7b30e2b46b8e7ec4b5649685518b6d53684edc98` | `DOMAIN_LEMMA` | Reverse orientation of the same accumulated odd-count recurrence. |

Counts: 14 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0 `PROVED_DERIVED_LEMMA`, 10 `DOMAIN_LEMMA`.

Every `simplification` rule is independently classified as either `DEFINITION` (rules 5–6) or `DOMAIN_LEMMA` (rules 15–24). None of rules 15–24 qualifies as `PROVED_DERIVED_LEMMA`: Stage 1 compiles `verification.k` containing them before proving the loop claim, and does not first prove any exact same rule in a module that omits it. The separately proved loop-tail claim and its later operational use occur in `spec.k` and `verification-with-lemma.k`, outside the frozen local inventory.

All ten domain lemmas are relevant. Rules 15–16 are the source program's `num == 0` result, rules 17–20 connect the postcondition summaries across the source program's `abs` operation, and rules 21–24 are exactly the parity update and decimal `/ 10` step used by the source loop and loop invariant.
