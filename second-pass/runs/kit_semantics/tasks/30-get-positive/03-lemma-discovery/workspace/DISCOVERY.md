# Trust-boundary discovery

## Canonical input and method

`/reference/rule-inventory.json` was treated as the exhaustive canonical rule
inventory for the local verification-module closure. Its embedded
`inventory_sha256` is:

```text
22a541b7d4934594e95b3772f125d9c1872b0d6b37d91b7d26eb5f7bcb7908fa
```

The inventory contains 10 rules, in modules `VERIFICATION-BASE` and
`VERIFICATION`. Each canonical `source_rule_id` appears exactly once and in the
same order in `trust-boundary.json`.

Classification totals:

- `DEFINITION`: 9
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 1

## Definitions

The following rules are defining equations or structural recurrences:

1. `rule-b241ce9f2bd7347fcfdf85ef6584e8b5bd3d4cbf1d60172dbccd972353a6263b`
   defines `numericVal`.
2. `rule-66cf82d7237685a06ca264938d829ef692b6502a47052bc8b2f6955fe66a6b93`
   and
   `rule-17c621b67d0aacf118bb323f41413fea744bb561265d52ff628c37ad78cc2cd9`
   are the empty and cons equations defining `numericVals`.
3. `rule-6617447b31c170258fdc23f4b1ca0dc4b3f7c945e50c08d4e290381d3e24508f`,
   `rule-b7d6ce82ec2a2ac7221e232a8762ec40e0c5f8a33688ec923438f1197c35a783`,
   and
   `rule-569442f388c8214bce6f506695671575b195c7d000bcc61c81f57507abc8eeae`
   are the Int, Float, and nonnumeric equations defining the total
   `positiveNumeric` predicate.
4. `rule-f59962ae3cbf101799667bef7e71cd44e7fc5067b67f94493ee34bff8c007791`,
   `rule-88784a48ac7e5083100f357cdc7fcd5856f28ba2c5b93d4a5efd4a85eb3dfae2`,
   and
   `rule-6f46b6b7356839cbf0b867220b1e1216ff7a93fb8ba127ad7cd2a420f744ecf2`
   are the empty, positive-head, and nonpositive-head equations defining the
   terminating `filterPositive` recurrence.

The three `filterPositive` rules carry `simplification`, but their role remains
definitional: each is an equation for the newly introduced summary symbol, and
the cases define its structural recursion.

## Operational rules

No canonical rule is classified `OPERATIONAL_RULE`. The canonical closure
contains proof-local summaries and one cross-symbol simplification, not an
ordinary execution or observation rule added as part of the verification
model. Rules from the supplied MPY semantics are outside this canonical local
inventory.

## Separately proved derived lemmas

There are no canonical rules eligible for `PROVED_DERIVED_LEMMA`.

Stage 1 does contain related connection evidence:

- `/reference/k-proof/prove.sh` lines 19–25 first compile
  `verification.k` with main module `VERIFICATION-BASE`, then run
  `kprove spec-connection.k` against that definition.
- `/reference/k-proof/connection-kompiled/mainModule.txt` records
  `VERIFICATION-BASE`, which excludes the guarded rule in module
  `VERIFICATION`.
- `/reference/k-proof/spec-connection.k` lines 9–35 contain four connection
  claims: end-to-end `Compare` claims and direct `applyCmp` claims, separately
  specialized to `I:Int` and `F:Float`.
- `/reference/k-proof/proof-run.log` line 161 records `#Top` for that connection
  proof. The direct `applyCmp` claims are also reported as trivial after
  simplification at lines 157–160.

This evidence is ordered before the full `VERIFICATION` build, but none of
those claims is the exact canonical generic statement
`applyCmp(">", V:Val, 0.0) => positiveNumeric(V) requires numericVal(V)`.
The inventory rule instead combines the static cases behind a dynamic
`V:Val` guard. Moreover, that rule carries `simplification`, for which the
allowed classifications are restricted to `DEFINITION` or `DOMAIN_LEMMA`.
Consequently, no inventory entry is labeled `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0
```

That rule rewrites the pre-existing MPY `applyCmp` operator to the proof-local
`positiveNumeric` summary whenever `numericVal(V)` holds. It does not define a
new symbol on its left-hand side, and it is not an ordinary execution rule.
It is therefore an additional cross-symbol mathematical fact used during
simplification. The Stage 1 static connection claims support the intended Int
and Float cases, but under the exact-statement criterion they do not remove the
generic guarded rule from the trusted domain-lemma boundary.

## Structural validation

The completed JSON was checked against the canonical inventory for:

- exact `schema_version` 2;
- exact copied `inventory_sha256`;
- exactly three top-level keys;
- exactly 10 rule entries;
- exact inventory order;
- one occurrence of every canonical `source_rule_id`;
- exactly the required three keys in every entry;
- an allowed classification and nonempty rationale for every entry; and
- `DEFINITION` or `DOMAIN_LEMMA` for every rule carrying `simplification`.
