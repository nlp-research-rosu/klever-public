# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory SHA-256
`50b8fc17588e9a70110064bc0f0e52b0922b9ce7723689693ff446b7a2d52d25`.
It contains four rules, all in the local `VERIFICATION` module. Every inventory
rule is represented once and in canonical inventory order in
`trust-boundary.json`.

## Classifications

| Source rule ID | Classification | Reason |
|---|---|---|
| `rule-c93f82157c0edf66f39013c6c43f9942de4d4fdb03a65233bc92f11b525c2c62` | `DEFINITION` | Expands the named `getMaxTriplesBody` proof term into the translated MPY statement sequence. |
| `rule-6e1a3f1a867ffa5aac98437215b212d2acc24e46fb6c160c7eef1d20a27d3da2` | `DEFINITION` | Defines the `chooseThree` mathematical summary. |
| `rule-ed9df131f37e783d697605c42deebd79589fdb258ea41d40595b1e3bc625bc2e` | `DEFINITION` | Defines the `zeroResidues` population summary. |
| `rule-54b144e14a69f0c5714e7e1621ac7fbbcf27e44642f7d6a540aa852db23a3ef0` | `DEFINITION` | Defines `tripleCount` by composing the population summaries. |

`getMaxTriplesBody` is a named proof-term expansion, not an added execution
rule. The remaining three rules are equations defining mathematical summaries.
No canonical rule has the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` compiles `verification.k` with all four inventory rules
already present and only then runs `kprove` on `spec.k`. It does not first prove
the exact statement of any inventory rule against a module omitting that rule,
nor does it subsequently install such a rule. The three residue claims in
`spec.k` prove modular-arithmetic cases, but none is an exact reusable rule in
the canonical inventory. The `get-max-triples-correct` claim also consumes the
already compiled definitions rather than establishing one for later reuse.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact; all four are definitional equations or named-term
expansions.

The operational-rule set is also empty for this canonical local inventory.
Execution behavior comes from the supplied reference semantics and is not
listed among these four launcher-inventoried local verification rules.
