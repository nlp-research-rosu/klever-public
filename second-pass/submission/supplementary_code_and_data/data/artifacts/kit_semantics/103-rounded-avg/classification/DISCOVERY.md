# Trust-boundary discovery

## Canonical scope

The sole classification source is
`/reference/rule-inventory.json`, whose copied inventory digest is
`c56fede9da88c87be21505bdccb01640677a3e69700202e3ff3859734027c180`.
It contains four rules, all in module `VERIFICATION`.
`trust-boundary.json` preserves their inventory order and includes each
canonical `source_rule_id` exactly once.

The mounted Stage 1 files were used only to determine rule behavior and proof
ordering. No rule outside the canonical inventory was added to the JSON.

## Classifications

### Operational rule

`rule-856b350eb7e5e0b8b4439c4c371b7848357d072149e50a9a7359680b877be187`
is `OPERATIONAL_RULE`.

This is the priority-40 binary-loop bridge in `verification.k:8-38`. It matches
the translated `while value > 1` computation, consumes that computation from
the `<k>` cell, and updates the active scope from `value = V` and
`digits = A` to `value = 1` and `digits = loopDigits(V,A)`. It therefore
models execution and state observation. It is not a definition of a
mathematical symbol and is not an additional free-standing mathematical fact.

Stage 1 gives the operational rule strong prior evidence:

1. `prove.sh:25-28` compiles `verification-base.k` as
   `connection-kompiled`. That module does not import `verification.k` and
   therefore does not contain the priority bridge.
2. `prove.sh:29-31` proves
   `LOOP-CONNECTION.binary-loop-exact` from `connection-spec.k`.
3. Only afterward, at `prove.sh:36-39`, does the script compile
   `verification.k`, which introduces the priority bridge.

The connection claim covers the same loop syntax, arbitrary continuation,
environment, scopes, positive-`V` and `allBits(A)` guards, unshadowed `chr`
binding, and `value`/`digits` transition. Its stronger postcondition also
records the numeric and bit-shape observations. This prior connection evidence
justifies the bridge, but it does not change the rule's behavioral
classification: the inventoried rule itself is an operational transition.

### Domain lemmas

`rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804`
is `DOMAIN_LEMMA`.

It simplifies the combined `bitWeight` and `bitValue` observation of
`loopDigits(V,A)` to the corresponding accumulator invariant for
`V > 0` and `allBits(A)`. The rule defines no new symbol; it asserts a
mathematical property of the already defined `loopDigits`, `bitWeight`, and
`bitValue` functions. It also carries the `simplification` attribute, which
limits its allowed classification to `DEFINITION` or `DOMAIN_LEMMA`.

`rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52`
is `DOMAIN_LEMMA`.

It is a syntactically normalized version of the same invariant whose left
side begins with `1 * bitWeight(...)`. It still defines no fresh named term and
instead adds a reusable guarded mathematical equality. No Stage 1 auxiliary
claim states this exact normalized rule before it is installed.

`rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f`
is `DOMAIN_LEMMA`.

It simplifies `allBits(loopDigits(V,A))` to `true` when `V > 0` and `A`
already contains only bit character codes. This is a preservation fact about
existing definitions, not a recurrence, macro expansion, or defining equation
for a new proof term. It carries the `simplification` attribute and therefore
cannot be classified as `PROVED_DERIVED_LEMMA` under the requested rules.

The domain-lemma set is **not empty**. It contains exactly the latter three
canonical rule IDs.

## Separately proved derived-lemma evidence

There are no canonical inventory entries classified
`PROVED_DERIVED_LEMMA`.

Two canonical domain lemmas nevertheless have exact earlier K proof evidence:

- The equality in
  `rule-8310e1f4464214d1a36b421c21b8d0b34d095a4184d5b03438744e7709fd7804`
  is the first conjunct of the `ensures` clause at
  `connection-spec.k:36-39`.
- The preservation fact in
  `rule-555ac2e26b8914f371e3c4e9148f353eb28acaaa57ec7204eaaac93ef182837f`
  is the second conjunct of that same `ensures` clause.

`prove.sh:25-31` compiles and proves that claim against
`VERIFICATION-BASE`, before `prove.sh:36-39` compiles the module containing
the inventoried simplification rules. Thus the mounted evidence demonstrates
both ordering and exact correspondence for those two facts. They remain
`DOMAIN_LEMMA` in the JSON because the task explicitly requires every
`simplification` rule to be either `DEFINITION` or `DOMAIN_LEMMA`, and neither
rule is definitional.

The normalized rule
`rule-6e9c2e5d70c22424d8d31241e77f4a57bfa09c7fdc7184626d62f64c7ef9fd52`
does not have an exact separately stated Stage 1 claim. It is related by the
ordinary integer identity eliminating multiplication by one, but that
relationship is not the exact pre-installation proof required for
`PROVED_DERIVED_LEMMA`.

Stage 1 also proves two Euclidean reconstruction claims in
`arithmetic-spec.k` against `ARITHMETIC-VERIFICATION` before compiling
`verification-base.k`. Their corresponding source rules are not entries in
the launcher-generated canonical inventory. They are consequently not added
to `trust-boundary.json` and receive no classification in this discovery
artifact.

## Counts

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 1
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 3
- Total: 4
