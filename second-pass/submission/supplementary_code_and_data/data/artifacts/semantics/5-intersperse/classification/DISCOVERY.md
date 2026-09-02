# Trust-boundary discovery

The canonical inventory contains six rules, all from
`INTERSPERSE-VERIFICATION` in Stage 1 `verification.k`. The inventory contains
no rule with the `simplification` attribute.

## Classifications

All six rules are `DEFINITION`:

- `rule-05af82756816da99d1e49a9f8d009c94185476c6c7d0fb7678256f49b7839b01`
  is the empty-input base equation for `intersperseAcc`.
- `rule-a69c7f927a81762ea2c4fbf188360727e079a96344cde3099709abd953299501`
  defines the empty-accumulator/first-element recurrence for
  `intersperseAcc`.
- `rule-96273f0b4eae15373ec58939dbd00740dde58870a697d93b32a5a4bd04ed197b`
  defines the nonempty-accumulator recurrence, including insertion of the
  delimiter before the next value.
- `rule-9be9c742f13371df267a06b8e67ec2e35592c9ac3cd5aa5b772100f6bf8c3abe`
  defines the named result summary `intersperseVS` by starting
  `intersperseAcc` with an empty accumulator.
- `rule-20166af5adb55b2aa1e6c90c631d9e6c733f576541555c546a5a90c9a7e7f3b7`
  is the empty-tail base equation for `lastNumber`.
- `rule-1602c9e6a845786876a75dac174363782ca1ac8b767d2e5f3baca81621fbc25b`
  is the structural recurrence for `lastNumber`.

These are equations and structural recurrences for terms declared
`[function, total]`. They define mathematical summaries used in the loop
claims; they do not execute Python constructs or observe machine state.
Consequently, the inventory has no `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` as
`INTERSPERSE-VERIFICATION` and then runs `kprove` on `spec.k` against that
already-compiled definition. Thus all six inventoried rules are present before
the four reachability claims are proved. Stage 1 contains no earlier proof
against a module lacking any one of these rules, followed by addition of an
exactly corresponding reusable rule. The claims in `spec.k` prove loop and
end-to-end reachability properties, but they are not inventoried rewrite rules
and do not establish the required staged provenance for a derived-lemma
classification.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule adds a trusted mathematical
fact beyond the defining equations of the named summaries.
