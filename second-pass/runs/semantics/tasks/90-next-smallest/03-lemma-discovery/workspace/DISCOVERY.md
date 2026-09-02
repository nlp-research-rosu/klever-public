# Trust-boundary discovery

The canonical inventory hash is
`fa23b9c4607ef517134979f874e704c9629ea9852e1eeb73ba5642663a693ab5`.
All 19 inventory rules are classified exactly once and remain in canonical
inventory order in `trust-boundary.json`.

## Classification summary

- 16 `DEFINITION` rules:
  - four macro expansions defining `nextSmallestLoopBody`,
    `nextSmallestReturn`, `nextSmallestBody`, and `solutionModule`;
  - four structural observer equations defining `intsEmpty`, `intsHead`, and
    `intsTail`;
  - eight base/recursive equations defining the `nsScan` mathematical summary.
- 2 `OPERATIONAL_RULE` rules implementing the empty and yielding observations
  of the symbolic integer-sequence iterator.
- 0 `PROVED_DERIVED_LEMMA` rules.
- 1 `DOMAIN_LEMMA`, the installed loop-summary rule
  `rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba`.

No canonical rule has the `simplification` attribute.

## Separately proved derived lemmas and Stage 1 evidence

No inventory rule qualifies as a separately proved derived lemma under the
required exact-statement criterion.

Stage 1 does contain a staged proof attempt:

1. `prove.sh` lines 31–40 compile
   `NEXT-SMALLEST-VERIFICATION`, which excludes the installed rule, and prove
   `NEXT-SMALLEST-LOOP-SPEC`. `loop-proof.out` contains `#Top`.
2. `prove.sh` lines 43–51 then compile
   `NEXT-SMALLEST-WITH-LOOP-LEMMA`, which includes the rule, and prove the
   entry claim. `entry-proof.out` also contains `#Top`.

However, the first claim and the installed rule are not exact statements. In
`spec.k` lines 22–32, the claim's final `<scopes>` cell is the unconstrained
existential `?FINAL_SCOPES:Map`. In `verification.k` lines 116–132, the
installed rule instead fixes that cell to the original scopes map updated by
deleting location 1. Proving reachability to an arbitrary existential map does
not establish that more specific consequent. The comment calling the rule a
proved lemma therefore does not justify `PROVED_DERIVED_LEMMA`.

## Domain-lemma boundary

The domain-lemma set is **not empty**. It contains exactly the installed
loop-summary rule identified above. That rule is an additional trusted fact
used to close the entry-point proof because its exact, stronger scope effect
was not first proved against a definition that omitted it.
