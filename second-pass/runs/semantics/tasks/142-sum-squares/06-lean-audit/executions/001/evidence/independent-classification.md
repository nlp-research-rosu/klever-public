# Independent rule classification

The canonical local verification-module closure is the single module
`SUM-SQUARES-VERIFICATION`. It contains 13 rules. The classifications below
were made from the frozen rule text, `solution.py`/`solution.mpy`, `spec.k`, and
the supplied operational semantics; Stage 2's classification was not used as
authority.

| Lines | Source rule ID | Independent class | Reason |
|---:|---|---|---|
| 15–16 | `rule-fb1cdb3a89c33afefb0a0c5b0a47e951912ef197bd45509a577efe372d682002` | `OPERATIONAL_RULE` | Empty `intVals` list observation: `#iterNext` produces `#iterDone`, exactly paralleling the supplied list iterator's empty case. |
| 17–19 | `rule-823fe844036b54e6e8472a5d0431256fc8ae8a77598a45750268365ac4dac4ed` | `OPERATIONAL_RULE` | Nonempty `intVals` list observation: yields the head and residual iterator, exactly paralleling the supplied list iterator's `vCons` case. |
| 24–25 | `rule-63536b6587c994802960586db08f679291258f0748f2e10f19a923fd3350c931` | `DEFINITION` | First guarded equation of the newly named `contribution` summary: square when the index is divisible by 3. |
| 26–27 | `rule-15e02f60b07bb5c87cf993fd87f405403d7b7f04ae6caf632ad9b88aa47705ca` | `DEFINITION` | Second guarded equation of `contribution`: cube when not divisible by 3 but divisible by 4. |
| 28–29 | `rule-92f9fa4d6e57713f793a9366d28a846d3d56d0e604cf2a2b5d6330dc51a58cdd` | `DEFINITION` | Final guarded equation of `contribution`: identity when neither earlier branch applies. |
| 33 | `rule-bf31de50897e710924d8fbb882c66865ce2e9543687d31159334ebae048c4670` | `DEFINITION` | Base equation of the newly named tail-recursive `sumSquares` summary. |
| 34–35 | `rule-10a0ae512e11a118d8100b15240076e0cd7f15f7a1fb32d4ebac572c70a7349d` | `DEFINITION` | Structurally descending recurrence for `sumSquares`, matching one frozen loop iteration. |
| 39 | `rule-d51ac0c56e230a256920a1c271fb1f2f5cb9b79fb5c055069a90f36384fe719e` | `DEFINITION` | Base equation of the newly named loop-post-state summary `endIndex`. |
| 40–41 | `rule-138e642ec3a5dd016b07d44a4b0badc8bab34c5720dcb85de7374f6af9746d85` | `DEFINITION` | Structurally descending recurrence for `endIndex`, consuming one element and incrementing once. |
| 44 | `rule-8b938e3e87a8b1e82de418aa640185bf47a88ba96e537684a0455141f138c303` | `DEFINITION` | Base equation of the newly named loop-post-state summary `endValue`. |
| 45–46 | `rule-64e8575b1d93b44dff01d0b4bd0e1a1004da6fe2ba7f43c118e02af3af0d246c` | `DEFINITION` | Structurally descending recurrence for `endValue`, carrying the most recently bound element. |
| 49–75 | `rule-66b63cb7b5d01727a05f1463c8497314972338aa98a424002c36909e4a3978fb` | `DEFINITION` | Exact macro expansion of the named loop-body proof term; it reproduces the frozen translated branch and index-update AST. |
| 78–83 | `rule-38e6a28bd65f89b1992106811b8bd7c968c48ad1cb93c8813bc73137899776bc` | `DEFINITION` | Exact macro expansion of the named function-body proof term; it reproduces initialization, loop, and return. |

The three `contribution` guards are pairwise disjoint and exhaustive. The
recursive equations descend on `Ints`. The iterator rules only expose the
constructor cases of the symbolic `ValSeq` representation and preserve the
active continuation and all other cells via the `<k> ... </k>` frame.

No rule states a pre-existing arithmetic or list theorem. No rule was first
proved against a module excluding that exact rule and then used later. The
loop and body claims in `spec.k` are separately proved reachability claims, not
rules in this inventory. Therefore:

- `DEFINITION`: 11
- `OPERATIONAL_RULE`: 2
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
- rules with the `simplification` attribute: 0
