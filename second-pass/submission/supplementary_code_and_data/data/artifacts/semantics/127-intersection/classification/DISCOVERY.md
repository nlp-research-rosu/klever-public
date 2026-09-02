# K proof trust-boundary discovery

The canonical inventory hash is
`2b8a9ab9483d01691862d6f17b9f749f531528c3930e42996b1feddba2790f04`.
All 12 inventory rules are classified exactly once and remain in canonical
inventory order in `trust-boundary.json`.

## Classification summary

| Classification | Count | Role |
|---|---:|---|
| `DEFINITION` | 10 | Named MPY-body expansions, answer encodings, the primality recurrence, and the overlap-length summary |
| `OPERATIONAL_RULE` | 0 | No local rule is merely an added execution or observation rule |
| `PROVED_DERIVED_LEMMA` | 1 | The reusable loop summary proved before installation |
| `DOMAIN_LEMMA` | 1 | The unproved symbolic Map normalization fact |

The two body equations expand `intersectionBody` and `divisorBody`. The two
answer equations define `yesV` and `noV`. Five equations define the
`primeFrom`/`primeResult` mathematical recurrence, and one defines
`overlapLength`. These are definitions because they introduce or expand named
proof terms and summaries rather than asserting independent facts about
pre-existing operations.

The rule
`rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0`
is a `DOMAIN_LEMMA`. It asserts that updating the known Map binding at key 1
to `undef` exposes the disjoint remainder. It is described in
`verification.k` as a proof-only normalization and a concrete map fact. It
does not define a new symbol, is not an ordinary program execution rule, and
is not the target of a separate Stage 1 proof.

## Separately proved derived lemma

Exactly one rule qualifies as `PROVED_DERIVED_LEMMA`:
`rule-3564ec1a0c7873a21e248d06a49acdb05fe46af166b68d498bbff1afc2702e72`.

The Stage 1 evidence establishes the required ordering:

1. `spec.k` defines the `loop-correct` claim in `LOOP-SPEC`, which imports
   `VERIFICATION-BASE`.
2. `VERIFICATION-BASE` ends before the reusable summary rule and therefore
   does not contain it.
3. `prove.sh` first compiles `verification.k` with
   `--main-module VERIFICATION-BASE` and proves `loop-correct` with `kprove`.
4. Only after that proof command does `prove.sh` compile
   `--main-module VERIFICATION`, whose additional rule installs the loop
   summary for the final `intersection-correct` proof.
5. The installed rule is the proved claim after expanding the definitional
   abbreviation `divisorBody` and alpha-renaming unused local-frame variables.
   Its configuration rewrites, continuation, range state, precondition, and
   `primeFrom(LENGTH, DIVISOR)` result correspond to the proved claim.

The domain-lemma set is **not empty**. It contains exactly the single Map
tombstone-normalization rule identified above.
