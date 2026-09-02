# Independent rule classification

Frozen source: `/reference/k-proof/verification.k`, whose SHA-256 is
`ff40adf397cc707c4b5426c16572837e23a14834b93aafbbc134c51c45402bd5`.
The local verification-module closure reconstructed by the trusted inventory
contains only `VERIFICATION`.

| # | Source span and identity | Independent class | Source/semantics judgment |
|---:|---|---|---|
| 1 | 9–14, `rule-db9420e8fd1c4626595b79b7ea2e6307a53b03fc99d9a63570388395764ad474` | `DEFINITION` | Macro expansion of the named `longestLoopBody` proof term. It is the exact translated loop-body AST: compare `len(string) > len(result)`, conditionally assign `result := string`, then stop. |
| 2 | 17–27, `rule-79576cfe9c9b959c7fa701acac35d9e135e225f3fdeb54b5effd615e4a16a951` | `DEFINITION` | Macro expansion of the named `longestProgram` proof term. It matches `solution.mpy`: empty test and `None`, first-element seed, loop, return. |
| 3 | 33, `rule-cf8b57d453a6eeb1d815ece37d5946c5fead470f5c67daf85939a3638bd36896` | `DEFINITION` | Defines the `stringList` representation wrapper from mathematical `Strings` to runtime `listVal`. |
| 4 | 34, `rule-7f473637b44742359337a6ea4b8811bbced9fc57f43365394878fa092f0337db` | `DEFINITION` | Base equation of the named structural conversion `stringValues`. |
| 5 | 35–36, `rule-0eb9fd5516c5c09a4385fa1fb3ce068e72e602071ec62aa60e1aca23a6648342` | `DEFINITION` | Recursive equation of `stringValues`; maps each K string to `strVal`. |
| 6 | 43, `rule-d522a0d2a80d77bf23fff3789a4c9cc1dee3902e31f1443c813bc6cbc8bd5e20` | `DEFINITION` | Empty case of the named contract summary `expectedLongest`. |
| 7 | 44–45, `rule-0632983b57909c5400dca4ed74248b5d09a3914a9a277a31c21c50ec82e29e7f` | `DEFINITION` | Nonempty case of `expectedLongest`, seeded with the first string. |
| 8 | 47, `rule-bb0ed98a5e6ea08b1f41e028d4ab4f62da3a797dbe6f3b3a6b0fb0b0be94ec3b` | `DEFINITION` | Base equation of the named fold `firstLongest`. |
| 9 | 48–50, `rule-e2ea59e583e9aba4f56686bbb8c31703b58b4e536d869f118bf4f3f066a4c42b` | `DEFINITION` | Strictly-longer recurrence of `firstLongest`; the candidate is replaced. |
| 10 | 51–53, `rule-41608496e24b276d61c515e55ec432cae88d14f9e1bdb34b9983811ac7afe643` | `DEFINITION` | Complementary recurrence of `firstLongest`; the existing candidate is retained, including ties. |
| 11 | 60–61, `rule-b0f0333a8289ed42bf63f5f68911b09e710cd5d1f3945ffceead604fd31c6755` | `OPERATIONAL_RULE` | Runtime observation rule for `isEmpty(seqVal(..., N))` at `N = 0`, paralleling `isEmpty(listVal(.Values))` in `semantic.k`. |
| 12 | 62–63, `rule-e69efc7581406d022b7856deb7b0903c7ce4f89a28c7ba8668b210fa8eeb1f44` | `OPERATIONAL_RULE` | Runtime observation rule for positive-length symbolic sequences, paralleling nonempty `listVal`. |
| 13 | 64–65, `rule-b1717a1cb9f20abb2c92ed3d8bb9f5dfc66a3f417779b528e3fcddc52cf5e014` | `OPERATIONAL_RULE` | Runtime head observation on nonempty `seqVal`, returning the indexed runtime string value; it specializes the `head` operation used by subscript evaluation. |
| 14 | 67–68, `rule-f224022b33a01068dbf84152f03ad2c24f192cea0b778266eb7958ce3e3c07ca` | `OPERATIONAL_RULE` | Ordinary loop-termination rule for zero remaining symbolic elements, corresponding to `forValues(_, listVal(.Values), _) => .`. |
| 15 | 69–74, `rule-6217bfa50b953d6505f0f15ac2a66ceb8481b6397d4eea8a5ca19a91b3cef5da` | `OPERATIONAL_RULE` | Ordinary loop-step rule: bind the current element, execute the body, then advance index and decrement remaining length. This mirrors the concrete `listVal(V, VS)` iteration rule cell-for-cell for the symbolic representation; it is not an equation about a mathematical theorem. |
| 16 | 78–79, `rule-e4633a59660c5ec7ead77cb473c04e9f0d1cdbe206f021fdb481ce4081ba04f7` | `DEFINITION` | Zero-remaining base equation of the named invariant/postcondition fold `firstInSeq`. |
| 17 | 80–83, `rule-64119d60105d2cb544dd81225851d868a9c84ab75c122076ae4a088d7f4cf1ab` | `DEFINITION` | Strictly-longer recurrence of `firstInSeq`, with structural descent `N ↦ N - 1`. |
| 18 | 84–87, `rule-2c6384deca5d2eff6d3d334e4b29720ab4673a16bc8a4f57ad4341881f7e6cc3` | `DEFINITION` | Complementary recurrence of `firstInSeq`, retaining the old candidate on shorter or equal strings. |

The independently reconstructed attributes list is empty for all 18 entries,
so there is no `simplification` rule to reclassify. The 13 definition rules
all define macros, representation conversions, contract summaries, or named
recurrences. The five operational rules observe or execute the new `seqVal`
runtime representation through existing semantic operations (`isEmpty`,
`head`, and `forValues`).

There is no `PROVED_DERIVED_LEMMA`. `prove.sh` first compiles
`verification.k` with every listed rule already present, then makes one
`kprove spec.k` call. It never proves an exact listed rule against a module
from which that rule has been removed and then reuses it later.

There is no `DOMAIN_LEMMA`. This is not a conclusion from the Stage 3 label:
each rule has the definitional or operational role described above. Every
summary is tied to the source contract (empty input, first maximum, string-list
representation) or to the actual invariant/postcondition, and every
operational rule is tied to the symbolic-sequence execution used by the frozen
program proof.

Counterfactual sensitivity is visible directly in the equations. Replacing
strict `>` by `>=` in either loop macro or fold changes the required
first-on-tie result. Replacing `stringAt(ID, I)` with a constant changes head
observation and the loop binding. Failing to increment `I` or decrement `N`
changes iteration. These are substantive source/operational meanings, not
vacuous logical conjuncts.
