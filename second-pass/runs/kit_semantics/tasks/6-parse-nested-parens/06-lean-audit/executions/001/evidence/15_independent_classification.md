# Independent Stage 3 classification

The local verification-module closure is the single locally declared module
`VERIFICATION`.  The `MPY` import is supplied semantics, not another module
declared in `verification.k`.  I classified the 37 reconstructed rules below
from their frozen text and the supplied operational semantics, without using
the protected manifest's rationales.

| # | Source rule ID | Span | Independent class | Independent reason |
|---:|---|---:|---|---|
| 1 | `rule-5726f243d32eab9074cd938bb708721974e6f93403b9a81b84c8bafb2e0aba1f` | 8–19 | `DEFINITION` | Nullary macro equation naming the exact loop-body AST. It neither matches a runtime cell nor states a result fact. |
| 2 | `rule-a8c8a92bbe087be04a1b87bd4672ecf4e852861eb514c5861fc6c421da89ecb0` | 22–26 | `DEFINITION` | Nullary macro equation naming the exact post-loop AST. |
| 3 | `rule-b733d820579460b3aa0111391c4c0eb0ee7990558a6a12bbb15a89e2738dc088` | 29–35 | `DEFINITION` | Nullary macro equation composing initialization, the loop macro, and the post-loop macro into the function body. |
| 4 | `rule-39ad3e2c71f593e07645aad99e6f755ba03f98a8150b5b6883e8c3f0ecd0908d` | 38–41 | `DEFINITION` | Nullary macro equation naming the module AST and its function definition. |
| 5 | `rule-de3d2682d4fa9b72a1a9e67bbe4efd8a5104012a1f324db6711e8f0be65f3507` | 48–49 | `DEFINITION` | Guarded equation for the opening-parenthesis branch of the `nextDepth` summary. |
| 6 | `rule-76482713092a898c39db87d936ae2d6961af869ec96bafbe21dd7d7021b68c9e` | 50–51 | `DEFINITION` | Guarded equation for the closing-parenthesis branch of `nextDepth`. |
| 7 | `rule-397efc7aa5616f5d60a2ca3632114571c441d4bc6519f5e3ef56304e211ae399` | 52–53 | `DEFINITION` | Complementary guarded equation completing `nextDepth` on non-parenthesis codes. |
| 8 | `rule-12fd5d20d629decc9577e815753dc149cb3435deb694554cd8f0ae5f6a68eee2` | 55 | `DEFINITION` | Empty-sequence base equation for the structurally recursive `scanDepth` summary. |
| 9 | `rule-2e532b0c5f055c499e41a9372af3ee64f57fefd5f0eb665e0952de62a78289a7` | 56 | `DEFINITION` | Cons recurrence for `scanDepth`; it consumes the head and recurs on the tail. |
| 10 | `rule-8b700c4be9fb81b4c76bb416aa0509416c66be815dcf8247d0253d15b939dba1` | 60–61 | `DEFINITION` | First guarded case of the `openDeepest` max-update helper. |
| 11 | `rule-95a58ede21449df024f6bbced9c53aebf75bea00dd402d21ca41a54e8787608c` | 62–63 | `DEFINITION` | Complementary guarded case of the `openDeepest` max-update helper. |
| 12 | `rule-269835c6a6ba9319a58cf01acc424396c06eda8eb23e3d603112f377283cffff` | 66–67 | `DEFINITION` | Positive case of the delimiter-reset helper `delimiterDeepest`. |
| 13 | `rule-db9d4d1e238794d91eb60b5eb6ab041eb7274cbbe2dfb1e33ae2aa8039336e2d` | 68–69 | `DEFINITION` | Complementary nonpositive case of `delimiterDeepest`. |
| 14 | `rule-26364381489aa9187954b1cf6f40d3087761c1c9fc29c28373a3fe9ff05c3693` | 72–73 | `DEFINITION` | Opening-parenthesis equation for the one-character `nextDeepest` summary transition. |
| 15 | `rule-c897db40052b40e52745f50e5f01ae38102075048b69da62cd12ee47e8239d91` | 74–75 | `DEFINITION` | Closing-parenthesis equation for `nextDeepest`. |
| 16 | `rule-97316e0eb91a90f2f2e33a75ff93f859a3c959be2c7fe0693d777755386bf4d0` | 76–77 | `DEFINITION` | Complementary delimiter equation completing `nextDeepest`. |
| 17 | `rule-aa55996290827dd7dc7b74d76be6e6ffba4687f816f744a26ac719a500fbd77b` | 79 | `DEFINITION` | Empty-sequence base equation for `scanDeepest`. |
| 18 | `rule-0cc36cded93d4a7b10b00bfa1bd9c2baad33b7184497d3a984fab90c602ba97b` | 80–81 | `DEFINITION` | Tail-decreasing recurrence for `scanDeepest`, parameterized by current depth and maximum. |
| 19 | `rule-b54d51a9437c8867e237458bc937023e94bb9b378f344e9de1710c5f3d67f213` | 85–86 | `DEFINITION` | Positive case of `delimiterOutput`, defining append-to-accumulator behavior. |
| 20 | `rule-2da3145f080f7220ae735fb312fe40d2b95345238e06730aaee472c46288977a` | 87–88 | `DEFINITION` | Complementary nonpositive case of `delimiterOutput`. |
| 21 | `rule-2d3a6a4d80d3c698face502b519e54365b366da2c256a682d07c243195f072a6` | 91–92 | `DEFINITION` | Opening-parenthesis transition equation for the output accumulator. |
| 22 | `rule-74e506885dda6f0b5f2552dc5f5840ad06c7347c49504c6225f151c07d1f1ff0` | 93–94 | `DEFINITION` | Closing-parenthesis transition equation for the output accumulator. |
| 23 | `rule-ebdaec1ca60a4e8c2264edbee49639fdd62cfc0aa06e6395291da8bd016380c8` | 95–96 | `DEFINITION` | Complementary delimiter transition equation completing `nextOutput`. |
| 24 | `rule-7f5f95627027f06d8ff36996df5d6a264985a1338c1eafb5264a7014f82977b5` | 98 | `DEFINITION` | Empty-sequence base equation for `scanOutput`. |
| 25 | `rule-0d88b06fec397ceb4cdcedf1835e834822b52b817e61eac4e1572b5a456cb706` | 99–101 | `DEFINITION` | Tail-decreasing recurrence for `scanOutput`, threading depth, maximum, and output state. |
| 26 | `rule-bb95e2fadf8bf67cee1f000040bda885cbed1fc4aa6012fa1ad87f9ee93ac437` | 104 | `DEFINITION` | Empty-sequence base equation for the loop-variable summary `scanChar`. |
| 27 | `rule-40e75b4bf4b1fffabe18b338838c26299293a6a139cd25dec7921bc7a304c88f` | 105 | `DEFINITION` | Tail-decreasing recurrence recording the current one-character string in `scanChar`. |
| 28 | `rule-4055b50fbb470df4941a4d811be8147604bac1ebb76a089c89440771f00666fd` | 108–111 | `DEFINITION` | Positive guarded equation for the post-loop `finishOutput` helper. |
| 29 | `rule-a8bced5805605ba802558f2a30f58e2bbeb06e79e9e56afadb36ff394a68e86c` | 112–113 | `DEFINITION` | Complementary nonpositive equation completing `finishOutput`. |
| 30 | `rule-0a12b1ada34df54813713aa46e76132f43ec986c3fd7b81fbde5f37ec2148dbd` | 116 | `DEFINITION` | Wrapper equation defining `expectedDepths` as `finishOutput` with the source program’s initial state. It names the postcondition summary but does not assert its equality to execution. |
| 31 | `rule-18b6e3869e8f0490d1505f93448fdc097c0b6af70d8c9936bffa5c8c11da7591` | 123–124 | `DEFINITION` | Opening-parenthesis transition equation of the recursive input-domain predicate. |
| 32 | `rule-1b76a6ef163277cd26ec8b14211519ddff167c0043a09aae3552e4171d523ac6` | 125–126 | `DEFINITION` | Closing-parenthesis transition equation of that predicate, explicitly requiring positive prior depth. |
| 33 | `rule-d98d2e6e9a277120c34fa3fb0732cd16f792d4cf3022c8a8f56db674538d1534` | 127–128 | `DEFINITION` | ASCII-space transition equation of the predicate, requiring group-boundary depth zero. |
| 34 | `rule-a4ea4395372d8c70559f7557daef5a460acc9b80b121b715709843e51372357f` | 129–130 | `DEFINITION` | Complementary equation making all other character codes invalid. |
| 35 | `rule-8d161c9f8e3083e9c2153ad64d2c7055cb08b85afb5919e24efa8b759d63e790` | 132 | `DEFINITION` | Empty-sequence base equation for `wellFormed`. |
| 36 | `rule-327c993b765903236ca6a085116085ac6e3a9c58295324c782e00315b2e2be18` | 133 | `DEFINITION` | Tail-decreasing recurrence dispatching `wellFormed` through `wellFormedStep`. |
| 37 | `rule-db73acc81a02eefe944dca08c79b2658d7015d61bf682b4bc807e23265b90755` | 136 | `DEFINITION` | Wrapper equation defining `validInput` by initializing `wellFormed` at depth zero. |

## Classification judgment

- All 37 entries are genuine named macros, helpers, base equations, guarded
  cases, or structural recurrences.  The recurrence equations consume an
  `IntSeq` tail, and each guarded family is exhaustive with disjoint guards.
- None is an ordinary execution/observation rule: none rewrites a `<k>` cell or
  another runtime configuration cell.  The actual execution rules for
  iteration, assignment, branching, string iteration, list allocation, and
  append remain in the supplied `MPY` semantics.
- None is a derived theorem.  The rules do not assert a cross-symbol equality
  between fixed execution and a postcondition; that connection is made by the
  Stage 1 reachability claims in `spec.k`.
- None is a `DOMAIN_LEMMA`.  In particular, `expectedDepths` and `validInput`
  name the theorem’s output summary and precondition respectively, while their
  equations define those terms structurally.  They do not assume that program
  execution returns `expectedDepths`; the target claim must establish that.
- No inventory entry has a `simplification` attribute, so the special
  simplification-category constraint is vacuous.

The independent classification therefore matches the protected manifest:
37 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0 `PROVED_DERIVED_LEMMA`, and
0 `DOMAIN_LEMMA`.
