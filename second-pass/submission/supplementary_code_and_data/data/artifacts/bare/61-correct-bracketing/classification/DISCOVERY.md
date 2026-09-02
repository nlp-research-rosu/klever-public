# Trust-boundary discovery

The canonical inventory contains five rules from `MPY-VERIFICATION`.

- `solutionProgram` is a structural definition: it expands a named proof term into the translated constructor AST used by the claims.
- The four `bracketSpec` rules are the base case and recursive clauses defining the mathematical summary of the bracket scan. Their `simplification` attributes make those defining equations available during symbolic proof, but they do not assert additional mathematical facts.

Accordingly, every inventory rule is classified as `DEFINITION`. The inventory contains no `OPERATIONAL_RULE`, no rule eligible for `PROVED_DERIVED_LEMMA`, and no `DOMAIN_LEMMA`.

## Separately proved derived lemma

Stage 1 has one separately proved derived lemma, the labeled reachability claim `SPEC.loop` in `spec.k` lines 9–32. The evidence and ordering are:

1. `prove.sh` lines 32–33 build `verification-kompiled` from `verification.k`; that module does not contain `SPEC.loop`.
2. `prove.sh` lines 34–35 invoke `kprove` with `--claims SPEC.loop`, proving that exact labeled claim against `verification-kompiled`.
3. `prove.sh` lines 36–37 invoke `kprove` again with `--trusted SPEC.loop`, reusing the same claim for the remaining proofs only after the separate proof command.

`SPEC.loop` is a claim in `spec.k`, not a rule in the canonical verification-module inventory. It therefore has no `rules` array entry to classify as `PROVED_DERIVED_LEMMA`.

The domain-lemma set is empty.
