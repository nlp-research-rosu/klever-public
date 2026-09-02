# K proof trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains two
rules, in the following inventory order. Both are definitions.

1. `rule-13a0bacbae0b39374d726ce54a37713ed37ed4f9b136c8829c84c5044ee37b5e`
   expands `solutionProgram` to the exact `Module(FuncDef(...))` constructor
   tree. The associated `Program ::= "solutionProgram"` syntax production is
   marked `[macro]` in Stage 1 `verification.k`. This is a named proof-term
   definition.
2. `rule-f4d1b4e43e3df7c9420c834d8d784562f282a07d1aab2b46e86f475bea400230`
   expands `RunAnyInt(X, Y, Z)` to
   `Invoke(solutionProgram, X, Y, Z)`. Its syntax production is likewise
   marked `[macro]`, and the rule is a structural wrapper definition.

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
operational execution rules reside in `MPY-SEMANTICS`, but the launcher states
that the supplied inventory is exhaustive and canonical for this
classification task; those semantic rules have no canonical
`source_rule_id` entries and therefore are not added to the output.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 `prove.sh` compiles
`ANY-INT-VERIFICATION` with both inventory rules already present and then runs
`kprove` on the seven claims in `spec.k`. It does not first prove either exact
rule statement against a module omitting that rule, so the required
proof-before-use evidence does not exist.

## Domain lemmas

The domain-lemma set is empty. Neither inventory rule supplies an additional
mathematical fact; both only expand named macro terms. The inventory also
contains no rule carrying the `simplification` attribute.
