# Trust-boundary discovery

The canonical inventory has SHA-256
`2f8b212c17f86ce405005dc29a58c94ce010a10384580bdedeaa3c8b15778416`
and contains 11 rules. Every inventory rule is represented exactly once in
`trust-boundary.json`, in canonical inventory order.

## Classification summary

- **DEFINITION — 10 rules.** The three `factorizeStep`, `factorizeBody`, and
  `factorizeDef` rules are macro expansions for named program terms. The three
  `factorLoop` rules define its base, divisible, and nondivisible recurrence;
  `primeFactors` defines its initial invocation. The three `factorDivisor`
  rules likewise define that proof-summary recurrence.
- **PROVED_DERIVED_LEMMA — 1 rule.** The rule labeled
  `factorize-loop-lemma` is the promoted loop-summary claim.
- **OPERATIONAL_RULE — 0 rules.** The local verification modules add no
  unproved execution or observation rule. Execution behavior is supplied by
  the imported Stage 1 MPY semantics and is outside this canonical local-rule
  inventory.
- **DOMAIN_LEMMA — 0 rules.** The domain-lemma set is empty.

The inventory contains no rule carrying the `simplification` attribute.

## Separately proved derived lemma

The sole separately proved derived lemma is
`rule-7a0b234f2c7d2f2e9f5ca663b20c6f7b0d9cfa7eb71ea38b3a1681cb48235035`.
Its rewrite over the `k`, `env`, `scopes`, and `heap` cells, together with
`N >=Int 1 andBool D >=Int 2`, is the same statement as the
`factorize-loop` claim in `FACTORIZE-LOOP-SPEC`. The promoted rule adds only
the operational metadata `priority(40)` and
`label(factorize-loop-lemma)`; these attributes do not change the proved
rewrite or precondition.

The Stage 1 proof ordering is explicit in `prove.sh`:

1. It compiles `verification.k` with main module
   `FACTORIZE-VERIFICATION`. That module imports `MPY` and does not import
   `FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA`, so the promoted rule is absent
   from this proof definition.
2. It runs `kprove` on `FACTORIZE-LOOP-SPEC`, whose `factorize-loop` claim is
   therefore proved against the base module without the derived rule.
3. Only afterward does it compile
   `FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA`, which imports the base module and
   contains the matching rule, and use that definition to prove
   `FACTORIZE-SPEC`.

This establishes both the required proof-before-use ordering and the exact
correspondence needed for the `PROVED_DERIVED_LEMMA` classification.
