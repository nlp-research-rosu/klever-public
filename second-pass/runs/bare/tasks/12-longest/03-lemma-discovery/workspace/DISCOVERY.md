# Trust-boundary discovery

The canonical inventory contains 18 rules, all from `VERIFICATION`, in the
order preserved by `trust-boundary.json`.

## Definitions

Thirteen rules are `DEFINITION`:

- `rule-db9420e8fd1c4626595b79b7ea2e6307a53b03fc99d9a63570388395764ad474`
  and
  `rule-79576cfe9c9b959c7fa701acac35d9e135e225f3fdeb54b5effd615e4a16a951`
  expand the named loop-body and full-program proof terms.
- `rule-cf8b57d453a6eeb1d815ece37d5946c5fead470f5c67daf85939a3638bd36896`,
  `rule-7f473637b44742359337a6ea4b8811bbced9fc57f43365394878fa092f0337db`,
  and
  `rule-0eb9fd5516c5c09a4385fa1fb3ce068e72e602071ec62aa60e1aca23a6648342`
  define the structural encoding of mathematical string lists as runtime
  values.
- `rule-d522a0d2a80d77bf23fff3789a4c9cc1dee3902e31f1443c813bc6cbc8bd5e20`,
  `rule-0632983b57909c5400dca4ed74248b5d09a3914a9a277a31c21c50ec82e29e7f`,
  `rule-bb0ed98a5e6ea08b1f41e028d4ab4f62da3a797dbe6f3b3a6b0fb0b0be94ec3b`,
  `rule-e2ea59e583e9aba4f56686bbb8c31703b58b4e536d869f118bf4f3f066a4c42b`,
  and
  `rule-41608496e24b276d61c515e55ec432cae88d14f9e1bdb34b9983811ac7afe643`
  define the empty/nonempty contract summary and its first-longest fold.
- `rule-e4633a59660c5ec7ead77cb473c04e9f0d1cdbe206f021fdb481ce4081ba04f7`,
  `rule-64119d60105d2cb544dd81225851d868a9c84ab75c122076ae4a088d7f4cf1ab`,
  and
  `rule-2c6384deca5d2eff6d3d334e4b29720ab4673a16bc8a4f57ad4341881f7e6cc3`
  define the indexed symbolic-sequence fold used by the loop invariant and
  postcondition.

These are equations, macro expansions, encodings, or recurrences. They define
named terms and summaries rather than asserting extra mathematical facts.

## Operational rules

Five rules are `OPERATIONAL_RULE`:

- `rule-b0f0333a8289ed42bf63f5f68911b09e710cd5d1f3945ffceead604fd31c6755`
  and
  `rule-e69efc7581406d022b7856deb7b0903c7ce4f89a28c7ba8668b210fa8eeb1f44`
  implement empty/nonempty observations for the symbolic sequence model.
- `rule-b1717a1cb9f20abb2c92ed3d8bb9f5dfc66a3f417779b528e3fcddc52cf5e014`
  implements its head observation.
- `rule-f224022b33a01068dbf84152f03ad2c24f192cea0b778266eb7958ce3e3c07ca`
  and
  `rule-6217bfa50b953d6505f0f15ac2a66ceb8481b6397d4eea8a5ca19a91b3cef5da`
  implement loop termination and one-step iteration over that model.

These rules describe execution or observations, not standalone mathematical
lemmas.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 `prove.sh` first compiles
the complete `verification.k`, containing all 18 inventory rules, and then
runs one `kprove` command against that compiled module. It does not first prove
any inventory rule against a module lacking that rule, nor does it subsequently
add a proved statement as a reusable rule. The claims in `spec.k` are proof
goals, but their exact statements are not reintroduced as inventory rules.

## Domain lemmas and simplification rules

The domain-lemma set is explicitly empty. The canonical inventory also reports
no rule carrying the `simplification` attribute, so the required restriction
on simplification-rule classifications is satisfied vacuously.
