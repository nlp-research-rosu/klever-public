# K proof trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory SHA-256 `abf5939fc8aa355bb81970ac2b1d2d6f440f70116c4662dbba6c00549cef528b`. It contains 13 rules from `EXCHANGE-VERIFICATION`.

## Classification

The two `#iterNext` rules are `OPERATIONAL_RULE` entries. They give the empty and nonempty execution transitions for the verification model's typed `intVals` representation. They are observations of that model's list iteration, not extra arithmetic or logical facts.

The remaining eleven rules are `DEFINITION` entries:

- Six equations define the base and parity-dependent recursive cases of `oddAcc` and `evenAcc`.
- Two conditional equations define the named result summary `exchangeResult`.
- Three macro expansions define `ODD-BODY`, `EVEN-BODY`, and `exchangeDef`.

The canonical inventory contains no rule with the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's `prove.sh` first compiles `verification.k`, so every canonical inventory rule is already present in `EXCHANGE-VERIFICATION`. It then runs one `kprove` command on `spec.k` against that compiled definition. The claims labeled `odd-loop`, `even-loop`, and `exchange-correct` are proved in `spec.k`, but none of those claim statements is a canonical inventory rule, and Stage 1 does not first prove an exact inventory rule against a module that excludes it and then reuse it as a rule. Consequently, the required ordering and exact correspondence for `PROVED_DERIVED_LEMMA` are absent.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical rule is an additional trusted mathematical fact used to close the proof.

The resulting count is 2 operational rules, 11 definitions, 0 proved derived lemmas, and 0 domain lemmas, covering all 13 canonical rules exactly once.
