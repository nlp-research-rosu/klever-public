# Trust-boundary classification

The canonical inventory contains exactly two rules, in the `VERIFICATION`
module. Both rules define the mathematical summary `concatAcc` used in the
reachability claims:

- `rule-df6c6246e36176afc3c709b2cac7210c00527c8cbdd63317e19954afb58e6d9b`
  is `DEFINITION` because it is the empty-list base equation of the left fold.
- `rule-4785cdfafa15c19b300ac57d1f3eefe6562fc8e321341a00841e9a26112e2f64`
  is `DEFINITION` because it is the nonempty-list recurrence of that same left
  fold.

Neither rule is an `OPERATIONAL_RULE`: neither advances the translated Python
program or observes its machine state. Neither is a `DOMAIN_LEMMA`: the rules
introduce the meaning of `concatAcc` rather than asserting an additional
mathematical fact. Neither is a `PROVED_DERIVED_LEMMA`: `prove.sh` does not
first prove either exact equation against a module that omits it.

Stage 1 does contain one separately proved and reused derived reachability
lemma, the claim labelled `SPEC.concatenate-loop` in `spec.k`. Its proof
evidence is the ordering in `prove.sh`:

1. `kprove spec.k --definition semantic-kompiled --claims SPEC.concatenate-loop`
   first discharges that exact labelled claim.
2. `kprove spec.k --definition semantic-kompiled --trusted SPEC.concatenate-loop`
   then reuses the same claim as a trusted circularity while proving the
   end-to-end claim.

`SPEC.concatenate-loop` is a specification claim, not a rule in the canonical
verification-module inventory, so it has no entry in `trust-boundary.json`.
There are no separately proved derived lemmas among the inventoried rules.

The domain-lemma set is empty.
