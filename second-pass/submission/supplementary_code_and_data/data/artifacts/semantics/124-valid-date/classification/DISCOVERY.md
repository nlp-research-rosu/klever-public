# Trust-boundary discovery

The canonical inventory has SHA-256
`aa03a783afce0185a257e19022038c87fe753a5e88184b59db7f63deb69599f5`
and contains seven rules, all from `VALID-DATE-VERIFICATION`. The inventory
contains no rule carrying the `simplification` attribute.

## Classification

All seven rules are classified as `DEFINITION`.

- `validDateBody` expands a named proof term to the translated target-function
  body.
- `validDateClosure` and `validDateModule` are structural definitions that
  package that body as a closure and module.
- `digitCode`, `dateNumber`, and `dateLimit` define the component mathematical
  summaries used by the contract.
- `validDate10` defines the complete executable contract summary for an input
  represented by ten character codes.

These rules introduce the program term and contract vocabulary used by the
claims. They do not add independent mathematical facts beyond those
definitions. There are no local `OPERATIONAL_RULE` classifications: ordinary
execution behavior comes from the imported reference semantics, and the
launcher-provided inventory is canonical and exhaustive for the local
verification-module closure.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` with
`VALID-DATE-VERIFICATION` as the main module and then invokes `kprove` on
`spec.k` using that compiled definition. Consequently, all seven inventory
rules are already present in the definition used for the proof. Stage 1 does
not first prove the exact statement of any inventory rule against a module
that omits that rule, so none qualifies as `PROVED_DERIVED_LEMMA`. The two
claims in `spec.k` are target correctness claims rather than reusable
inventory rules. The Stage 1 proof logs record `#Top`, but that result does not
change the introduction order of the seven rules.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact used to close the proof; every inventory rule is a
definition of a named program or contract term.
