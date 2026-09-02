# K proof trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with embedded
inventory hash
`11c89cc35585dc358ff90ecb064dc19d96b1288ea183620d0fdeb33f28bdc46d`.
It contains 38 rules in the local `VERIFICATION`-module closure. The
classification in `trust-boundary.json` preserves that order and assigns each
canonical `source_rule_id` exactly once.

## Classification result

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 28 | Classifier equations, sequence predicates and recurrences, accumulator summaries, projection-helper definitions, and the exact closure-syntax macro |
| `OPERATIONAL_RULE` | 0 | Every operational rule in the canonical closure has separately proved Stage 1 connection evidence |
| `PROVED_DERIVED_LEMMA` | 3 | Bridge-free universal reachability claims precede installation of the corresponding reusable transition rules |
| `DOMAIN_LEMMA` | 7 | Symbolic cast orientations, cast-definedness facts, and the guarded `intOf` correspondence are imported assumptions rather than separately proved lemmas |

All rules carrying a `simplification` attribute are classified as either
`DEFINITION` or `DOMAIN_LEMMA`.

## Definitions

The following groups define proof-local names rather than assert additional
facts about program results:

- `integralV` and `floatV` define mutually exclusive modeled numeric
  classifiers.
- Empty/cons equations for `allIntegral`, `allNumeric`, and `hasFloat` define
  structural predicates over `ValSeq`.
- The equations for `sumInts`, `sumFloatRest`, and `sumToFloat` define
  accumulator summaries by recursion on the strict sequence tail, including
  their explicit off-domain totalization cases.
- `reverseSlice` defines a name for the exact `buildVS` traversal.
- The sorted identity and guarded Val-to-projection equations for
  `projectIntTotal`, `projectBoolTotal`, and `projectFloatTotal` define those
  proof-local projection helpers. The two guarded `intLikeTotal` equations
  define the modeled Int/Bool conversion summary.
- `willItFlyClosure` is a macro for the exact translated closure syntax; it
  does not replace lookup, call, binding, body execution, or return.

## Separately proved derived lemmas

Exactly three canonical rules qualify.

### Reverse-slice transition

Canonical rule:
`rule-2c28a35276cc6a362988e024fe349cea1d30d7ecae33a6f4e36274e57eff1425`.

Stage 1 first compiles `verification.k` with
`--main-module SUMMARY-DEFINITION` into `connection-kompiled`.
`SUMMARY-DEFINITION` imports `VERIFICATION-BASE`, not `VERIFICATION`, so the
canonical reverse operational rule is absent. Then `prove.sh` runs:

```text
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module SUM-CONNECTION
```

The proved claim `SUM-CONNECTION.reverse-slice` has the same
`someB(-1) ~> #slStep(list(VS), noB, noB)` source, the same
`#alloc(list(reverseSlice(VS)))` destination, and the same arbitrary
continuation. Stage 1 records `#Top`, exit 0. Only afterward does `prove.sh`
compile `--main-module VERIFICATION`, which installs the reusable rule.

### Integral sum-fold transition

Canonical rule:
`rule-d13390ee12bb568d6ae90c95e9b2775c482f3676255a20bcfb3ab2ec0c868edf`.

The same bridge-free `connection-kompiled` build proves
`SUM-CONNECTION.sum-fold` with the identical
`#iterNext(list(VS)) ~> #sumCont(ACC) => sumInts(ACC, VS)` transition and an
arbitrary continuation. The claim assumes `allIntegral(VS)`, a broader domain
than the installed rule's
`allIntegral(VS) andBool notBool hasFloat(VS)` guard, so the proved transition
specializes exactly to every rule match. Stage 1 records `#Top`, exit 0, before
the later `VERIFICATION` compilation installs the rule.

### Float-containing sum-fold transition

Canonical rule:
`rule-8baf5b1816cf4d527c6421dfb6aa4fa022d589cd1ac2f991393fc77ef9ede209`.

After the bridge-free `SUM-CONNECTION.float-rest-fold` proof, `prove.sh`
compiles `--main-module FLOAT-REST-VERIFICATION` and proves:

```text
kprove float-connection-spec.k \
  --definition float-connection-kompiled \
  --spec-module FLOAT-SUM-CONNECTION
```

That definition contains the independently connected float-rest transition
but does not contain the canonical initial-accumulator rule from
`VERIFICATION`. The `FLOAT-SUM-CONNECTION.float-sum-fold` claim has the same
`#iterNext(list(VS)) ~> #sumCont(ACC) => sumToFloat(ACC, VS)` transition and
arbitrary continuation. Its `allNumeric(VS) andBool hasFloat(VS)` domain is
broader than the installed rule's additional `notBool allIntegral(VS)`
conjunct. Stage 1 records `#Top`, exit 0, before the subsequent
`--main-module VERIFICATION` build installs the reusable rule.

The intermediate float-rest operational rule is not a canonical inventory
entry because it is outside the launcher-declared `VERIFICATION` closure; it
is therefore evidence for the third rule, not an additional item to classify.

## Domain lemmas

The domain-lemma set is **not empty**. It contains seven canonical rules:

- `rule-ec583fc3f12bafee23d7f302c742e52ce776b44b86fb0ae71114dc6dcdb3bb9f`
  and
  `rule-90eb7f013a9e927996889600de0ac06a1c48fe1f32ff329772fa38b5022a8a28`
  for Int projection orientation and definedness;
- `rule-3905ebe2499ea5ede82420688c2f2bdadaaf27ab8b44aef52876a9281ba13c4e`
  and
  `rule-223d04d630bd21ce9624149f41397f24c0af78120813951d1f3ef073273e8a83`
  for Bool projection orientation and definedness;
- `rule-aea328b93abee3d0539e019d0745462924337ff6c0e980f560da1a6fa1c0b72e`
  and
  `rule-725c0275ed9c194a24cc6686a7d8ac0e05163edac4687c027a68f98431430868`
  for Float projection orientation and definedness; and
- `rule-82314b210da1b2e71ed9cacdc03ed14b6f144d73a7db17b8f0b5688eb4d30e92`,
  which rewrites supplied `intOf` to the proof-local `intLikeTotal` summary
  under `integralV`.

These rules occur in `VERIFICATION-BASE`, so they are already present in
`SUMMARY-DEFINITION` and in every Stage 1 connection definition. The
connection claims demonstrate consequences under a theory containing these
rules; they do not first prove any of these exact rules against a module that
omits them. The Stage 1 comments and `PROOF.md` describe them as projection,
orientation, definedness, or guarded dispatch helpers, but that description
does not satisfy the required proof-order criterion. They are therefore the
explicit trusted mathematical boundary of the finalized K proof.

No theorem, replacement statement, Lean formulation, or alternative rule has
been added.
