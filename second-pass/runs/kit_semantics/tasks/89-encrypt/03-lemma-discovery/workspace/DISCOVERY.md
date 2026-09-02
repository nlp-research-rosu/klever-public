# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with canonical
`inventory_sha256`
`21e3419f1942121a9fa0035fd52d04a450b0359c12014aa2545fe788fed4d6d8`.
It contains nine rules, all from the mounted Stage 1 `VERIFICATION` module.
`trust-boundary.json` preserves their inventory order and classifies each
`source_rule_id` exactly once.

No canonical rule has the `simplification` attribute. The declarations
containing these rules are proof-local total functions, and none of their
rules matches a K configuration, source-language expression, call, loop, or
other execution redex.

## Classifications

All nine rules are `DEFINITION`:

| Inventory position | Source rule | Defined role |
|---:|---|---|
| 1 | `rule-a2cf8a164cbf94a5a3d7e444fbdaf3102628d2d0fecf228f37fd79d4dece6873` | Equation defining the per-character `rot4Code` summary |
| 2 | `rule-d0417986ed3df602be0bfac4ca4cca3508a931dd5e1f044c0f0c1403dda203c7` | Below-alphabet guarded case of `encryptedChar` |
| 3 | `rule-235635117bf711de90184aa7ad59620fe6b55936d3bbd90d5bb3b6a779d23518` | Lowercase-alphabet guarded case of `encryptedChar` |
| 4 | `rule-7fd0c0a9b39e8cb02242fc4650209b4e029307a059efc848cc10aeb01bec0b3e` | Above-alphabet guarded case of `encryptedChar` |
| 5 | `rule-5a9a473afba1abcdb4a753006cdb3325c9531614b72a97d3ae145928cb54c00e` | Empty-sequence base equation of `encryptFold` |
| 6 | `rule-6d8f5b2a6f2c94349997e8605406de5e3a62f684322db20582a216c99de16051` | Constructor recurrence of `encryptFold` |
| 7 | `rule-85d0bc26ae10c2b14fd916a400f96b49f796f68ed4a275143ca218d6795865b0` | Wrapper equation defining `encryptResult` |
| 8 | `rule-5e6f27b3aa1140b7b8710b50f99a56ad029c2c48b9706918c0973fff130113a2` | Empty-sequence base equation of `finalLoopChar` |
| 9 | `rule-f55a8da87fb92ce9e96ebbc4ea82ce71e9cee705e034c1c7003d546479f625c2` | Constructor recurrence of `finalLoopChar` |

The three `encryptedChar` guards are the cases of one total definition. The
`encryptFold` and `finalLoopChar` pairs are structural recurrences whose
recursive calls consume the tail constructor. `encryptResult` is a named
initialization of `encryptFold`. These rules name proof summaries; fixed MPY
rules continue to execute the program in the Stage 1 claims.

No inventory rule is an `OPERATIONAL_RULE`: the canonical closure contains no
ordinary execution or observation rule added by `VERIFICATION`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

The mounted Stage 1 `prove.sh` first compiles `verification.k`, so all nine
canonical rules are present in `verification-kompiled` before it invokes:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That command proves the `SPEC.encrypt-loop` and `SPEC.encrypt-entry`
reachability claims under the already compiled definitions. It does not first
prove the exact statement of any canonical rule against a module from which
that rule is absent. The `spec-vacuity.k` and `spec-body-mutation.k` commands
are expected-failure probes and likewise are not evidence of a separately
proved reusable rule.

## Domain lemmas

The domain-lemma set is empty. No canonical rule adds an independent
mathematical fact beyond the equations and structural recurrences that define
the proof summaries.
