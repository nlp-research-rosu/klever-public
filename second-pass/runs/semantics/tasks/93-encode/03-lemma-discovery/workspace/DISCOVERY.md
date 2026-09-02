# Trust-boundary discovery

The canonical inventory identifies eight rules in the `ENCODE-VERIFICATION`
module. Every inventory entry has an empty attribute list, so in particular
none carries the `simplification` attribute.

All eight rules are classified as `DEFINITION`:

- `encodeLoopBody` and `encodeFunctionBody` are macro expansions naming the
  exact program statement sequences used in the claims.
- `isVowelCode` defines the contract's vowel predicate by its ten ASCII code
  points.
- The two conditional `encodeCode` equations are the exhaustive vowel and
  non-vowel cases of the single-character encoding function.
- The two `encodeAcc` equations are its base and recursive accumulator cases.
- `encodeCodes` defines the public mathematical summary using an empty
  accumulator.

These equations introduce and unfold named proof terms; they do not add
independent mathematical facts and are not ordinary execution or observation
rules. Accordingly, the inventory contains no `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` compiles `verification.k` as
`ENCODE-VERIFICATION` and then invokes `kprove` on `spec.k`. The proved
statements are the three reachability claims `encode-total`, `encode-init`,
and `encode-loop`. None of those claims is the exact statement of an
inventory rule, and Stage 1 does not first prove any inventory rule against a
module from which that rule is absent. Thus the mounted evidence does not
satisfy the required ordering and exact-correspondence test for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact used to close the proof.
