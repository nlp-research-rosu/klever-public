# K proof trust-boundary discovery

The canonical inventory has schema version 2, inventory SHA-256
`997f9d867d49fb42b1d83ee8bdd60f1713a245267682473af0e3d6032a48e174`,
and eight rules, all from `DIGITS-VERIFICATION`. The mounted
`verification.k` has SHA-256
`c1a6bf80154b292ad15a0eba97f4d80cf283d9c7906e8ceeb4d6db8e939010f3`,
matching the verification hash recorded by the inventory.

## Definitions

The first five inventory rules are `DEFINITION`:

1. `rule-707d2fff65d29fc33df78fa7df36a27570c6ead38e034ac0561a47af26b8cadd`
   is the zero-remaining-input base equation for `oddDigitProduct`.
2. `rule-72752e93fc84beda2568dfffa077ef72955a8f0f706517d875412fca8af59242`
   is its positive-input decimal recurrence and dispatches to `oddDigitStep`.
3. `rule-5b347c8a08e5a3787eb910773a322c40a260bd764f177d0ba72804d83ff940b9`
   defines the step for a digit that is not odd.
4. `rule-47bf10a3ae4840b8cea3e2bfa5c81034547e374f6a91f99094dc6e0291b4fcbd`
   defines the first-odd-digit case, where zero is the “none seen” sentinel.
5. `rule-108d879768555f310cc51819054b5d497269e3d4cf23cab9d938e93438b5bcc3`
   defines multiplication by a later odd digit.

These rules collectively define the named mathematical summary used in the
loop invariant and final correctness claim. They are not ordinary Python
execution rules, so no inventory entry is classified as `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 `prove.sh` first compiles `verification.k` into
`verification-kompiled` and only then invokes `kprove spec.k`. All eight
inventory rules—including all three simplifiers—are therefore already in the
proof definition used by `kprove`. The recorded `kprove.stdout` contains
`#Top`, which establishes the claims in `spec.k` under that definition, but it
does not demonstrate a prior proof of any simplifier's exact statement against
a module from which that simplifier was absent. No other mounted Stage 1
command or proof artifact supplies the required ordering and exact
correspondence.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of exactly these three
rules:

- `rule-4d51675c3f64dd8d5acd7f855e28f517fc1edc539220ae3724773ad4a26eded2`
  asserts the equality form of the recurrence when the current digit is not
  odd.
- `rule-3978fc0ec976783d9a30feccc0ac292802be0d3aecc09914bc975f6c302270b2`
  asserts the equality form for an odd digit with the zero sentinel
  accumulator.
- `rule-373920d268cfa5acff78b262ff1885548fb9bfba4fc32627ec554bbb6f424ebd`
  asserts the equality form for an odd digit with a nonzero accumulator.

Each carries the `simplification` attribute and rewrites an equality involving
the summary function to `true`. Although the source comment describes them as
exposing the defining recurrence, they are additional reusable equality facts
that close target-side comparisons. Because Stage 1 did not separately prove
them before including them, they form the trusted mathematical boundary.
