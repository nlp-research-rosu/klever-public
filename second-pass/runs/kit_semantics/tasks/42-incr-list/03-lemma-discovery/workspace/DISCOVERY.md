# Trust-boundary discovery

## Canonical source

The exhaustive source is `/reference/rule-inventory.json`, with canonical
`inventory_sha256`:

```text
e5ea14caf9f22c1087c2aa07a466c55d4997f2cd117345f37fa56fb8353ec40b
```

It contains eight rules, all from module `VERIFICATION`. Classification follows
that inventory's order and does not add claims or rules from outside the
canonical closure.

## Classification

All eight rules are `DEFINITION`.

| Inventory position | Source rule | Reason |
|---:|---|---|
| 0 | `rule-ea9ef756a199853827a586359d8f870476c308a30f0eeddad81ed1ced5c1534f` | `isNumericVal` constructor case for `Int` |
| 1 | `rule-eb56166732daec8d40953b1a816a0c32e93ece7bbf820f66cac61cfed1f4ca23` | `isNumericVal` constructor case for `Bool` |
| 2 | `rule-f1ada8e553470df79e923850e9a82e4ade7d8b82de56eded497f90ba526c9b0a` | `isNumericVal` constructor case for `Float` |
| 3 | `rule-304ee5c0da386cdc923ba4c73cc1f6dd81caf237937dabfdc90aeed8214fa4c2` | Exhaustive `[owise]` case completing `isNumericVal` |
| 4 | `rule-f75f569f79b2c115362441fba7806717279c1238ce0191528cc1eb8220a50c99` | Empty-sequence base equation for `allNumeric` |
| 5 | `rule-0599900824f5015e8454b006675aebe384009350a1ba7e6c7f893c8f3f2c7fff` | Structural recurrence for `allNumeric` |
| 6 | `rule-dfc5044ec376f017835fd3fb82e8d9f45dd942408b63f2e73bf8d69e88ec62f1` | Empty-remainder base equation for `incrAcc` |
| 7 | `rule-2c9fbc7cd6f99b65dbc48f9711be674cb9780c46cb33ec56bd27b7846bb99640` | Structural recurrence defining the `incrAcc` summary |

The `isNumericVal` group defines a named predicate by disjoint constructor
cases and an exhaustive `owise` complement. The `allNumeric` group defines a
predicate by structural recursion over `ValSeq`. The `incrAcc` group defines
the mathematical accumulator summary by structural recursion over the
remaining sequence. None of these rules matches a configuration cell or
performs program execution.

No canonical rule carries the `simplification` attribute. The only listed
attribute is `owise` on the complement case of `isNumericVal`, and that rule is
classified as `DEFINITION`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k` with all
eight canonical rules present:

```text
kompile --backend haskell verification.k --main-module VERIFICATION ...
```

It then proves the claims in `spec.k`. It does not first prove the exact
statement of any canonical rule against a module from which that rule is
absent, so none satisfies the required proof-before-installation ordering.

`SPEC.loop-inv` is independently machine-checked and Stage 1 records `#Top` in
`loop-proof.out`, but it is a reachability claim rather than a rule in the
canonical inventory. It therefore creates no `PROVED_DERIVED_LEMMA` entry in
`trust-boundary.json`.

## Other classification sets

- `OPERATIONAL_RULE`: empty. Every canonical rule is a pure function equation;
  fixed-semantics execution remains in the imported reference semantics.
- `DOMAIN_LEMMA`: empty. The domain predicates are defined by constructor
  equations; no additional mathematical fact is installed as a trusted rule.

The domain-lemma set is explicitly empty.

## Coverage result

- Canonical rules: 8
- Classified exactly once: 8
- `DEFINITION`: 8
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The JSON preserves canonical inventory order and uses only the required object
and entry fields.
