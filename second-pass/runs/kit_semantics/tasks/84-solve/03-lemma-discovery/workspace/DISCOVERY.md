# Trust-boundary discovery

The classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory. Its copied `inventory_sha256` is
`0d280d2436eed6d6d7b88857c60dfbe7ccf942ecf8cc442fa068cb3e4b47e6c2`,
and it contains 11 rules in module `VERIFICATION`.

## Classification summary

| Classification | Count | Rule set |
|---|---:|---|
| `DEFINITION` | 9 | `solutionModule`; both `decodeBin` equations; both `allBinDigits` equations; all three `canonicalBin` equations; `digitDomain` |
| `OPERATIONAL_RULE` | 0 | Empty |
| `PROVED_DERIVED_LEMMA` | 0 | Empty |
| `DOMAIN_LEMMA` | 2 | The guarded decimal-remainder and decimal-quotient simplification rules |

The domain-lemma set is **not empty**. It consists exactly of:

- `rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a`
- `rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d`

## Rule classification

`rule-dabe5596b9af337f8a3164e47c3cfc9c95ac77a7f0264e301a20c92506acca00`
is a `DEFINITION`: the equation expands the nullary `solutionModule` proof
term to the translated `Module(...)` AST. The fixed MPY semantics still loads
and executes that AST.

The two guarded arithmetic rules,
`rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a`
and
`rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d`,
are `DOMAIN_LEMMA`. Each rewrites an expression over built-in integer
operations and therefore contributes an additional mathematical fact rather
than defining a named summary. Both carry the `simplification` attribute, so
the requested classification policy permits only `DEFINITION` or
`DOMAIN_LEMMA`; their semantic role selects `DOMAIN_LEMMA`.

`rule-4919db5997cb25213b3ce98a76a6388b59df5563a22cfed932df4735a6ada343`
and
`rule-029a575b73486388e10fb475acdaa1c76ca37368761dae92ed2d68bb1867892f`
are the base and recursive equations of `decodeBin`. They are `DEFINITION`
because they define a mathematical decoding summary and the recursion descends
through the sequence tail.

`rule-f2aba656d92faee38fea90204e6da2354ebcd914af1f55350da58939351da8e7`
and
`rule-41b4ad77e7eb08d36e9936dfae668eb2aaabf4d1b688374fb8aa3dc01a172ded`
are the base and recursive equations of the structural `allBinDigits`
predicate. Both are `DEFINITION`.

`rule-aa7e0002a3407b5d4b867e2d6bc75311639f1ebc558615aef42627e335282198`,
`rule-5545f7cabeaaacdd260458c643ec6a2bf61709a3bd4df73bd5c83a82a0344b84`,
and
`rule-7475c26cae009c85998c0c5a72c4d4421a9a2f44657a413aca401a947f1e1b24`
are the canonical-zero, leading-one, and `owise` fallback equations of
`canonicalBin`. Together they form a structural predicate definition, so all
three are `DEFINITION`.

`rule-983c37ae659da6b7c7eb71a96580a3332dd4fa37b9eb2a0a0e5f23e7c4c2b339`
is a `DEFINITION`: it expands the named `digitDomain` predicate to the
constraints defining the symbolic decimal parameterization.

No canonical rule is an `OPERATIONAL_RULE`. Program execution is supplied by
the imported MPY semantics, while the locally inventoried `solutionModule`
equation only supplies the AST and the other local rules are definitions or
arithmetic facts.

## Separately proved derived lemmas and Stage 1 evidence

Stage 1 separately proved four bridge-free derived claims in
`/reference/k-proof/bridge-spec.k`:

- `BRIDGE-SPEC.mod10-horner`
- `BRIDGE-SPEC.floordiv10-horner`
- `BRIDGE-SPEC.mod10-expanded`
- `BRIDGE-SPEC.quotient-expanded`

The expanded remainder claim has the same guarded arithmetic rewrite as
`rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a`,
framed by an arbitrary `REST:K`. The expanded quotient claim likewise
corresponds exactly to
`rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d`.
The two Horner claims additionally connect fixed MPY `applyBin` execution to
those arithmetic results.

The proof ordering and import boundary are explicit in the mounted artifacts:

1. `/reference/k-proof/bridge-verification.k` imports only the supplied `MPY`
   module and contains neither simplification rule.
2. `/reference/k-proof/prove.sh` compiles that bridge-free module and runs:

   ```sh
   kprove bridge-spec.k \
     --definition bridge-verification-kompiled \
     --spec-module BRIDGE-SPEC
   ```

3. Only after that command does `prove.sh` compile
   `/reference/k-proof/verification.k`, which contains the simplification
   rules.
4. `/reference/k-proof/bridge-proof.log` records all four claims and contains
   an exact `#Top` line; `prove.sh` checks that success line before proceeding.

None of these four claims is itself a `source_rule_id` in the canonical
inventory. Consequently there is no canonical rule classified
`PROVED_DERIVED_LEMMA`. In particular, the two exact rule counterparts remain
`DOMAIN_LEMMA` because the task explicitly restricts every rule carrying
`simplification` to `DEFINITION` or `DOMAIN_LEMMA`; the separate proofs are
recorded here as their Stage 1 justification evidence.
