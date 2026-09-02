# Trust-boundary discovery

The canonical inventory contains eight rules from `BELOW-ZERO-COMMON` and
`MPY-VERIFICATION-LEMMA`. Each is classified exactly once and retained in
canonical inventory order in `trust-boundary.json`.

## Definitions

Five rules are `DEFINITION`:

- `rule-37490b390355d40b96a24fb6238d94c721dd106775648ef6adf702d0f018a945`
  expands the `belowZeroLoopBody` macro.
- `rule-7ad011f4ad8584143ada5134978d05f498d1696b3f046f0aafd22e1826e11e5d`
  expands the `belowZeroFunctionBody` macro.
- `rule-f0df05e0e38700aa105eb11f7349ed86c708125ba2ed7016c90aeb1231ddfdc2`
  expands `solutionProgram` to the translated module term.
- `rule-7ec387f9629680162121a42c4d6abab222bfc61592daa736e9caca2524fa4f39`
  is the empty-sequence equation of `prefixBelow`.
- `rule-2c07a06a5689cd1d706ba5a69e6209e1668dc73225ce9c4bbd9b06ff4f661a03`
  is the recursive equation of `prefixBelow`.

These rules name or recursively define proof terms and the mathematical result
against which execution is checked. They do not introduce independent domain
facts.

## Operational verification-model rules

Two rules are `OPERATIONAL_RULE`:

- `rule-333fe6107e77ab191c2f76ba40e090e2476f94d001c790092147629f8518d311`
  implements the empty
  `#iterNext` observation for `asValSeq(.IntVals)`.
- `rule-8a249bc8e455d2bdc6fd578ff3452bd8220f754f9622c7679e0505ee4b9f4fd6`
  implements the nonempty `#iterNext` observation, yielding the `Int`-sorted
  head and the symbolic tail.

They are ordinary execution rules for the symbolic integer-list carrier used
by the verification model. They mirror the empty and cons iterator cases in
`MPY-LIST`; they are not separately asserted mathematical lemmas.

## Separately proved derived lemma

Exactly one rule is `PROVED_DERIVED_LEMMA`:

- `rule-f5db78ced6090ff9fb5c369808923c5e0a9d90c895bad6c69844f2b05f7c04e1`
  summarizes execution of the `below_zero` loop and function-frame return as
  `prefixBelow(B, IS)`.

The Stage 1 evidence establishes the required ordering and correspondence:

1. `spec.k` states this same loop reachability transition as the sole
   `AUX-SPEC` claim.
2. The first symbolic definition in `prove.sh` is compiled with
   `--main-module MPY-VERIFICATION`. That module imports only
   `BELOW-ZERO-COMMON` and therefore does not contain the summary rule, which
   resides in `MPY-VERIFICATION-LEMMA`.
3. `prove.sh` runs `kprove ... --spec-module AUX-SPEC` against that base
   definition.
4. Only afterward does `prove.sh` compile
   `--main-module MPY-VERIFICATION-LEMMA` and use the proved transition, with
   scheduling attribute `priority(40)`, to prove `MAIN-SPEC`.

The rule and auxiliary claim have the same K term, cell transitions, frame
shape, and result. The priority attribute controls reuse scheduling and does
not replace or weaken the proved statement.

## Domain lemmas and simplification rules

The `DOMAIN_LEMMA` set is empty. The canonical inventory also contains no rule
with the `simplification` attribute.
