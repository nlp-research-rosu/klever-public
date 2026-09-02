# Trust-boundary discovery

The canonical inventory contains four rules, all from the `VERIFICATION`
module. Together they define the mathematical summary `#vowels`:

- the empty-string base equation;
- the recurrence that adds one for an ordinary vowel;
- the equation for a final `y` or `Y`; and
- the fallback recurrence that continues with the string tail.

Each is therefore classified as `DEFINITION`. None is an
`OPERATIONAL_RULE`: these rules characterize the result summary rather than
executing the translated Python program. None is a `DOMAIN_LEMMA`: no
additional mathematical fact appears in the canonical inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` compiles
`verification.k` as module `VERIFICATION`, so all four inventoried rules are
already present in the compiled definition. It then invokes `kprove` on the
claims in `spec.k`; it does not first prove any inventoried rule against a
module that excludes that rule, nor does it subsequently introduce such a
proved rule. Consequently, none meets the evidence requirement for
`PROVED_DERIVED_LEMMA`.

The domain-lemma set is explicitly empty.
