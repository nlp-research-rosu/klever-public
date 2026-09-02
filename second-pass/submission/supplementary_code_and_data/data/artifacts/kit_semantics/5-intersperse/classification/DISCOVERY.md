# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with inventory
identifier
`98d24755c0d3f453b048d563519170cd08da8c9b2f46b3546f105d537cb4fbe9`.
It contains four rules, all in `VERIFICATION`. The JSON output preserves their
inventory order and classifies each `source_rule_id` exactly once.

## Classifications

All four rules are `DEFINITION`:

1. `rule-e28394b585c4090679938a1fc2a49542a90c06f9fd53d8d2ea93cb550aecd2b6`
   expands the `INTERSPERSE-BODY` macro into the exact `Stmts` term used by the
   closure and loop claim. The associated syntax production carries `[macro]`;
   the rule defines a named proof term and does not survive as a runtime
   execution rule.
2. `rule-671fd3686197e0c91cef745f9b7af75d1bd0f7277cabab95a54dc8fbf6e1ef79`
   is the base equation of `intersperseAcc`: an empty remaining sequence returns
   the accumulator.
3. `rule-386331eb5a2c59cc86798243ff1afd3badb062dc83a886655fce827ef4f75b24`
   is the first-element recurrence of `intersperseAcc`: with an empty
   accumulator, it consumes the first remaining value without a delimiter.
4. `rule-b0a9306232910cc5bd1efab08c4f20853e642eec8176e7d9e7d39d1d46f375cd`
   is the subsequent-element recurrence of `intersperseAcc`: it appends the
   delimiter and next value and recurses on the strict tail of `REST`.

The three `intersperseAcc` rules are equations for a `[function, total]`
mathematical summary. Their constructor cases define the summary rather than
observe or advance the K configuration. None is an additional algebraic fact
about a previously defined symbol.

The `OPERATIONAL_RULE` set is empty. The local verification rules neither match
configuration cells nor replace or supplement execution steps. Operational
execution comes from the supplied `MPY` semantics, outside the canonical local
verification-module inventory.

No canonical rule carries the `simplification` attribute.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

There is no Stage 1 ordering evidence in which the exact statement of any
canonical rule is first proved against a module omitting that rule and only
then added for reuse. `/reference/k-proof/prove.sh` first compiles
`verification.k` with all four canonical rules present and then invokes
`kprove` on `spec.k`. Consequently, the successful `#Top` result does not turn
any of these already-imported definitions into a separately proved derived
lemma.

`SPEC.loop-invariant` is a reachability claim in `spec.k` and is described in
Stage 1 as a derived lemma used coinductively. It is not a rule in the canonical
inventory, so it is not an entry in `trust-boundary.json` and does not justify
reclassifying any of the four inventoried rules.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. The local verification-module closure adds no
trusted mathematical fact beyond the four named definitions above.
