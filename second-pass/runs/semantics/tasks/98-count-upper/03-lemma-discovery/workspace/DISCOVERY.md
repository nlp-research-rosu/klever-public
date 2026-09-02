# Trust-boundary discovery

The canonical inventory identifies two rules in the local
`COUNT-UPPER-VERIFICATION` module. Each rule is classified exactly once, and
both are `DEFINITION`.

- `rule-10b63a2e2225cd457dcf51887aec2f5c265ce7e5117c82e30a96da4d69dce4ab`
  is the base equation for the named mathematical summary
  `countUpperFrom(IntSeq, Bool)`. It defines the count of an empty code
  sequence as zero.
- `rule-dbe614f8b007441a5b97fefaac5825ae89bddf38faf17cc47420c3c905ada5d1`
  is the structural recurrence for the same summary. It accounts for the head
  character when its position is even and it belongs to `AEIOU`, then recurs
  on the tail after toggling parity.

These equations describe the mathematical result used by the loop invariant;
they do not execute Python configurations, inspect operational cells, or add
an independent mathematical fact beyond the definition of that result.
Neither rule has the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` first
compiles `verification.k` into `verification-kompiled`, so both inventoried
rules are already present in the proof definition. It then runs `kprove` on
`spec.k`, whose claims prove the loop invariant and the end-to-end function
property using that definition. No Stage 1 command first proves either exact
inventoried rule statement against a module from which that rule is absent.
Therefore neither rule qualifies as `PROVED_DERIVED_LEMMA`.

There are no `OPERATIONAL_RULE` entries in the local verification-module
inventory: all operational Python behavior comes from the imported reference
semantics rather than from either inventoried local rule.

The `DOMAIN_LEMMA` set is empty.
